# 网站监控脚本

本目录包含所有与网站连接测试和监控相关的脚本。

## 📋 脚本列表

### 🎯 生产环境推荐
- **ping_monitor_fixed.py** ⭐ - 最新修复版本，推荐生产使用
- **no_dependency_ping_monitor.py** - 无依赖版本，适合无法安装第三方库的环境

### 📚 学习和测试版本
- **beginner_website_test.py** - 初学者友好的简单网站测试
- **simple_website_test.py** - 基础网站连接测试
- **learning_website_test.py** - 带详细注释的学习版本
- **website_connection_test.py** - 网站连接状态检查

### 🔄 监控版本
- **continuous_ping_monitor.py** - 详细版本的持续监控
- **simple_ping_monitor.py** - 需要requests库的简单监控版本

## 🚀 快速开始

### 推荐使用（生产环境）
```bash
python ping_monitor_fixed.py
```

### 无依赖环境
```bash
python no_dependency_ping_monitor.py
```

### 学习测试
```bash
python beginner_website_test.py
```

## ⚙️ 功能对比

| 脚本 | 依赖 | 超时检测 | 文件记录 | 统计信息 | 推荐用途 |
|------|------|----------|----------|----------|----------|
| ping_monitor_fixed.py | 无 | ✅ | ✅ | ✅ | 生产环境 |
| no_dependency_ping_monitor.py | 无 | ✅ | ✅ | ✅ | 备选方案 |
| simple_ping_monitor.py | requests | ✅ | ✅ | ✅ | 有依赖环境 |
| continuous_ping_monitor.py | requests | ✅ | ✅ | ✅ | 详细监控 |
| beginner_website_test.py | requests | ❌ | ❌ | ❌ | 学习测试 |

## 📝 输出文件

所有监控脚本会在根目录生成：
- **timeout.txt** - 超时记录文件

## 🎯 目标网站

默认监控：`https://production-kul.unitedcaps.com/`

## 📞 支持

遇到问题请查看 `../documentation/` 目录下的相关文档。