# Python环境诊断脚本
# 帮助诊断Python环境和模块安装问题

import sys
import os

def check_python_info():
    """检查Python基本信息"""
    print("🐍 Python环境信息:")
    print("=" * 50)
    print(f"Python版本: {sys.version}")
    print(f"Python路径: {sys.executable}")
    print(f"当前工作目录: {os.getcwd()}")
    print()

def check_modules():
    """检查模块安装情况"""
    print("📦 模块检查:")
    print("=" * 50)
    
    # 检查内置模块
    builtin_modules = ['urllib', 'time', 'datetime', 'socket', 'os', 'sys']
    print("内置模块:")
    for module in builtin_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} - 可用")
        except ImportError:
            print(f"  ❌ {module} - 不可用")
    
    print()
    
    # 检查第三方模块
    third_party_modules = ['requests']
    print("第三方模块:")
    for module in third_party_modules:
        try:
            __import__(module)
            print(f"  ✅ {module} - 已安装")
        except ImportError:
            print(f"  ❌ {module} - 未安装")
    
    print()

def test_basic_connection():
    """测试基本网络连接"""
    print("🌐 网络连接测试:")
    print("=" * 50)
    
    # 使用内置模块测试
    try:
        import urllib.request
        import socket
        
        url = "https://production-kul.unitedcaps.com/"
        print(f"测试连接: {url}")
        
        request = urllib.request.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')
        
        with urllib.request.urlopen(request, timeout=10) as response:
            status = response.getcode()
            print(f"✅ 连接成功 - 状态码: {status}")
            
    except Exception as e:
        print(f"❌ 连接失败: {e}")
    
    print()

def provide_solutions():
    """提供解决方案"""
    print("🔧 解决方案:")
    print("=" * 50)
    print("如果遇到 'ModuleNotFoundError: No module named requests':")
    print("1. 安装requests模块:")
    print("   pip install requests")
    print()
    print("2. 如果pip不工作，尝试:")
    print("   python -m pip install requests")
    print()
    print("3. 使用无依赖版本:")
    print("   运行 no_dependency_ping_monitor.py")
    print()
    print("4. 检查Python环境:")
    print("   确保使用正确的Python解释器")
    print("   python --version")
    print()

def main():
    print("🔍 Python环境诊断工具")
    print("=" * 60)
    
    check_python_info()
    check_modules()
    test_basic_connection()
    provide_solutions()
    
    print("诊断完成!")

if __name__ == "__main__":
    main()