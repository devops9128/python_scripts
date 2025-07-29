#!/usr/bin/env python3
"""
网站连接测试脚本
测试指定网站的连接状态、响应时间和基本信息
不使用面向对象，采用简单的函数式编程
"""

import requests
import time
import socket
import ssl
from urllib.parse import urlparse
from datetime import datetime

def test_basic_connection(url):
    """测试基本HTTP连接"""
    print(f"🔗 测试基本连接: {url}")
    print("-" * 50)
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 发送GET请求
        response = requests.get(url, timeout=10)
        
        # 计算响应时间
        response_time = (time.time() - start_time) * 1000  # 转换为毫秒
        
        # 打印基本信息
        print(f"✅ 连接成功!")
        print(f"📊 状态码: {response.status_code}")
        print(f"⏱️  响应时间: {response_time:.2f} ms")
        print(f"📏 响应大小: {len(response.content)} bytes")
        print(f"🌐 最终URL: {response.url}")
        
        # 检查状态码
        if response.status_code == 200:
            print("✅ 网站正常运行")
        elif 300 <= response.status_code < 400:
            print("🔄 网站重定向")
        elif 400 <= response.status_code < 500:
            print("❌ 客户端错误")
        elif 500 <= response.status_code < 600:
            print("🚨 服务器错误")
        
        return True, response
        
    except requests.exceptions.Timeout:
        print("⏰ 连接超时")
        return False, None
    except requests.exceptions.ConnectionError:
        print("❌ 连接失败")
        return False, None
    except requests.exceptions.RequestException as e:
        print(f"❌ 请求异常: {e}")
        return False, None

def test_response_headers(response):
    """分析响应头信息"""
    if not response:
        return
    
    print(f"\n📋 响应头信息:")
    print("-" * 50)
    
    # 重要的响应头
    important_headers = [
        'Server',
        'Content-Type',
        'Content-Length',
        'Date',
        'Last-Modified',
        'Cache-Control',
        'Set-Cookie'
    ]
    
    for header in important_headers:
        if header in response.headers:
            print(f"{header}: {response.headers[header]}")
    
    # 安全相关头
    security_headers = [
        'X-Frame-Options',
        'X-Content-Type-Options',
        'X-XSS-Protection',
        'Strict-Transport-Security'
    ]
    
    print(f"\n🔒 安全头检查:")
    for header in security_headers:
        if header in response.headers:
            print(f"✅ {header}: {response.headers[header]}")
        else:
            print(f"❌ {header}: 未设置")

def test_ssl_certificate(url):
    """测试SSL证书信息"""
    parsed_url = urlparse(url)
    
    if parsed_url.scheme != 'https':
        print(f"\n🔓 该网站不使用HTTPS")
        return
    
    print(f"\n🔐 SSL证书信息:")
    print("-" * 50)
    
    try:
        hostname = parsed_url.hostname
        port = parsed_url.port or 443
        
        # 获取SSL证书信息
        context = ssl.create_default_context()
        with socket.create_connection((hostname, port), timeout=10) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                
                print(f"📜 证书主题: {cert.get('subject', 'N/A')}")
                print(f"🏢 证书颁发者: {cert.get('issuer', 'N/A')}")
                print(f"📅 有效期从: {cert.get('notBefore', 'N/A')}")
                print(f"📅 有效期到: {cert.get('notAfter', 'N/A')}")
                print(f"🔢 序列号: {cert.get('serialNumber', 'N/A')}")
                print(f"📝 版本: {cert.get('version', 'N/A')}")
                
    except Exception as e:
        print(f"❌ SSL证书检查失败: {e}")

def test_dns_resolution(url):
    """测试DNS解析"""
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname
    
    print(f"\n🌐 DNS解析测试:")
    print("-" * 50)
    
    try:
        # 解析IP地址
        ip_addresses = socket.gethostbyname_ex(hostname)
        
        print(f"🏠 主机名: {ip_addresses[0]}")
        print(f"🔗 别名: {ip_addresses[1] if ip_addresses[1] else '无'}")
        print(f"📍 IP地址: {', '.join(ip_addresses[2])}")
        
    except socket.gaierror as e:
        print(f"❌ DNS解析失败: {e}")

def test_response_content(response):
    """分析响应内容"""
    if not response:
        return
    
    print(f"\n📄 响应内容分析:")
    print("-" * 50)
    
    content = response.text
    
    # 基本统计
    print(f"📏 内容长度: {len(content)} 字符")
    print(f"📝 内容类型: {response.headers.get('Content-Type', '未知')}")
    
    # 检查是否包含常见元素
    checks = [
        ('<html', 'HTML文档'),
        ('<head', 'HTML头部'),
        ('<body', 'HTML主体'),
        ('<title', '页面标题'),
        ('javascript', 'JavaScript代码'),
        ('css', 'CSS样式'),
        ('error', '错误信息'),
        ('404', '404错误'),
        ('500', '500错误')
    ]
    
    print(f"\n🔍 内容检查:")
    for check, description in checks:
        if check.lower() in content.lower():
            print(f"✅ 包含 {description}")
        else:
            print(f"❌ 不包含 {description}")
    
    # 显示前200个字符
    print(f"\n📖 内容预览 (前200字符):")
    print("-" * 30)
    print(content[:200] + "..." if len(content) > 200 else content)

def test_multiple_requests(url, count=5):
    """测试多次请求的稳定性"""
    print(f"\n🔄 稳定性测试 (发送{count}次请求):")
    print("-" * 50)
    
    response_times = []
    success_count = 0
    
    for i in range(count):
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                success_count += 1
                response_times.append(response_time)
                print(f"请求 {i+1}: ✅ {response_time:.2f}ms")
            else:
                print(f"请求 {i+1}: ❌ 状态码 {response.status_code}")
                
        except Exception as e:
            print(f"请求 {i+1}: ❌ 失败 - {e}")
        
        # 请求间隔
        if i < count - 1:
            time.sleep(1)
    
    # 统计结果
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        
        print(f"\n📊 统计结果:")
        print(f"成功率: {success_count}/{count} ({success_count/count*100:.1f}%)")
        print(f"平均响应时间: {avg_time:.2f}ms")
        print(f"最快响应时间: {min_time:.2f}ms")
        print(f"最慢响应时间: {max_time:.2f}ms")

def main():
    """主函数"""
    # 要测试的网站
    test_url = "https://production-kul.unitedcaps.com/"
    
    print("🚀 网站连接测试工具")
    print("=" * 60)
    print(f"🎯 目标网站: {test_url}")
    print(f"🕐 测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # 1. 基本连接测试
    success, response = test_basic_connection(test_url)
    
    # 2. DNS解析测试
    test_dns_resolution(test_url)
    
    # 3. SSL证书测试
    test_ssl_certificate(test_url)
    
    if success and response:
        # 4. 响应头分析
        test_response_headers(response)
        
        # 5. 响应内容分析
        test_response_content(response)
    
    # 6. 稳定性测试
    test_multiple_requests(test_url, 3)
    
    print("\n" + "=" * 60)
    print("✅ 测试完成!")
    print("=" * 60)

if __name__ == "__main__":
    main()