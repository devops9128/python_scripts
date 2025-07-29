#!/usr/bin/env python3
"""
日志分析脚本
解析和分析各种格式的日志文件，提取关键信息和统计数据
"""

import os
import re
import json
import logging
import argparse
import pandas as pd
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
import gzip

class LogAnalyzer:
    def __init__(self, input_dir, output_dir):
        """初始化日志分析器"""
        self.input_dir = Path(input_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
        # 常用日志格式正则表达式
        self.log_patterns = {
            'apache_access': r'(?P<ip>\S+) \S+ \S+ \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\S+)',
            'nginx_access': r'(?P<ip>\S+) - \S+ \[(?P<timestamp>[^\]]+)\] "(?P<method>\S+) (?P<url>\S+) (?P<protocol>\S+)" (?P<status>\d+) (?P<size>\d+)',
            'syslog': r'(?P<timestamp>\w+\s+\d+\s+\d+:\d+:\d+) (?P<hostname>\S+) (?P<process>\S+): (?P<message>.*)',
            'application': r'(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[(?P<level>\w+)\] (?P<message>.*)'
        }
        
    def setup_logging(self):
        """设置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'analyzer.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def detect_log_format(self, sample_lines):
        """检测日志格式"""
        for format_name, pattern in self.log_patterns.items():
            matches = 0
            for line in sample_lines[:10]:  # 检查前10行
                if re.match(pattern, line):
                    matches += 1
            
            if matches >= len(sample_lines) * 0.7:  # 70%匹配率
                return format_name, pattern
        
        return 'unknown', None
    
    def parse_log_file(self, file_path):
        """解析单个日志文件"""
        self.logger.info(f"解析日志文件: {file_path}")
        
        try:
            # 处理压缩文件
            if file_path.suffix == '.gz':
                with gzip.open(file_path, 'rt', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            else:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
            
            if not lines:
                return []
            
            # 检测日志格式
            format_name, pattern = self.detect_log_format(lines)
            self.logger.info(f"检测到日志格式: {format_name}")
            
            parsed_logs = []
            
            if pattern:
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    match = re.match(pattern, line)
                    if match:
                        log_entry = match.groupdict()
                        log_entry['line_number'] = line_num
                        log_entry['file_name'] = file_path.name
                        log_entry['format'] = format_name
                        parsed_logs.append(log_entry)
            else:
                # 未知格式，按行处理
                for line_num, line in enumerate(lines, 1):
                    line = line.strip()
                    if line:
                        parsed_logs.append({
                            'line_number': line_num,
                            'file_name': file_path.name,
                            'format': 'unknown',
                            'raw_line': line
                        })
            
            return parsed_logs
            
        except Exception as e:
            self.logger.error(f"解析文件失败 {file_path}: {e}")
            return []
    
    def analyze_access_logs(self, logs):
        """分析访问日志"""
        if not logs:
            return {}
        
        df = pd.DataFrame(logs)
        
        analysis = {
            'total_requests': len(df),
            'unique_ips': df['ip'].nunique() if 'ip' in df.columns else 0,
            'status_codes': df['status'].value_counts().to_dict() if 'status' in df.columns else {},
            'top_ips': df['ip'].value_counts().head(10).to_dict() if 'ip' in df.columns else {},
            'top_urls': df['url'].value_counts().head(10).to_dict() if 'url' in df.columns else {},
            'methods': df['method'].value_counts().to_dict() if 'method' in df.columns else {},
        }
        
        # 错误分析
        if 'status' in df.columns:
            error_logs = df[df['status'].astype(str).str.startswith(('4', '5'))]
            analysis['error_count'] = len(error_logs)
            analysis['error_rate'] = len(error_logs) / len(df) * 100
        
        return analysis
    
    def analyze_application_logs(self, logs):
        """分析应用日志"""
        if not logs:
            return {}
        
        df = pd.DataFrame(logs)
        
        analysis = {
            'total_entries': len(df),
            'log_levels': df['level'].value_counts().to_dict() if 'level' in df.columns else {},
        }
        
        # 错误和警告统计
        if 'level' in df.columns:
            error_logs = df[df['level'].isin(['ERROR', 'FATAL'])]
            warning_logs = df[df['level'] == 'WARNING']
            
            analysis['error_count'] = len(error_logs)
            analysis['warning_count'] = len(warning_logs)
        
        return analysis
    
    def analyze_security_events(self, logs):
        """分析安全事件"""
        security_patterns = [
            r'failed login',
            r'authentication failed',
            r'invalid user',
            r'brute force',
            r'sql injection',
            r'xss attack',
            r'unauthorized access'
        ]
        
        security_events = []
        
        for log in logs:
            content = log.get('message', '') or log.get('raw_line', '')
            for pattern in security_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    security_events.append({
                        'type': pattern,
                        'content': content,
                        'file': log.get('file_name'),
                        'line': log.get('line_number')
                    })
        
        return {
            'total_security_events': len(security_events),
            'events_by_type': Counter([event['type'] for event in security_events]),
            'events': security_events[:100]  # 限制返回数量
        }
    
    def generate_time_analysis(self, logs):
        """生成时间分析"""
        time_analysis = {
            'hourly_distribution': defaultdict(int),
            'daily_distribution': defaultdict(int)
        }
        
        for log in logs:
            timestamp_str = log.get('timestamp')
            if timestamp_str:
                try:
                    # 尝试解析不同的时间格式
                    for fmt in ['%d/%b/%Y:%H:%M:%S', '%Y-%m-%d %H:%M:%S', '%b %d %H:%M:%S']:
                        try:
                            dt = datetime.strptime(timestamp_str.split()[0], fmt)
                            time_analysis['hourly_distribution'][dt.hour] += 1
                            time_analysis['daily_distribution'][dt.strftime('%Y-%m-%d')] += 1
                            break
                        except ValueError:
                            continue
                except Exception:
                    continue
        
        return dict(time_analysis)
    
    def run_analysis(self):
        """运行完整分析"""
        self.logger.info("开始日志分析")
        
        all_logs = []
        file_analyses = {}
        
        # 处理所有日志文件
        for log_file in self.input_dir.glob('**/*'):
            if log_file.is_file() and (log_file.suffix in ['.log', '.gz'] or 'log' in log_file.name):
                logs = self.parse_log_file(log_file)
                all_logs.extend(logs)
                
                if logs:
                    # 按格式分析
                    format_type = logs[0].get('format', 'unknown')
                    
                    if format_type in ['apache_access', 'nginx_access']:
                        analysis = self.analyze_access_logs(logs)
                    elif format_type == 'application':
                        analysis = self.analyze_application_logs(logs)
                    else:
                        analysis = {'total_entries': len(logs)}
                    
                    file_analyses[str(log_file)] = analysis
        
        # 生成综合分析报告
        comprehensive_analysis = {
            'summary': {
                'total_files': len(file_analyses),
                'total_log_entries': len(all_logs),
                'analysis_timestamp': datetime.now().isoformat()
            },
            'file_analyses': file_analyses,
            'security_analysis': self.analyze_security_events(all_logs),
            'time_analysis': self.generate_time_analysis(all_logs)
        }
        
        # 保存分析结果
        output_file = self.output_dir / 'analysis_results.json'
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(comprehensive_analysis, f, indent=2, ensure_ascii=False)
        
        # 保存解析后的日志数据
        if all_logs:
            df = pd.DataFrame(all_logs)
            df.to_csv(self.output_dir / 'parsed_logs.csv', index=False)
        
        self.logger.info(f"分析完成，结果保存到: {output_file}")
        return comprehensive_analysis

def main():
    parser = argparse.ArgumentParser(description='日志分析工具')
    parser.add_argument('--input', required=True, help='输入日志目录')
    parser.add_argument('--output', required=True, help='输出分析结果目录')
    args = parser.parse_args()
    
    analyzer = LogAnalyzer(args.input, args.output)
    analyzer.run_analysis()

if __name__ == '__main__':
    main()