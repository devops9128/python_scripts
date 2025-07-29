# 超时模拟测试 - 验证timeout.txt文件写入功能
# 使用不存在的网站来模拟超时情况

import urllib.request
import urllib.error
import time
import socket
from datetime import datetime

def test_timeout_simulation():
    # 使用一个不存在的网站来模拟超时
    website = "https://this-website-does-not-exist-12345.com/"
    
    # 确保timeout.txt文件路径
    timeout_file = "timeout.txt"
    
    print("🧪 超时模拟测试 - 验证timeout.txt文件写入")
    print(f"🎯 测试网站: {website}")
    print("⏰ 超时阈值: 5秒")
    print(f"📝 超时日志: {timeout_file}")
    print("=" * 60)
    
    # 计数器
    check_count = 0
    timeout_count = 0
    
    try:
        for i in range(2):  # 只测试2次
            check_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{check_count}] {current_time} - 正在测试超时...")
            
            try:
                # 记录开始时间
                start_time = time.time()
                
                # 创建请求，设置5秒超时
                request = urllib.request.Request(website)
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                
                # 发送请求
                with urllib.request.urlopen(request, timeout=5) as response:
                    response_time = time.time() - start_time
                    print(f"✅ 意外成功 - {response_time:.2f}秒")
                
            except socket.timeout:
                # 超时了！记录到文件
                response_time = time.time() - start_time
                timeout_count += 1
                
                timeout_info = f"[{current_time}] 第{check_count}次检查 - socket超时 - 响应时间: {response_time:.2f}秒 - 测试模拟超时"
                
                try:
                    with open(timeout_file, "a", encoding="utf-8") as file:
                        file.write(timeout_info + "\n")
                    print(f"⏰ 超时! {response_time:.2f}秒 - 已记录到{timeout_file}")
                except Exception as write_error:
                    print(f"❌ 写入文件失败: {write_error}")
                
            except urllib.error.URLError as e:
                response_time = time.time() - start_time
                timeout_count += 1
                
                timeout_info = f"[{current_time}] 第{check_count}次检查 - URL错误超时 - 响应时间: {response_time:.2f}秒 - 错误: {str(e)[:50]}"
                
                try:
                    with open(timeout_file, "a", encoding="utf-8") as file:
                        file.write(timeout_info + "\n")
                    print(f"⏰ URL超时! {response_time:.2f}秒 - 已记录到{timeout_file}")
                except Exception as write_error:
                    print(f"❌ 写入文件失败: {write_error}")
                
            except Exception as error:
                response_time = time.time() - start_time
                print(f"❌ 其他错误: {error}")
            
            print(f"📊 当前统计: 总计{check_count}次, 超时{timeout_count}次")

    except KeyboardInterrupt:
        print(f"\n\n🛑 测试已停止")
    
    # 测试结束，显示结果
    print(f"\n\n🧪 超时模拟测试完成")
    print("=" * 60)
    print(f"📊 测试统计:")
    print(f"   总检查次数: {check_count}")
    print(f"   超时次数: {timeout_count}")
    
    # 检查timeout.txt文件
    try:
        with open(timeout_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                print(f"\n✅ {timeout_file} 文件内容 (共{len(lines)}条记录):")
                for i, line in enumerate(lines, 1):
                    print(f"   {i}. {line.strip()}")
            else:
                print(f"\n📝 {timeout_file} 文件存在但为空")
    except FileNotFoundError:
        print(f"\n❌ {timeout_file} 文件未找到")
    
    print("=" * 60)

if __name__ == "__main__":
    test_timeout_simulation()