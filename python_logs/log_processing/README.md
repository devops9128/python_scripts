# 日志处理脚本

本目录包含所有与日志收集、处理、分析和报告相关的脚本。

## 📋 脚本列表

### 🔄 核心处理
- **run_pipeline.py** ⭐ - 主要的管道运行脚本
- **log_processor.py** - 日志处理核心模块
- **log_collector.py** - 日志收集器

### 📊 分析和报告
- **log_analyzer.py** - 日志分析器
- **log_reporter.py** - 日志报告生成器
- **log_exporter.py** - 日志导出工具

## 🚀 快速开始

### 运行完整管道
```bash
python run_pipeline.py
```

### 单独使用组件
```bash
# 收集日志
python log_collector.py

# 分析日志
python log_analyzer.py

# 生成报告
python log_reporter.py

# 导出数据
python log_exporter.py
```

## 🔧 配置文件

使用根目录的配置文件：
- **../config.yaml** - 主配置文件
- **../export_config.json** - 导出配置

## 📁 输出目录

处理后的文件通常保存在：
- 分析结果
- 报告文件
- 导出数据

## 🔄 工作流程

1. **收集** → `log_collector.py`
2. **处理** → `log_processor.py`
3. **分析** → `log_analyzer.py`
4. **报告** → `log_reporter.py`
5. **导出** → `log_exporter.py`

## 📞 支持

遇到问题请查看 `../documentation/` 目录下的相关文档。