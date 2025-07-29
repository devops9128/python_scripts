# 无依赖版本 - 持续ping监控脚本
# 使用Python内置模块，无需安装额外依赖
# 功能：持续检查 https://production-kul.unitedcaps.com/ 连接
# 当超时超过1分钟时，自动记录到 timeout.txt 文件

import urllib.request
import urllib.error
import time
import socket
from datetime import datetime

def main():
    # 要监控的网站
    website = "https://production-kul.unitedcaps.com/"
    
    # 确保timeout.txt文件路径
    timeout_file = "timeout.txt"
    
    print("🚀 开始持续ping监控 (无依赖版本)")
    print(f"🎯 目标网站: {website}")
    print("⏰ 超时阈值: 60秒 (1分钟)")
    print("📝 超时日志: timeout.txt")
    print("🛑 按 Ctrl+C 停止监控")
    print("=" * 60)
    
    # 计数器
    check_count = 0
    success_count = 0
    timeout_count = 0
    
    try:
        while True:  # 无限循环，持续监控
            check_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{check_count}] {current_time} - 正在ping...")
            
            try:
                # 记录开始时间
                start_time = time.time()
                
                # 创建请求，设置60秒超时
                request = urllib.request.Request(website)
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                
                # 发送请求
                with urllib.request.urlopen(request, timeout=60) as response:
                    # 计算响应时间
                    response_time = time.time() - start_time
                    success_count += 1
                    
                    # 获取状态码
                    status_code = response.getcode()
                    
                    # 连接成功
                    print(f"✅ 成功 - {response_time:.2f}秒 - 状态码: {status_code}")
                
            except socket.timeout:
                # 超时了！记录到文件
                response_time = time.time() - start_time
                timeout_count += 1
                
                # 准备要写入文件的信息
                timeout_info = f"[{current_time}] 第{check_count}次检查 - 连接超时 - 响应时间: {response_time:.2f}秒 - 超过1分钟阈值"
                
                # 写入timeout.txt文件
                try:
                    with open(timeout_file, "a", encoding="utf-8") as file:
                        file.write(timeout_info + "\n")
                    print(f"⏰ 超时! {response_time:.2f}秒 - 已记录到{timeout_file}")
                except Exception as write_error:
                    print(f"❌ 写入文件失败: {write_error}")
                
            except urllib.error.URLError as e:
                # URL错误（包括超时）
                response_time = time.time() - start_time
                
                if "timed out" in str(e) or response_time >= 60:
                    # 这是超时错误
                    timeout_count += 1
                    timeout_info = f"[{current_time}] 第{check_count}次检查 - URL超时 - 响应时间: {response_time:.2f}秒 - 超过1分钟阈值"
                    
                    try:
                        with open(timeout_file, "a", encoding="utf-8") as file:
                            file.write(timeout_info + "\n")
                        print(f"⏰ 超时! {response_time:.2f}秒 - 已记录到{timeout_file}")
                    except Exception as write_error:
                        print(f"❌ 写入文件失败: {write_error}")
                else:
                    # 其他URL错误
                    print(f"❌ URL错误: {e}")
                
            except Exception as error:
                # 其他错误
                print(f"❌ 其他错误: {error}")
            
            # 显示统计信息
            if check_count > 0:
                success_rate = (success_count / check_count) * 100
                print(f"📊 统计: 总计{check_count}次, 成功{success_count}次, 超时{timeout_count}次, 成功率{success_rate:.1f}%")
            
            # 等待5秒再检查下一次
            print("⏳ 等待5秒后继续...")
            time.sleep(5)

    except KeyboardInterrupt:
        # 用户按Ctrl+C停止程序
        print(f"\n\n🛑 监控已停止")
        print("=" * 60)
        print(f"📊 最终统计:")
        print(f"   总检查次数: {check_count}")
        print(f"   成功次数: {success_count}")
        print(f"   超时次数: {timeout_count}")
        if check_count > 0:
            success_rate = (success_count / check_count) * 100
            print(f"   成功率: {success_rate:.1f}%")
        print(f"📝 超时记录保存在: {timeout_file}")
        
        # 如果有超时记录，显示最近的几条
        try:
            with open(timeout_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    print(f"\n📋 最近的超时记录 (共{len(lines)}条):")
                    for line in lines[-3:]:  # 显示最后3条
                        print(f"   {line.strip()}")
                else:
                    print("\n✅ 没有超时记录")
        except FileNotFoundError:
            print("\n✅ 没有超时记录文件")
        
        print("=" * 60)

if __name__ == "__main__":
    main()