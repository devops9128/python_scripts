# 测试版本 - 可以模拟超时情况
# 用于验证timeout.txt文件写入功能

import requests
import time
from datetime import datetime

# 要监控的网站
website = "https://production-kul.unitedcaps.com/"

print("测试版本 - 持续监控网站:", website)
print("正常超时阈值: 60秒")
print("测试超时阈值: 2秒 (用于快速测试)")
print("按 Ctrl+C 停止监控")
print("-" * 50)

# 计数器
check_count = 0

try:
    while True:
        check_count += 1
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"[{check_count}] {current_time} - 检查中...")
        
        try:
            # 记录开始时间
            start_time = time.time()
            
            # 为了测试，我们使用2秒超时来快速看到效果
            # 在实际使用中，您可以改回60秒
            timeout_seconds = 2  # 测试用，实际使用改为60
            
            response = requests.get(website, timeout=timeout_seconds)
            
            # 计算响应时间
            response_time = time.time() - start_time
            
            # 连接成功
            print(f"✅ 成功 - {response_time:.2f}秒 - 状态码: {response.status_code}")
            
        except requests.exceptions.Timeout:
            # 超时了！记录到文件
            response_time = time.time() - start_time
            
            # 准备要写入文件的信息
            timeout_info = f"[{current_time}] 第{check_count}次检查 - 超时 - 响应时间: {response_time:.2f}秒 - 超时阈值: {timeout_seconds}秒"
            
            # 写入timeout.txt文件
            with open("timeout.txt", "a", encoding="utf-8") as file:
                file.write(timeout_info + "\n")
            
            print(f"⏰ 超时! {response_time:.2f}秒 - 已记录到timeout.txt")
            
        except Exception as error:
            # 其他错误
            print(f"❌ 错误: {error}")
        
        # 等待3秒再检查下一次（测试用，比较快）
        time.sleep(3)

except KeyboardInterrupt:
    # 用户按Ctrl+C停止程序
    print(f"\n监控已停止，总共检查了 {check_count} 次")
    print("超时记录保存在 timeout.txt 文件中")
    
    # 显示timeout.txt的内容
    try:
        with open("timeout.txt", "r", encoding="utf-8") as file:
            content = file.read()
            if content:
                print("\n=== timeout.txt 内容 ===")
                print(content)
            else:
                print("\ntimeout.txt 文件为空（没有发生超时）")
    except FileNotFoundError:
        print("\ntimeout.txt 文件不存在（没有发生超时）")