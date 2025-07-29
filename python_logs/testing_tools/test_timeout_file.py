# 测试timeout.txt文件生成功能
# 使用短超时时间来快速验证文件写入功能

import urllib.request
import urllib.error
import time
import socket
from datetime import datetime

def test_timeout_file():
    # 要监控的网站
    website = "https://production-kul.unitedcaps.com/"
    
    # 确保timeout.txt文件路径
    timeout_file = "timeout.txt"
    
    print("🧪 测试timeout.txt文件生成功能")
    print(f"🎯 目标网站: {website}")
    print("⏰ 测试超时阈值: 2秒 (用于快速测试)")
    print(f"📝 超时日志: {timeout_file}")
    print("🛑 按 Ctrl+C 停止测试")
    print("=" * 60)
    
    # 计数器
    check_count = 0
    success_count = 0
    timeout_count = 0
    
    try:
        while check_count < 5:  # 只测试5次
            check_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{check_count}] {current_time} - 正在测试...")
            
            try:
                # 记录开始时间
                start_time = time.time()
                
                # 创建请求，设置2秒超时（用于测试）
                request = urllib.request.Request(website)
                request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
                
                # 发送请求
                with urllib.request.urlopen(request, timeout=2) as response:
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
                timeout_info = f"[{current_time}] 第{check_count}次检查 - 连接超时 - 响应时间: {response_time:.2f}秒 - 测试超时阈值"
                
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
                
                if "timed out" in str(e) or response_time == ' ':
                    # 这是超时错误
                    timeout_count += 1
                    timeout_info = f"[{current_time}] 第{check_count}次检查 - URL超时 - 响应时间: {response_time:.2f}秒 - 测试超时阈值"
                    
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
            
            # 等待2秒再检查下一次
            if check_count < 5:
                print("⏳ 等待2秒后继续...")
                time.sleep(2)

    except KeyboardInterrupt:
        print(f"\n\n🛑 测试已停止")
    
    # 测试结束，显示结果
    print(f"\n\n🧪 测试完成")
    print("=" * 60)
    print(f"📊 测试统计:")
    print(f"   总检查次数: {check_count}")
    print(f"   成功次数: {success_count}")
    print(f"   超时次数: {timeout_count}")
    if check_count > 0:
        success_rate = (success_count / check_count) * 100
        print(f"   成功率: {success_rate:.1f}%")
    
    # 检查timeout.txt文件是否存在
    try:
        with open(timeout_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if lines:
                print(f"\n✅ {timeout_file} 文件生成成功! (共{len(lines)}条记录)")
                print(f"📋 文件内容:")
                for line in lines:
                    print(f"   {line.strip()}")
            else:
                print(f"\n📝 {timeout_file} 文件存在但为空")
    except FileNotFoundError:
        print(f"\n❌ {timeout_file} 文件未生成")
        
        # 尝试手动创建一个测试记录
        print("🔧 尝试手动创建测试记录...")
        try:
            test_info = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 测试记录 - 手动创建的测试条目"
            with open(timeout_file, "w", encoding="utf-8") as file:
                file.write(test_info + "\n")
            print(f"✅ 手动创建成功! 文件路径: {timeout_file}")
        except Exception as e:
            print(f"❌ 手动创建失败: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    test_timeout_file()