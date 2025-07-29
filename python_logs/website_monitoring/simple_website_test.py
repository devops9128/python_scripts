#!/usr/bin/env python3
"""
简单的网站连接测试脚本
专门测试 https://production-kul.unitedcaps.com/ 是否有响应
使用简单的函数，不涉及面向对象概念
"""

import requests
import time

def test_website_connection():
    """测试网站连接的简单函数"""
    
    # 要测试的网站URL
    url = "https://production-kul.unitedcaps.com/"
    
    print("开始测试网站连接...")
    print(f"目标网站: {url}")
    print("-" * 40)
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 发送HTTP GET请求
        response = requests.get(url, timeout=10)
        
        # 计算响应时间
        response_time = time.time() - start_time
        
        # 打印结果
        print("✅ 连接成功!")
        print(f"状态码: {response.status_code}")
        print(f"响应时间: {response_time:.2f} 秒")
        print(f"响应大小: {len(response.content)} 字节")
        
        # 判断网站状态
        if response.status_code == 200:
            print("🎉 网站正常运行，有响应终端!")
            return True
        else:
            print(f"⚠️ 网站有响应，但状态异常: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ 连接超时，网站可能无响应")
        return False
        
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败，网站可能不存在或无法访问")
        return False
        
    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return False

def check_website_details():
    """检查网站的详细信息"""
    
    url = "https://production-kul.unitedcaps.com/"
    
    try:
        response = requests.get(url, timeout=10)
        
        print("\n网站详细信息:")
        print("-" * 40)
        
        # 服务器信息
        server = response.headers.get('Server', '未知')
        print(f"服务器类型: {server}")
        
        # 内容类型
        content_type = response.headers.get('Content-Type', '未知')
        print(f"内容类型: {content_type}")
        
        # 最后修改时间
        last_modified = response.headers.get('Last-Modified', '未知')
        print(f"最后修改: {last_modified}")
        
        # 检查是否是网页
        if 'text/html' in content_type:
            print("✅ 这是一个网页")
        else:
            print("ℹ️ 这不是标准网页")
            
        return True
        
    except Exception as e:
        print(f"获取详细信息失败: {e}")
        return False

def main():
    """主程序"""
    print("🌐 网站连接测试工具")
    print("=" * 50)
    
    # 测试基本连接
    if test_website_connection():
        # 如果连接成功，获取更多信息
        check_website_details()
    
    print("\n测试完成!")

# 运行程序
if __name__ == "__main__":
    main()