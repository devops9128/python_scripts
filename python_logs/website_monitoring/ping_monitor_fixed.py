# 生产版本 - 持续ping监控脚本 (修复版)
# 无依赖版本，使用Python内置模块
# 功能：持续检查 https://production-kul.unitedcaps.com/ 连接
# 当超时超过1分钟时，自动记录到 timeout.txt 文件

import urllib.request
import urllib.error
import time
import socket
import os
from datetime import datetime

def main():
    # 要监控的网站
    website = "https://production-kul.unitedcaps.com/"
    
    # 确保timeout.txt文件路径 - 使用绝对路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    timeout_file = os.path.join(script_dir, "timeout.txt")
    
    print("🚀 开始持续ping监控 (修复版)")
    print(f"🎯 目标网站: {website}")
    print("⏰ 超时阈值: 60秒 (1分钟)")
    print(f"📝 超时日志: {timeout_file}")
    print("🛑 按 Ctrl+C 停止监控")
    print("=" * 60)
    
    # 计数器
    check_count = 0
    success_count = 0
    timeout_count = 0
    
    # 确保可以写入文件
    try:
        test_write = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 监控开始 - 文件写入测试\n"
        with open(timeout_file, "a", encoding="utf-8") as file:
            file.write(test_write)
        print(f"✅ 文件写入测试成功: {timeout_file}")
    except Exception as e:
        print(f"❌ 文件写入测试失败: {e}")
        print("⚠️  请检查文件权限或磁盘空间")
        return
    
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
                # socket超时 - 记录到文件
                response_time = time.time() - start_time
                timeout_count += 1
                
                timeout_info = f"[{current_time}] 第{check_count}次检查 - Socket超时 - 响应时间: {response_time:.2f}秒 - 超过60秒阈值"
                
                try:
                    with open(timeout_file, "a", encoding="utf-8") as file:
                        file.write(timeout_info + "\n")
                    print(f"⏰ Socket超时! {response_time:.2f}秒 - 已记录到文件")
                except Exception as write_error:
                    print(f"❌ 写入文件失败: {write_error}")
                
            except urllib.error.URLError as e:
                # URL错误（包括超时）
                response_time = time.time() - start_time
                
                # 检查是否是超时相关的错误
                error_str = str(e).lower()
                is_timeout = any(keyword in error_str for keyword in ['timeout', 'timed out', 'time out']) or response_time >= 60
                
                if is_timeout:
                    timeout_count += 1
                    timeout_info = f"[{current_time}] 第{check_count}次检查 - URL超时 - 响应时间: {response_time:.2f}秒 - 错误: {str(e)[:100]}"
                    
                    try:
                        with open(timeout_file, "a", encoding="utf-8") as file:
                            file.write(timeout_info + "\n")
                        print(f"⏰ URL超时! {response_time:.2f}秒 - 已记录到文件")
                    except Exception as write_error:
                        print(f"❌ 写入文件失败: {write_error}")
                else:
                    # 其他URL错误（非超时）
                    print(f"❌ URL错误: {e}")
                
            except Exception as error:
                # 其他错误
                response_time = time.time() - start_time
                print(f"❌ 其他错误: {error} (响应时间: {response_time:.2f}秒)")
            
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
        
        # 显示超时记录
        try:
            with open(timeout_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
                if lines:
                    # 过滤掉测试记录，只显示真实的超时记录
                    timeout_lines = [line for line in lines if "超时" in line and "测试" not in line]
                    if timeout_lines:
                        print(f"\n📋 超时记录 (共{len(timeout_lines)}条):")
                        for line in timeout_lines[-5:]:  # 显示最后5条
                            print(f"   {line.strip()}")
                    else:
                        print(f"\n✅ 没有真实的超时记录 (文件中有{len(lines)}条测试记录)")
                else:
                    print("\n✅ 没有超时记录")
        except FileNotFoundError:
            print("\n✅ 没有超时记录文件")
        
        print("=" * 60)

if __name__ == "__main__":
    main()