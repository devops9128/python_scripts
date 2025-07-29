# 测试工具

本目录包含所有测试、诊断和验证相关的脚本。

## 📋 脚本列表

### 🔍 诊断工具
- **python_diagnostic.py** ⭐ - Python环境诊断工具

### 🧪 监控测试
- **test_ping_monitor.py** - ping监控功能测试
- **test_timeout_file.py** - 超时文件生成测试
- **test_timeout_simulation.py** - 超时情况模拟测试

## 🚀 快速开始

### 环境诊断
```bash
python python_diagnostic.py
```

### 监控功能测试
```bash
# 测试ping监控
python test_ping_monitor.py

# 测试文件写入
python test_timeout_file.py

# 模拟超时情况
python test_timeout_simulation.py
```

## 🎯 使用场景

### 🔍 环境检查
使用 `python_diagnostic.py` 来：
- 检查Python版本和路径
- 验证模块安装情况
- 测试网络连接
- 诊断常见问题

### 🧪 功能验证
使用测试脚本来：
- 验证监控脚本功能
- 测试文件写入权限
- 模拟各种网络情况
- 确保脚本正常工作

## 📊 测试类型

| 脚本 | 测试内容 | 超时设置 | 输出文件 | 用途 |
|------|----------|----------|----------|------|
| test_ping_monitor.py | 基础监控 | 2秒 | timeout.txt | 快速验证 |
| test_timeout_file.py | 文件写入 | 2秒 | timeout.txt | 权限测试 |
| test_timeout_simulation.py | 超时模拟 | 5秒 | timeout.txt | 超时测试 |
| python_diagnostic.py | 环境诊断 | - | 控制台 | 环境检查 |

## 🔧 故障排除

如果测试失败：
1. 运行 `python_diagnostic.py` 检查环境
2. 查看 `../documentation/TROUBLESHOOTING.md`
3. 检查网络连接和文件权限

## 📞 支持

遇到问题请查看 `../documentation/` 目录下的相关文档。