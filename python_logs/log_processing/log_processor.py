#!/usr/bin/env python3
"""
日志处理脚本
对日志进行清洗、格式化、转换和异常检测
"""

import os
import re
import json
import logging
import argparse
import pandas as pd
from datetime import datetime, timedelta
from pathlib import Path
import hashlib

class LogProcessor:
    def __init__(self, input_dir, output_dir, config=None):
        """初始化日志处理器"""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.config = config or {}
        self.setup_logging()
        
        # 数据清洗规则
        self.cleaning_rules = {
            'remove_empty_lines': True,
            'remove_duplicates': True,
            'normalize_timestamps': True,
            'filter_noise': True,
            'anonymize_ips': self.config.get('anonymize_ips', False)
        }
        
        # 异常检测规则
        self.anomaly_rules = {
            'high_error_rate': 10,  # 错误率超过10%
            'unusual_traffic': 1000,  # 单IP请求超过1000次
            'suspicious_patterns': [
                r'\.\./',  # 路径遍历
                r'<script',  # XSS攻击
                r'union.*select',  # SQL注入
                r'eval\(',  # 代码注入
            ]
        }
    
    def setup_logging(self):
        """设置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'processor.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_parsed_logs(self):
        """加载已解析的日志数据"""
        csv_file = self.input_dir / 'parsed_logs.csv'
        if csv_file.exists():
            return pd.read_csv(csv_file)
        
        # 如果没有CSV文件，尝试加载JSON
        json_file = self.input_dir / 'analysis_results.json'
        if json_file.exists():
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            # 这里需要根据实际JSON结构来提取日志数据
            return pd.DataFrame()
        
        self.logger.error("未找到可处理的日志数据文件")
        return pd.DataFrame()
    
    def clean_data(self, df):
        """数据清洗"""
        self.logger.info("开始数据清洗")
        original_count = len(df)
        
        # 移除空行
        if self.cleaning_rules['remove_empty_lines']:
            df = df.dropna(subset=['raw_line'] if 'raw_line' in df.columns else df.columns[:1])
        
        # 移除重复行
        if self.cleaning_rules['remove_duplicates']:
            # 基于内容生成哈希值来检测重复
            if 'raw_line' in df.columns:
                df['content_hash'] = df['raw_line'].apply(lambda x: hashlib.md5(str(x).encode()).hexdigest())
                df = df.drop_duplicates(subset=['content_hash'])
                df = df.drop('content_hash', axis=1)
        
        # 标准化时间戳
        if self.cleaning_rules['normalize_timestamps'] and 'timestamp' in df.columns:
            df['normalized_timestamp'] = df['timestamp'].apply(self.normalize_timestamp)
        
        # IP地址匿名化
        if self.cleaning_rules['anonymize_ips'] and 'ip' in df.columns:
            df['ip'] = df['ip'].apply(self.anonymize_ip)
        
        # 过滤噪音数据
        if self.cleaning_rules['filter_noise']:
            df = self.filter_noise(df)
        
        cleaned_count = len(df)
        self.logger.info(f"数据清洗完成: {original_count} -> {cleaned_count} 条记录")
        
        return df
    
    def normalize_timestamp(self, timestamp_str):
        """标准化时间戳格式"""
        if pd.isna(timestamp_str):
            return None
        
        # 常见时间格式
        formats = [
            '%d/%b/%Y:%H:%M:%S',
            '%Y-%m-%d %H:%M:%S',
            '%b %d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d %H:%M:%S.%f'
        ]
        
        for fmt in formats:
            try:
                dt = datetime.strptime(str(timestamp_str).split()[0], fmt)
                return dt.strftime('%Y-%m-%d %H:%M:%S')
            except ValueError:
                continue
        
        return timestamp_str
    
    def anonymize_ip(self, ip):
        """IP地址匿名化"""
        if pd.isna(ip):
            return ip
        
        try:
            parts = str(ip).split('.')
            if len(parts) == 4:
                # 保留前两段，后两段用xxx替换
                return f"{parts[0]}.{parts[1]}.xxx.xxx"
        except:
            pass
        
        return ip
    
    def filter_noise(self, df):
        """过滤噪音数据"""
        # 过滤明显的爬虫和机器人请求
        bot_patterns = [
            r'bot',
            r'crawler',
            r'spider',
            r'scraper'
        ]
        
        if 'message' in df.columns:
            for pattern in bot_patterns:
                df = df[~df['message'].str.contains(pattern, case=False, na=False)]
        
        return df
    
    def detect_anomalies(self, df):
        """异常检测"""
        self.logger.info("开始异常检测")
        anomalies = []
        
        # 检测高错误率
        if 'status' in df.columns:
            error_count = len(df[df['status'].astype(str).str.startswith(('4', '5'))])
            total_count = len(df)
            error_rate = (error_count / total_count) * 100 if total_count > 0 else 0
            
            if error_rate > self.anomaly_rules['high_error_rate']:
                anomalies.append({
                    'type': 'high_error_rate',
                    'value': error_rate,
                    'threshold': self.anomaly_rules['high_error_rate'],
                    'description': f'错误率过高: {error_rate:.2f}%'
                })
        
        # 检测异常流量
        if 'ip' in df.columns:
            ip_counts = df['ip'].value_counts()
            for ip, count in ip_counts.items():
                if count > self.anomaly_rules['unusual_traffic']:
                    anomalies.append({
                        'type': 'unusual_traffic',
                        'ip': ip,
                        'count': count,
                        'threshold': self.anomaly_rules['unusual_traffic'],
                        'description': f'IP {ip} 请求次数异常: {count}'
                    })
        
        # 检测可疑模式
        content_columns = ['message', 'url', 'raw_line']
        for col in content_columns:
            if col in df.columns:
                for pattern in self.anomaly_rules['suspicious_patterns']:
                    matches = df[df[col].str.contains(pattern, case=False, na=False, regex=True)]
                    if not matches.empty:
                        anomalies.append({
                            'type': 'suspicious_pattern',
                            'pattern': pattern,
                            'count': len(matches),
                            'description': f'检测到可疑模式 "{pattern}": {len(matches)} 次'
                        })
        
        self.logger.info(f"异常检测完成，发现 {len(anomalies)} 个异常")
        return anomalies
    
    def transform_data(self, df):
        """数据转换"""
        self.logger.info("开始数据转换")
        
        # 添加派生字段
        if 'normalized_timestamp' in df.columns:
            df['hour'] = pd.to_datetime(df['normalized_timestamp']).dt.hour
            df['day_of_week'] = pd.to_datetime(df['normalized_timestamp']).dt.dayofweek
            df['date'] = pd.to_datetime(df['normalized_timestamp']).dt.date
        
        # 状态码分类
        if 'status' in df.columns:
            df['status_category'] = df['status'].astype(str).apply(self.categorize_status)
        
        # URL路径提取
        if 'url' in df.columns:
            df['url_path'] = df['url'].apply(lambda x: str(x).split('?')[0] if pd.notna(x) else x)
            df['has_query'] = df['url'].apply(lambda x: '?' in str(x) if pd.notna(x) else False)
        
        # 文件大小分类
        if 'size' in df.columns:
            df['size_category'] = pd.to_numeric(df['size'], errors='coerce').apply(self.categorize_size)
        
        return df
    
    def categorize_status(self, status):
        """状态码分类"""
        try:
            code = int(status)
            if 200 <= code < 300:
                return 'success'
            elif 300 <= code < 400:
                return 'redirect'
            elif 400 <= code < 500:
                return 'client_error'
            elif 500 <= code < 600:
                return 'server_error'
            else:
                return 'unknown'
        except:
            return 'unknown'
    
    def categorize_size(self, size):
        """文件大小分类"""
        if pd.isna(size):
            return 'unknown'
        
        try:
            size_bytes = float(size)
            if size_bytes < 1024:
                return 'small'
            elif size_bytes < 1024 * 1024:
                return 'medium'
            elif size_bytes < 10 * 1024 * 1024:
                return 'large'
            else:
                return 'very_large'
        except:
            return 'unknown'
    
    def generate_summary_stats(self, df, anomalies):
        """生成汇总统计"""
        stats = {
            'processing_timestamp': datetime.now().isoformat(),
            'total_records': len(df),
            'anomalies_count': len(anomalies),
            'data_quality': {
                'completeness': {},
                'validity': {}
            }
        }
        
        # 数据完整性检查
        for col in df.columns:
            null_count = df[col].isnull().sum()
            stats['data_quality']['completeness'][col] = {
                'null_count': int(null_count),
                'null_percentage': float(null_count / len(df) * 100)
            }
        
        # 按类别统计
        if 'status_category' in df.columns:
            stats['status_distribution'] = df['status_category'].value_counts().to_dict()
        
        if 'hour' in df.columns:
            stats['hourly_distribution'] = df['hour'].value_counts().sort_index().to_dict()
        
        return stats
    
    def run_processing(self):
        """运行完整处理流程"""
        self.logger.info("开始日志处理")
        
        # 加载数据
        df = self.load_parsed_logs()
        if df.empty:
            self.logger.error("没有可处理的数据")
            return
        
        # 数据清洗
        df_cleaned = self.clean_data(df)
        
        # 数据转换
        df_transformed = self.transform_data(df_cleaned)
        
        # 异常检测
        anomalies = self.detect_anomalies(df_transformed)
        
        # 生成统计信息
        stats = self.generate_summary_stats(df_transformed, anomalies)
        
        # 保存处理结果
        # 保存清洗后的数据
        df_transformed.to_csv(self.output_dir / 'processed_logs.csv', index=False)
        
        # 保存异常报告
        with open(self.output_dir / 'anomalies.json', 'w', encoding='utf-8') as f:
            json.dump(anomalies, f, indent=2, ensure_ascii=False)
        
        # 保存统计信息
        with open(self.output_dir / 'processing_stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
        
        self.logger.info("日志处理完成")
        
        return {
            'processed_data': df_transformed,
            'anomalies': anomalies,
            'stats': stats
        }

def main():
    parser = argparse.ArgumentParser(description='日志处理工具')
    parser.add_argument('--input', required=True, help='输入目录（包含解析后的日志）')
    parser.add_argument('--output', required=True, help='输出目录')
    parser.add_argument('--config', help='配置文件路径')
    args = parser.parse_args()
    
    config = {}
    if args.config:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = json.load(f)
    
    processor = LogProcessor(args.input, args.output, config)
    processor.run_processing()

if __name__ == '__main__':
    main()