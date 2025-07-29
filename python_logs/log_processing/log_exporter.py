#!/usr/bin/env python3
"""
日志输出脚本
将处理后的日志数据导出到各种目标系统
"""

import os
import json
import logging
import argparse
import pandas as pd
from datetime import datetime
from pathlib import Path
import smtplib
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from email.mime.base import MimeBase
from email import encoders

# 可选依赖导入
try:
    from sqlalchemy import create_engine, text
    HAS_SQLALCHEMY = True
except ImportError:
    HAS_SQLALCHEMY = False

try:
    import pymongo
    HAS_PYMONGO = True
except ImportError:
    HAS_PYMONGO = False

try:
    from elasticsearch import Elasticsearch
    HAS_ELASTICSEARCH = True
except ImportError:
    HAS_ELASTICSEARCH = False

try:
    import redis
    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

class LogExporter:
    def __init__(self, config_file):
        """初始化日志导出器"""
        self.config = self.load_config(config_file)
        self.setup_logging()
    
    def load_config(self, config_file):
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}
    
    def setup_logging(self):
        """设置日志记录"""
        log_config = self.config.get('logging', {})
        logging.basicConfig(
            level=getattr(logging, log_config.get('level', 'INFO')),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_config.get('file', 'exporter.log')),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def load_processed_data(self, data_dir):
        """加载处理后的数据"""
        data_path = Path(data_dir)
        
        # 加载处理后的日志
        logs_file = data_path / 'processed_logs.csv'
        logs_df = pd.read_csv(logs_file) if logs_file.exists() else pd.DataFrame()
        
        # 加载异常数据
        anomalies_file = data_path / 'anomalies.json'
        anomalies = []
        if anomalies_file.exists():
            with open(anomalies_file, 'r', encoding='utf-8') as f:
                anomalies = json.load(f)
        
        # 加载统计数据
        stats_file = data_path / 'processing_stats.json'
        stats = {}
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                stats = json.load(f)
        
        return {
            'logs': logs_df,
            'anomalies': anomalies,
            'stats': stats
        }
    
    def export_to_database(self, data, db_config):
        """导出到数据库"""
        if not HAS_SQLALCHEMY:
            self.logger.error("SQLAlchemy 未安装，无法导出到数据库")
            return False
        
        try:
            # 构建连接字符串
            db_type = db_config.get('type', 'mysql')
            host = db_config.get('host', 'localhost')
            port = db_config.get('port', 3306)
            username = db_config.get('username')
            password = db_config.get('password')
            database = db_config.get('database')
            
            if db_type == 'mysql':
                connection_string = f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
            elif db_type == 'postgresql':
                connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database}"
            elif db_type == 'sqlite':
                connection_string = f"sqlite:///{database}"
            else:
                self.logger.error(f"不支持的数据库类型: {db_type}")
                return False
            
            engine = create_engine(connection_string)
            
            # 导出日志数据
            if not data['logs'].empty:
                table_name = db_config.get('logs_table', 'log_entries')
                data['logs'].to_sql(table_name, engine, if_exists='append', index=False)
                self.logger.info(f"成功导出 {len(data['logs'])} 条日志记录到数据库表 {table_name}")
            
            # 导出异常数据
            if data['anomalies']:
                anomalies_df = pd.DataFrame(data['anomalies'])
                anomalies_df['created_at'] = datetime.now()
                table_name = db_config.get('anomalies_table', 'log_anomalies')
                anomalies_df.to_sql(table_name, engine, if_exists='append', index=False)
                self.logger.info(f"成功导出 {len(data['anomalies'])} 条异常记录到数据库表 {table_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"数据库导出失败: {e}")
            return False
    
    def export_to_mongodb(self, data, mongo_config):
        """导出到MongoDB"""
        if not HAS_PYMONGO:
            self.logger.error("pymongo 未安装，无法导出到MongoDB")
            return False
        
        try:
            # 连接MongoDB
            host = mongo_config.get('host', 'localhost')
            port = mongo_config.get('port', 27017)
            database = mongo_config.get('database', 'logs')
            username = mongo_config.get('username')
            password = mongo_config.get('password')
            
            if username and password:
                client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/")
            else:
                client = pymongo.MongoClient(host, port)
            
            db = client[database]
            
            # 导出日志数据
            if not data['logs'].empty:
                collection_name = mongo_config.get('logs_collection', 'log_entries')
                logs_collection = db[collection_name]
                
                # 转换DataFrame为字典列表
                logs_dict = data['logs'].to_dict('records')
                for log in logs_dict:
                    log['created_at'] = datetime.now()
                
                logs_collection.insert_many(logs_dict)
                self.logger.info(f"成功导出 {len(logs_dict)} 条日志记录到MongoDB集合 {collection_name}")
            
            # 导出异常数据
            if data['anomalies']:
                collection_name = mongo_config.get('anomalies_collection', 'log_anomalies')
                anomalies_collection = db[collection_name]
                
                for anomaly in data['anomalies']:
                    anomaly['created_at'] = datetime.now()
                
                anomalies_collection.insert_many(data['anomalies'])
                self.logger.info(f"成功导出 {len(data['anomalies'])} 条异常记录到MongoDB集合 {collection_name}")
            
            client.close()
            return True
            
        except Exception as e:
            self.logger.error(f"MongoDB导出失败: {e}")
            return False
    
    def export_to_elasticsearch(self, data, es_config):
        """导出到Elasticsearch"""
        if not HAS_ELASTICSEARCH:
            self.logger.error("elasticsearch 未安装，无法导出到Elasticsearch")
            return False
        
        try:
            # 连接Elasticsearch
            host = es_config.get('host', 'localhost')
            port = es_config.get('port', 9200)
            
            es = Elasticsearch([f"{host}:{port}"])
            
            # 导出日志数据
            if not data['logs'].empty:
                index_name = es_config.get('logs_index', 'log-entries')
                
                for _, log in data['logs'].iterrows():
                    doc = log.to_dict()
                    doc['@timestamp'] = datetime.now().isoformat()
                    
                    es.index(index=index_name, body=doc)
                
                self.logger.info(f"成功导出 {len(data['logs'])} 条日志记录到Elasticsearch索引 {index_name}")
            
            # 导出异常数据
            if data['anomalies']:
                index_name = es_config.get('anomalies_index', 'log-anomalies')
                
                for anomaly in data['anomalies']:
                    anomaly['@timestamp'] = datetime.now().isoformat()
                    es.index(index=index_name, body=anomaly)
                
                self.logger.info(f"成功导出 {len(data['anomalies'])} 条异常记录到Elasticsearch索引 {index_name}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"Elasticsearch导出失败: {e}")
            return False
    
    def export_to_redis(self, data, redis_config):
        """导出到Redis"""
        if not HAS_REDIS:
            self.logger.error("redis 未安装，无法导出到Redis")
            return False
        
        try:
            # 连接Redis
            host = redis_config.get('host', 'localhost')
            port = redis_config.get('port', 6379)
            db = redis_config.get('db', 0)
            password = redis_config.get('password')
            
            r = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)
            
            # 导出统计数据到Redis
            stats_key = redis_config.get('stats_key', 'log_stats')
            r.hset(stats_key, mapping=data['stats'])
            
            # 导出异常计数
            if data['anomalies']:
                anomaly_key = redis_config.get('anomaly_key', 'log_anomalies_count')
                r.set(anomaly_key, len(data['anomalies']))
                
                # 按类型统计异常
                anomaly_types = {}
                for anomaly in data['anomalies']:
                    anomaly_type = anomaly.get('type', 'unknown')
                    anomaly_types[anomaly_type] = anomaly_types.get(anomaly_type, 0) + 1
                
                for anomaly_type, count in anomaly_types.items():
                    r.hset(f"{anomaly_key}_by_type", anomaly_type, count)
            
            self.logger.info("成功导出统计数据到Redis")
            return True
            
        except Exception as e:
            self.logger.error(f"Redis导出失败: {e}")
            return False
    
    def send_email_alert(self, data, email_config):
        """发送邮件告警"""
        try:
            # 检查是否有需要告警的异常
            high_priority_anomalies = [
                a for a in data['anomalies'] 
                if a.get('type') in ['high_error_rate', 'unusual_traffic']
            ]
            
            if not high_priority_anomalies:
                self.logger.info("没有需要告警的异常")
                return True
            
            # 构建邮件内容
            subject = f"日志异常告警 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            body = f"""
日志分析系统检测到以下异常：

总记录数: {data['stats'].get('total_records', 'N/A')}
异常数量: {len(data['anomalies'])}
高优先级异常: {len(high_priority_anomalies)}

异常详情:
"""
            
            for anomaly in high_priority_anomalies:
                body += f"- {anomaly.get('description', 'Unknown anomaly')}\n"
            
            body += f"\n报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # 发送邮件
            msg = MimeMultipart()
            msg['From'] = email_config['from']
            msg['To'] = ', '.join(email_config['to'])
            msg['Subject'] = subject
            
            msg.attach(MimeText(body, 'plain', 'utf-8'))
            
            # SMTP发送
            server = smtplib.SMTP(email_config['smtp_host'], email_config['smtp_port'])
            if email_config.get('use_tls', True):
                server.starttls()
            
            if email_config.get('username') and email_config.get('password'):
                server.login(email_config['username'], email_config['password'])
            
            server.send_message(msg)
            server.quit()
            
            self.logger.info(f"告警邮件已发送到: {', '.join(email_config['to'])}")
            return True
            
        except Exception as e:
            self.logger.error(f"邮件发送失败: {e}")
            return False
    
    def export_to_file(self, data, file_config):
        """导出到文件"""
        try:
            output_dir = Path(file_config.get('output_dir', './exports'))
            output_dir.mkdir(parents=True, exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            
            # 导出日志数据
            if not data['logs'].empty:
                if file_config.get('format', 'csv').lower() == 'csv':
                    filename = output_dir / f"logs_{timestamp}.csv"
                    data['logs'].to_csv(filename, index=False)
                elif file_config.get('format', 'csv').lower() == 'json':
                    filename = output_dir / f"logs_{timestamp}.json"
                    data['logs'].to_json(filename, orient='records', indent=2)
                
                self.logger.info(f"日志数据已导出到: {filename}")
            
            # 导出异常数据
            if data['anomalies']:
                filename = output_dir / f"anomalies_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data['anomalies'], f, indent=2, ensure_ascii=False)
                
                self.logger.info(f"异常数据已导出到: {filename}")
            
            # 导出统计数据
            if data['stats']:
                filename = output_dir / f"stats_{timestamp}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data['stats'], f, indent=2, ensure_ascii=False, default=str)
                
                self.logger.info(f"统计数据已导出到: {filename}")
            
            return True
            
        except Exception as e:
            self.logger.error(f"文件导出失败: {e}")
            return False
    
    def run_export(self, data_dir):
        """运行导出任务"""
        self.logger.info("开始日志导出任务")
        
        # 加载数据
        data = self.load_processed_data(data_dir)
        
        if data['logs'].empty and not data['anomalies']:
            self.logger.warning("没有可导出的数据")
            return
        
        # 执行各种导出任务
        export_configs = self.config.get('exports', {})
        
        # 数据库导出
        if 'database' in export_configs:
            self.export_to_database(data, export_configs['database'])
        
        # MongoDB导出
        if 'mongodb' in export_configs:
            self.export_to_mongodb(data, export_configs['mongodb'])
        
        # Elasticsearch导出
        if 'elasticsearch' in export_configs:
            self.export_to_elasticsearch(data, export_configs['elasticsearch'])
        
        # Redis导出
        if 'redis' in export_configs:
            self.export_to_redis(data, export_configs['redis'])
        
        # 文件导出
        if 'file' in export_configs:
            self.export_to_file(data, export_configs['file'])
        
        # 邮件告警
        if 'email' in export_configs and data['anomalies']:
            self.send_email_alert(data, export_configs['email'])
        
        self.logger.info("日志导出任务完成")

def main():
    parser = argparse.ArgumentParser(description='日志导出工具')
    parser.add_argument('--config', required=True, help='配置文件路径')
    parser.add_argument('--data', required=True, help='处理后的数据目录')
    args = parser.parse_args()
    
    exporter = LogExporter(args.config)
    exporter.run_export(args.data)

if __name__ == '__main__':
    main()