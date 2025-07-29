#!/usr/bin/env python3
"""
日志报告生成脚本
生成详细的日志分析报告，包括统计图表和可视化
"""

import os
import json
import logging
import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from pathlib import Path
from jinja2 import Template
import base64
from io import BytesIO

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class LogReporter:
    def __init__(self, analysis_dir, output_dir):
        """初始化日志报告生成器"""
        self.analysis_dir = Path(analysis_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.setup_logging()
        
        # 图表样式设置
        sns.set_style("whitegrid")
        plt.style.use('seaborn-v0_8')
    
    def setup_logging(self):
        """设置日志记录"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.output_dir / 'reporter.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_data(self):
        """加载分析数据"""
        data = {}
        
        # 加载处理后的日志数据
        processed_file = self.analysis_dir / 'processed_logs.csv'
        if processed_file.exists():
            data['logs'] = pd.read_csv(processed_file)
        
        # 加载异常数据
        anomalies_file = self.analysis_dir / 'anomalies.json'
        if anomalies_file.exists():
            with open(anomalies_file, 'r', encoding='utf-8') as f:
                data['anomalies'] = json.load(f)
        
        # 加载统计数据
        stats_file = self.analysis_dir / 'processing_stats.json'
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                data['stats'] = json.load(f)
        
        # 加载分析结果
        analysis_file = self.analysis_dir / 'analysis_results.json'
        if analysis_file.exists():
            with open(analysis_file, 'r', encoding='utf-8') as f:
                data['analysis'] = json.load(f)
        
        return data
    
    def create_status_chart(self, df):
        """创建状态码分布图"""
        if 'status_category' not in df.columns:
            return None
        
        plt.figure(figsize=(10, 6))
        status_counts = df['status_category'].value_counts()
        
        colors = ['#2ecc71', '#f39c12', '#e74c3c', '#9b59b6', '#95a5a6']
        plt.pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                colors=colors[:len(status_counts)])
        plt.title('HTTP状态码分布', fontsize=16, fontweight='bold')
        
        # 保存为base64
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_hourly_chart(self, df):
        """创建小时分布图"""
        if 'hour' not in df.columns:
            return None
        
        plt.figure(figsize=(12, 6))
        hourly_counts = df['hour'].value_counts().sort_index()
        
        plt.bar(hourly_counts.index, hourly_counts.values, color='#3498db', alpha=0.7)
        plt.xlabel('小时', fontsize=12)
        plt.ylabel('请求数量', fontsize=12)
        plt.title('24小时请求分布', fontsize=16, fontweight='bold')
        plt.xticks(range(0, 24))
        plt.grid(True, alpha=0.3)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_top_ips_chart(self, df):
        """创建Top IP访问图"""
        if 'ip' not in df.columns:
            return None
        
        plt.figure(figsize=(12, 8))
        top_ips = df['ip'].value_counts().head(10)
        
        plt.barh(range(len(top_ips)), top_ips.values, color='#e67e22')
        plt.yticks(range(len(top_ips)), top_ips.index)
        plt.xlabel('请求次数', fontsize=12)
        plt.ylabel('IP地址', fontsize=12)
        plt.title('Top 10 IP访问统计', fontsize=16, fontweight='bold')
        plt.gca().invert_yaxis()
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_daily_trend_chart(self, df):
        """创建日趋势图"""
        if 'date' not in df.columns:
            return None
        
        plt.figure(figsize=(14, 6))
        daily_counts = df['date'].value_counts().sort_index()
        
        plt.plot(daily_counts.index, daily_counts.values, marker='o', linewidth=2, 
                markersize=6, color='#9b59b6')
        plt.xlabel('日期', fontsize=12)
        plt.ylabel('请求数量', fontsize=12)
        plt.title('日访问趋势', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def create_size_distribution_chart(self, df):
        """创建文件大小分布图"""
        if 'size_category' not in df.columns:
            return None
        
        plt.figure(figsize=(10, 6))
        size_counts = df['size_category'].value_counts()
        
        plt.bar(size_counts.index, size_counts.values, color='#1abc9c', alpha=0.7)
        plt.xlabel('文件大小类别', fontsize=12)
        plt.ylabel('数量', fontsize=12)
        plt.title('文件大小分布', fontsize=16, fontweight='bold')
        plt.xticks(rotation=45)
        
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64
    
    def generate_html_report(self, data):
        """生成HTML报告"""
        template_str = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>日志分析报告</title>
    <style>
        body {
            font-family: 'Microsoft YaHei', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #34495e;
            border-left: 4px solid #3498db;
            padding-left: 15px;
            margin-top: 30px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .summary-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .summary-card h3 {
            margin: 0 0 10px 0;
            font-size: 14px;
            opacity: 0.9;
        }
        .summary-card .value {
            font-size: 28px;
            font-weight: bold;
        }
        .chart {
            text-align: center;
            margin: 30px 0;
        }
        .chart img {
            max-width: 100%;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .anomaly {
            background-color: #fff5f5;
            border: 1px solid #fed7d7;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
        }
        .anomaly-high {
            border-color: #fc8181;
            background-color: #fef5e7;
        }
        .anomaly-medium {
            border-color: #f6ad55;
            background-color: #fffaf0;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        .table th, .table td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }
        .table th {
            background-color: #f8f9fa;
            font-weight: bold;
        }
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #eee;
            color: #666;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>日志分析报告</h1>
        
        <div class="summary">
            <div class="summary-card">
                <h3>总记录数</h3>
                <div class="value">{{ stats.total_records if stats else 'N/A' }}</div>
            </div>
            <div class="summary-card">
                <h3>异常数量</h3>
                <div class="value">{{ stats.anomalies_count if stats else 'N/A' }}</div>
            </div>
            <div class="summary-card">
                <h3>处理时间</h3>
                <div class="value">{{ report_time }}</div>
            </div>
        </div>

        {% if charts.status_chart %}
        <h2>状态码分布</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ charts.status_chart }}" alt="状态码分布图">
        </div>
        {% endif %}

        {% if charts.hourly_chart %}
        <h2>24小时访问分布</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ charts.hourly_chart }}" alt="小时分布图">
        </div>
        {% endif %}

        {% if charts.top_ips_chart %}
        <h2>Top IP访问统计</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ charts.top_ips_chart }}" alt="Top IP图">
        </div>
        {% endif %}

        {% if charts.daily_trend_chart %}
        <h2>日访问趋势</h2>
        <div class="chart">
            <img src="data:image/png;base64,{{ charts.daily_trend_chart }}" alt="日趋势图">
        </div>
        {% endif %}

        {% if anomalies %}
        <h2>异常检测结果</h2>
        {% for anomaly in anomalies %}
        <div class="anomaly {% if anomaly.type == 'high_error_rate' %}anomaly-high{% else %}anomaly-medium{% endif %}">
            <strong>{{ anomaly.type }}</strong>: {{ anomaly.description }}
        </div>
        {% endfor %}
        {% endif %}

        <div class="footer">
            <p>报告生成时间: {{ report_time }}</p>
            <p>日志分析系统 v1.0</p>
        </div>
    </div>
</body>
</html>
        """
        
        template = Template(template_str)
        
        # 生成图表
        charts = {}
        if 'logs' in data and not data['logs'].empty:
            df = data['logs']
            charts['status_chart'] = self.create_status_chart(df)
            charts['hourly_chart'] = self.create_hourly_chart(df)
            charts['top_ips_chart'] = self.create_top_ips_chart(df)
            charts['daily_trend_chart'] = self.create_daily_trend_chart(df)
            charts['size_chart'] = self.create_size_distribution_chart(df)
        
        # 渲染模板
        html_content = template.render(
            stats=data.get('stats', {}),
            anomalies=data.get('anomalies', []),
            charts=charts,
            report_time=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        # 保存HTML报告
        html_file = self.output_dir / 'log_analysis_report.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def generate_json_report(self, data):
        """生成JSON格式报告"""
        report = {
            'report_metadata': {
                'generated_at': datetime.now().isoformat(),
                'version': '1.0',
                'type': 'log_analysis_report'
            },
            'summary': data.get('stats', {}),
            'anomalies': data.get('anomalies', []),
            'analysis_results': data.get('analysis', {})
        }
        
        # 添加统计摘要
        if 'logs' in data and not data['logs'].empty:
            df = data['logs']
            report['statistics'] = {
                'total_records': len(df),
                'unique_ips': df['ip'].nunique() if 'ip' in df.columns else 0,
                'date_range': {
                    'start': str(df['date'].min()) if 'date' in df.columns else None,
                    'end': str(df['date'].max()) if 'date' in df.columns else None
                }
            }
        
        json_file = self.output_dir / 'log_analysis_report.json'
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return json_file
    
    def generate_csv_summary(self, data):
        """生成CSV格式的汇总报告"""
        if 'logs' not in data or data['logs'].empty:
            return None
        
        df = data['logs']
        
        # 创建汇总统计
        summary_data = []
        
        # 按日期汇总
        if 'date' in df.columns:
            daily_summary = df.groupby('date').agg({
                'ip': 'nunique',
                'status_category': lambda x: (x == 'client_error').sum() + (x == 'server_error').sum()
            }).rename(columns={'ip': 'unique_ips', 'status_category': 'error_count'})
            
            daily_summary['total_requests'] = df.groupby('date').size()
            daily_summary['error_rate'] = (daily_summary['error_count'] / daily_summary['total_requests'] * 100).round(2)
            
            csv_file = self.output_dir / 'daily_summary.csv'
            daily_summary.to_csv(csv_file)
            
            return csv_file
        
        return None
    
    def run_reporting(self):
        """运行报告生成"""
        self.logger.info("开始生成日志报告")
        
        # 加载数据
        data = self.load_data()
        
        if not data:
            self.logger.error("没有可用的分析数据")
            return
        
        # 生成各种格式的报告
        reports = {}
        
        # HTML报告
        try:
            reports['html'] = self.generate_html_report(data)
            self.logger.info(f"HTML报告生成完成: {reports['html']}")
        except Exception as e:
            self.logger.error(f"HTML报告生成失败: {e}")
        
        # JSON报告
        try:
            reports['json'] = self.generate_json_report(data)
            self.logger.info(f"JSON报告生成完成: {reports['json']}")
        except Exception as e:
            self.logger.error(f"JSON报告生成失败: {e}")
        
        # CSV汇总
        try:
            csv_report = self.generate_csv_summary(data)
            if csv_report:
                reports['csv'] = csv_report
                self.logger.info(f"CSV汇总生成完成: {reports['csv']}")
        except Exception as e:
            self.logger.error(f"CSV汇总生成失败: {e}")
        
        self.logger.info("报告生成完成")
        return reports

def main():
    parser = argparse.ArgumentParser(description='日志报告生成工具')
    parser.add_argument('--analysis', required=True, help='分析结果目录')
    parser.add_argument('--report', required=True, help='报告输出目录')
    args = parser.parse_args()
    
    reporter = LogReporter(args.analysis, args.report)
    reporter.run_reporting()

if __name__ == '__main__':
    main()