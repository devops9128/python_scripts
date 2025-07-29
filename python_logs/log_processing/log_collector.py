#!/usr/bin/env python3
"""
日志拉取脚本
支持从远程服务器通过 SSH、FTP、HTTP 等方式拉取日志文件
"""

import os
import sys
import logging
import argparse
import yaml
import paramiko
import requests
from datetime import datetime, timedelta
from pathlib import Path
import ftplib
import gzip
import shutil

class LogCollector:
    def __init__(self, config_file):
        """初始化日志收集器"""
        self.config = self.load_config(config_file)
        self.setup_logging()
        
    def load_config(self, config_file):
        """加载配置文件"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            sys.exit(1)
    
    def setup_logging(self):
        """设置日志记录"""
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        log_file = self.config.get('logging', {}).get('file', 'collector.log')
        
        logging.basicConfig(
            level=getattr(logging, log_level),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def collect_ssh_logs(self, server_config):
        """通过 SSH 拉取日志"""
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            
            # 连接服务器
            ssh.connect(
                hostname=server_config['host'],
                port=server_config.get('port', 22),
                username=server_config['username'],
                password=server_config.get('password'),
                key_filename=server_config.get('key_file')
            )
            
            sftp = ssh.open_sftp()
            
            # 创建本地目录
            local_dir = Path(server_config['local_path'])
            local_dir.mkdir(parents=True, exist_ok=True)
            
            # 拉取日志文件
            for log_path in server_config['log_paths']:
                try:
                    # 获取远程文件列表
                    stdin, stdout, stderr = ssh.exec_command(f"find {log_path} -name '*.log' -type f")
                    remote_files = stdout.read().decode().strip().split('\n')
                    
                    for remote_file in remote_files:
                        if remote_file:
                            local_file = local_dir / Path(remote_file).name
                            self.logger.info(f"拉取文件: {remote_file} -> {local_file}")
                            sftp.get(remote_file, str(local_file))
                            
                except Exception as e:
                    self.logger.error(f"拉取日志路径 {log_path} 失败: {e}")
            
            sftp.close()
            ssh.close()
            self.logger.info(f"SSH 日志拉取完成: {server_config['host']}")
            
        except Exception as e:
            self.logger.error(f"SSH 连接失败 {server_config['host']}: {e}")
    
    def collect_http_logs(self, server_config):
        """通过 HTTP 拉取日志"""
        try:
            local_dir = Path(server_config['local_path'])
            local_dir.mkdir(parents=True, exist_ok=True)
            
            for url in server_config['log_urls']:
                try:
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()
                    
                    filename = Path(url).name or f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
                    local_file = local_dir / filename
                    
                    with open(local_file, 'wb') as f:
                        f.write(response.content)
                    
                    self.logger.info(f"HTTP 日志拉取完成: {url} -> {local_file}")
                    
                except Exception as e:
                    self.logger.error(f"HTTP 拉取失败 {url}: {e}")
                    
        except Exception as e:
            self.logger.error(f"HTTP 日志拉取失败: {e}")
    
    def collect_ftp_logs(self, server_config):
        """通过 FTP 拉取日志"""
        try:
            ftp = ftplib.FTP()
            ftp.connect(server_config['host'], server_config.get('port', 21))
            ftp.login(server_config['username'], server_config.get('password', ''))
            
            local_dir = Path(server_config['local_path'])
            local_dir.mkdir(parents=True, exist_ok=True)
            
            for remote_path in server_config['log_paths']:
                try:
                    ftp.cwd(remote_path)
                    files = ftp.nlst()
                    
                    for filename in files:
                        if filename.endswith('.log'):
                            local_file = local_dir / filename
                            with open(local_file, 'wb') as f:
                                ftp.retrbinary(f'RETR {filename}', f.write)
                            self.logger.info(f"FTP 日志拉取完成: {filename}")
                            
                except Exception as e:
                    self.logger.error(f"FTP 拉取路径 {remote_path} 失败: {e}")
            
            ftp.quit()
            
        except Exception as e:
            self.logger.error(f"FTP 连接失败: {e}")
    
    def compress_logs(self, directory):
        """压缩日志文件"""
        log_dir = Path(directory)
        for log_file in log_dir.glob('*.log'):
            try:
                compressed_file = log_file.with_suffix('.log.gz')
                with open(log_file, 'rb') as f_in:
                    with gzip.open(compressed_file, 'wb') as f_out:
                        shutil.copyfileobj(f_in, f_out)
                
                log_file.unlink()  # 删除原文件
                self.logger.info(f"压缩完成: {compressed_file}")
                
            except Exception as e:
                self.logger.error(f"压缩失败 {log_file}: {e}")
    
    def run(self):
        """运行日志收集"""
        self.logger.info("开始日志收集任务")
        
        for server in self.config.get('servers', []):
            protocol = server.get('protocol', 'ssh').lower()
            
            if protocol == 'ssh':
                self.collect_ssh_logs(server)
            elif protocol == 'http':
                self.collect_http_logs(server)
            elif protocol == 'ftp':
                self.collect_ftp_logs(server)
            else:
                self.logger.warning(f"不支持的协议: {protocol}")
        
        # 压缩日志文件
        if self.config.get('compress_logs', False):
            for server in self.config.get('servers', []):
                self.compress_logs(server['local_path'])
        
        self.logger.info("日志收集任务完成")

def main():
    parser = argparse.ArgumentParser(description='日志拉取工具')
    parser.add_argument('--config', default='config.yaml', help='配置文件路径')
    args = parser.parse_args()
    
    collector = LogCollector(args.config)
    collector.run()

if __name__ == '__main__':
    main()