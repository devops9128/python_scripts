# 解决 "ModuleNotFoundError: No module named 'requests'" 问题

## 问题描述
运行 `simple_ping_monitor.py` 时出现错误：
```
ModuleNotFoundError: No module named 'requests'
```

## 解决方案

### 方案1: 安装requests模块 (推荐)
```bash
pip install requests
```

如果上述命令不工作，尝试：
```bash
python -m pip install requests
```

### 方案2: 使用无依赖版本 (备选)
如果无法安装requests，可以使用无依赖版本：
```bash
python no_dependency_ping_monitor.py
```

这个版本只使用Python内置模块，无需安装任何额外依赖。

### 方案3: 检查Python环境
运行诊断脚本检查环境：
```bash
python python_diagnostic.py
```

## 可用的脚本文件

### 1. simple_ping_monitor.py (需要requests)
- 功能最完整
- 需要安装requests模块
- 推荐在正常环境下使用

### 2. no_dependency_ping_monitor.py (无依赖)
- 使用Python内置模块
- 无需安装额外依赖
- 功能与requests版本相同
- 适合无法安装第三方模块的环境

### 3. python_diagnostic.py (诊断工具)
- 检查Python环境
- 测试模块安装情况
- 提供解决方案建议

## 使用建议

1. **首先尝试安装requests**:
   ```bash
   pip install requests
   python simple_ping_monitor.py
   ```

2. **如果安装失败，使用无依赖版本**:
   ```bash
   python no_dependency_ping_monitor.py
   ```

3. **如果仍有问题，运行诊断**:
   ```bash
   python python_diagnostic.py
   ```

## 功能对比

| 功能 | simple_ping_monitor.py | no_dependency_ping_monitor.py |
|------|------------------------|-------------------------------|
| 持续ping监控 | ✅ | ✅ |
| 60秒超时检测 | ✅ | ✅ |
| 记录到timeout.txt | ✅ | ✅ |
| 实时统计 | ✅ | ✅ |
| 外部依赖 | requests | 无 |
| HTTP状态码 | ✅ | ✅ |
| 错误处理 | ✅ | ✅ |

两个版本功能完全相同，只是使用的HTTP库不同。

## 常见问题

### Q: 为什么会出现ModuleNotFoundError?
A: 因为requests不是Python的内置模块，需要单独安装。

### Q: 无依赖版本和requests版本有什么区别?
A: 功能完全相同，只是使用不同的HTTP库。无依赖版本使用urllib（内置），requests版本使用requests库（第三方）。

### Q: 哪个版本更好?
A: 如果可以安装requests，推荐使用simple_ping_monitor.py，因为requests库更稳定。如果无法安装，no_dependency_ping_monitor.py是完美的替代方案。

### Q: 如何确认脚本正常工作?
A: 运行后应该看到类似输出：
```
🚀 开始持续ping监控
🎯 目标网站: https://production-kul.unitedcaps.com/
⏰ 超时阈值: 60秒 (1分钟)
📝 超时日志: timeout.txt
🛑 按 Ctrl+C 停止监控
============================================================

[1] 2025-07-29 09:30:10 - 正在ping...
✅ 成功 - 0.85秒 - 状态码: 200
📊 统计: 总计1次, 成功1次, 超时0次, 成功率100.0%
⏳ 等待5秒后继续...
```