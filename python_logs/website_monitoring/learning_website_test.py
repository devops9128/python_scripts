#!/usr/bin/env python3
"""
网站连接测试 - 学习版本
详细注释版本，帮助理解每一步的作用
测试网站: https://production-kul.unitedcaps.com/
"""

# 导入需要的库
import requests  # 用于发送HTTP请求
import time      # 用于计算时间

def simple_test():
    """最简单的测试函数 - 只检查网站是否能访问"""
    
    print("=== 最简单的测试 ===")
    
    # 定义要测试的网站地址
    url = "https://production-kul.unitedcaps.com/"
    
    try:
        # 发送GET请求到网站
        response = requests.get(url)
        
        # 检查状态码
        if response.status_code == 200:
            print("✅ 网站可以访问!")
            print(f"状态码: {response.status_code}")
        else:
            print(f"⚠️ 网站有问题，状态码: {response.status_code}")
            
    except Exception as e:
        print(f"❌ 访问失败: {e}")

def detailed_test():
    """详细测试函数 - 获取更多信息"""
    
    print("\n=== 详细测试 ===")
    
    url = "https://production-kul.unitedcaps.com/"
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 发送请求，设置10秒超时
        response = requests.get(url, timeout=10)
        
        # 计算响应时间
        end_time = time.time()
        response_time = end_time - start_time
        
        # 打印详细信息
        print(f"🌐 网站地址: {url}")
        print(f"📊 状态码: {response.status_code}")
        print(f"⏱️ 响应时间: {response_time:.2f} 秒")
        print(f"📦 数据大小: {len(response.content)} 字节")
        
        # 检查响应头中的服务器信息
        server_info = response.headers.get('Server', '未知')
        print(f"🖥️ 服务器: {server_info}")
        
        # 检查内容类型
        content_type = response.headers.get('Content-Type', '未知')
        print(f"📄 内容类型: {content_type}")
        
        return response
        
    except requests.exceptions.Timeout:
        print("❌ 连接超时 - 网站响应太慢")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误 - 无法连接到网站")
        return None
    except Exception as e:
        print(f"❌ 其他错误: {e}")
        return None

def check_content(response):
    """检查网站内容"""
    
    if not response:
        return
    
    print("\n=== 内容检查 ===")
    
    # 获取网页内容
    content = response.text
    
    # 检查内容长度
    print(f"📏 内容长度: {len(content)} 字符")
    
    # 检查是否包含常见的HTML标签
    html_tags = ['<html', '<head', '<body', '<title']
    
    print("🔍 HTML标签检查:")
    for tag in html_tags:
        if tag in content.lower():
            print(f"  ✅ 包含 {tag} 标签")
        else:
            print(f"  ❌ 不包含 {tag} 标签")
    
    # 显示网页开头的一部分内容
    print(f"\n📖 网页内容预览 (前100字符):")
    print("-" * 30)
    preview = content[:100].replace('\n', ' ').replace('\r', ' ')
    print(preview + "...")

def multiple_tests():
    """多次测试检查稳定性"""
    
    print("\n=== 稳定性测试 ===")
    
    url = "https://production-kul.unitedcaps.com/"
    test_count = 3  # 测试3次
    
    success_count = 0
    total_time = 0
    
    for i in range(test_count):
        print(f"\n第 {i+1} 次测试:")
        
        try:
            start_time = time.time()
            response = requests.get(url, timeout=10)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                success_count += 1
                total_time += response_time
                print(f"  ✅ 成功 - {response_time:.2f}秒")
            else:
                print(f"  ❌ 失败 - 状态码: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ 错误: {e}")
        
        # 等待1秒再进行下一次测试
        if i < test_count - 1:
            time.sleep(1)
    
    # 计算成功率和平均时间
    success_rate = (success_count / test_count) * 100
    avg_time = total_time / success_count if success_count > 0 else 0
    
    print(f"\n📊 测试结果:")
    print(f"  成功次数: {success_count}/{test_count}")
    print(f"  成功率: {success_rate:.1f}%")
    if avg_time > 0:
        print(f"  平均响应时间: {avg_time:.2f}秒")

def main():
    """主程序 - 运行所有测试"""
    
    print("🚀 网站连接测试程序")
    print("目标: https://production-kul.unitedcaps.com/")
    print("=" * 50)
    
    # 1. 简单测试
    simple_test()
    
    # 2. 详细测试
    response = detailed_test()
    
    # 3. 内容检查
    check_content(response)
    
    # 4. 稳定性测试
    multiple_tests()
    
    print("\n" + "=" * 50)
    print("🎉 所有测试完成!")

# 程序入口点
if __name__ == "__main__":
    main()