#!/usr/bin/env python3
"""
完整的日志处理流水线示例
演示如何使用所有日志处理脚本
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from datetime import datetime

def setup_logging():
    """设置日志记录"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('pipeline.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

def run_command(command, description):
    """运行命令并记录结果"""
    logger = logging.getLogger(__name__)
    logger.info(f"开始执行: {description}")
    logger.info(f"命令: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"成功完成: {description}")
            if result.stdout:
                logger.info(f"输出: {result.stdout}")
        else:
            logger.error(f"执行失败: {description}")
            logger.error(f"错误: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"执行异常: {description} - {e}")
        return False
    
    return True

def main():
    """主函数 - 运行完整的日志处理流水线"""
    logger = setup_logging()
    logger.info("开始日志处理流水线")
    
    # 创建工作目录
    work_dir = Path('./log_pipeline_work')
    work_dir.mkdir(exist_ok=True)
    
    # 定义各个阶段的目录
    raw_logs_dir = work_dir / 'raw_logs'
    analysis_dir = work_dir / 'analysis'
    processed_dir = work_dir / 'processed'
    reports_dir = work_dir / 'reports'
    exports_dir = work_dir / 'exports'
    
    # 创建目录
    for directory in [raw_logs_dir, analysis_dir, processed_dir, reports_dir, exports_dir]:
        directory.mkdir(exist_ok=True)
    
    # 步骤1: 日志收集
    logger.info("=" * 50)
    logger.info("步骤1: 日志收集")
    logger.info("=" * 50)
    
    collect_cmd = f"python log_collector.py --config config.yaml"
    if not run_command(collect_cmd, "日志收集"):
        logger.error("日志收集失败，终止流水线")
        return False
    
    # 步骤2: 日志分析
    logger.info("=" * 50)
    logger.info("步骤2: 日志分析")
    logger.info("=" * 50)
    
    analyze_cmd = f"python log_analyzer.py --input {raw_logs_dir} --output {analysis_dir}"
    if not run_command(analyze_cmd, "日志分析"):
        logger.error("日志分析失败，终止流水线")
        return False
    
    # 步骤3: 日志处理
    logger.info("=" * 50)
    logger.info("步骤3: 日志处理")
    logger.info("=" * 50)
    
    process_cmd = f"python log_processor.py --input {analysis_dir} --output {processed_dir}"
    if not run_command(process_cmd, "日志处理"):
        logger.error("日志处理失败，终止流水线")
        return False
    
    # 步骤4: 生成报告
    logger.info("=" * 50)
    logger.info("步骤4: 生成报告")
    logger.info("=" * 50)
    
    report_cmd = f"python log_reporter.py --analysis {processed_dir} --report {reports_dir}"
    if not run_command(report_cmd, "报告生成"):
        logger.error("报告生成失败，终止流水线")
        return False
    
    # 步骤5: 数据导出
    logger.info("=" * 50)
    logger.info("步骤5: 数据导出")
    logger.info("=" * 50)
    
    export_cmd = f"python log_exporter.py --config export_config.json --data {processed_dir}"
    if not run_command(export_cmd, "数据导出"):
        logger.warning("数据导出失败，但不影响流水线完成")
    
    # 完成
    logger.info("=" * 50)
    logger.info("日志处理流水线完成!")
    logger.info("=" * 50)
    
    # 输出结果位置
    logger.info("结果文件位置:")
    logger.info(f"- 原始日志: {raw_logs_dir}")
    logger.info(f"- 分析结果: {analysis_dir}")
    logger.info(f"- 处理结果: {processed_dir}")
    logger.info(f"- 报告文件: {reports_dir}")
    logger.info(f"- 导出文件: {exports_dir}")
    
    # 检查关键文件
    key_files = [
        reports_dir / 'log_analysis_report.html',
        processed_dir / 'processed_logs.csv',
        processed_dir / 'anomalies.json'
    ]
    
    logger.info("\n关键输出文件:")
    for file_path in key_files:
        if file_path.exists():
            logger.info(f"✓ {file_path}")
        else:
            logger.warning(f"✗ {file_path} (未找到)")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)