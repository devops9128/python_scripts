# Python 日志处理脚本集合

## 脚本说明

这个目录包含了完整的 Python 日志处理解决方案：

### 1. 日志拉取 (log_collector.py)
- 从远程服务器拉取日志文件
- 支持 SSH、FTP、HTTP 等多种协议
- 支持增量拉取和全量拉取

### 2. 日志分析 (log_analyzer.py)
- 解析各种格式的日志文件
- 提取关键信息和统计数据
- 支持正则表达式和结构化解析

### 3. 日志处理 (log_processor.py)
- 日志清洗和格式化
- 数据转换和标准化
- 异常检测和过滤

### 4. 日志报告 (log_reporter.py)
- 生成统计报告
- 创建图表和可视化
- 支持多种输出格式

### 5. 日志输出 (log_exporter.py)
- 导出到数据库
- 发送到监控系统
- 生成告警通知

## 依赖安装

```bash
pip install -r requirements.txt
```

## 配置文件

所有脚本都使用 `config.yaml` 作为配置文件，请根据实际环境进行修改。

## 使用示例

```bash
# 拉取日志
python log_collector.py --config config.yaml

# 分析日志
python log_analyzer.py --input logs/ --output analysis/

# 生成报告
python log_reporter.py --analysis analysis/ --report reports/
```