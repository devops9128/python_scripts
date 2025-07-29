# Python脚本目录结构说明

## 📁 目录分类

本目录已按功能重新组织，将相同类型的脚本归类到对应的子目录中。

### 🌐 website_monitoring/ - 网站监控脚本
包含所有与网站连接测试和监控相关的脚本：

- **beginner_website_test.py** - 初学者版本的网站测试脚本
- **simple_website_test.py** - 简单的网站测试脚本
- **learning_website_test.py** - 学习版本的网站测试脚本
- **website_connection_test.py** - 网站连接测试脚本
- **continuous_ping_monitor.py** - 持续ping监控脚本（详细版）
- **simple_ping_monitor.py** - 简单ping监控脚本（需要requests库）
- **no_dependency_ping_monitor.py** - 无依赖ping监控脚本（推荐）
- **ping_monitor_fixed.py** - 修复版ping监控脚本（最新版本）

### 📊 log_processing/ - 日志处理脚本
包含所有与日志收集、处理、分析相关的脚本：

- **log_analyzer.py** - 日志分析器
- **log_collector.py** - 日志收集器
- **log_exporter.py** - 日志导出器
- **log_processor.py** - 日志处理器
- **log_reporter.py** - 日志报告器
- **run_pipeline.py** - 运行管道脚本

### 🧪 testing_tools/ - 测试工具
包含所有测试和诊断相关的脚本：

- **test_ping_monitor.py** - ping监控测试脚本
- **test_timeout_file.py** - 超时文件测试脚本
- **test_timeout_simulation.py** - 超时模拟测试脚本
- **python_diagnostic.py** - Python环境诊断脚本

### 📚 documentation/ - 文档
包含所有说明文档和故障排除指南：

- **ping_monitor_usage.md** - ping监控脚本使用说明
- **TROUBLESHOOTING.md** - 故障排除指南
- **TIMEOUT_FILE_FIX.md** - 超时文件修复说明

## 🚀 快速开始

### 网站监控
```bash
# 推荐使用（无依赖）
cd website_monitoring
python ping_monitor_fixed.py

# 或者使用
python no_dependency_ping_monitor.py
```

### 日志处理
```bash
cd log_processing
python run_pipeline.py
```

### 测试工具
```bash
cd testing_tools
python python_diagnostic.py
```

## 📋 文件保留在根目录

以下文件保留在根目录，因为它们是项目级别的配置：

- **README.md** - 项目主要说明文档
- **requirements.txt** - Python依赖包列表
- **config.yaml** - 配置文件
- **export_config.json** - 导出配置文件
- **timeout.txt** - 超时记录文件（由监控脚本生成）

## 🔄 使用建议

1. **网站监控**：优先使用 `website_monitoring/ping_monitor_fixed.py`
2. **日志处理**：从 `log_processing/run_pipeline.py` 开始
3. **测试诊断**：使用 `testing_tools/python_diagnostic.py` 检查环境
4. **查看文档**：参考 `documentation/` 目录下的相关文档

## 📞 支持

如有问题，请查看 `documentation/TROUBLESHOOTING.md` 文档。