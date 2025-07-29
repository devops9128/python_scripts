# 持续ping监控脚本 - 生产版本
# 功能：持续检查 https://production-kul.unitedcaps.com/ 连接
# 当超时超过1分钟时，自动记录到 timeout.txt 文件

import requests
import time
from datetime import datetime

def main():
    # 要监控的网站
    website = "https://production-kul.unitedcaps.com/"
    
    print("🚀 开始持续ping监控")
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
                
                # 发送请求，超时设置为60秒（1分钟）
                response = requests.get(website, timeout=60)
                
                # 计算响应时间
                response_time = time.time() - start_time
                success_count += 1
                
                # 连接成功
                print(f"✅ 成功 - {response_time:.2f}秒 - 状态码: {response.status_code}")
                
            except requests.exceptions.Timeout:
                # 超时了！记录到文件
                response_time = time.time() - start_time
                timeout_count += 1
                
                # 准备要写入文件的信息
                timeout_info = f"[{current_time}] 第{check_count}次检查 - 连接超时 - 响应时间: {response_time:.2f}秒 - 超过1分钟阈值"
                
                # 写入timeout.txt文件
                try:
                    with open("timeout.txt", "a", encoding="utf-8") as file:
                        file.write(timeout_info + "\n")
                    print(f"⏰ 超时! {response_time:.2f}秒 - 已记录到timeout.txt")
                except Exception as write_error:
                    print(f"❌ 写入文件失败: {write_error}")
                
            except requests.exceptions.ConnectionError:
                # 连接错误
                print(f"❌ 连接失败 - 无法连接到网站")
                
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
        print(f"📝 超时记录保存在: timeout.txt")
        
        # 如果有超时记录，显示最近的几条
        try:
            with open("timeout.txt", "r", encoding="utf-8") as file:
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