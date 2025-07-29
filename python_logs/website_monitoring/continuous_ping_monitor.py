#!/usr/bin/env python3
"""
持续监控网站连接脚本
功能：持续ping指定网站，超时超过1分钟时记录到timeout.txt
目标网站：https://production-kul.unitedcaps.com/
"""

import requests
import time
from datetime import datetime
import os

def write_timeout_log(message):
    """将超时信息写入timeout.txt文件"""
    try:
        with open("timeout.txt", "a", encoding="utf-8") as f:
            f.write(message + "\n")
        print(f"📝 超时信息已记录到 timeout.txt")
    except Exception as e:
        print(f"❌ 写入文件失败: {e}")

def ping_website():
    """ping网站并返回结果"""
    url = "https://production-kul.unitedcaps.com/"
    
    try:
        # 记录开始时间
        start_time = time.time()
        
        # 发送请求，设置60秒超时（1分钟）
        response = requests.get(url, timeout=60)
        
        # 计算响应时间
        response_time = time.time() - start_time
        
        # 返回成功结果
        return True, response_time, response.status_code
        
    except requests.exceptions.Timeout:
        # 超时异常
        response_time = time.time() - start_time
        return False, response_time, "TIMEOUT"
        
    except requests.exceptions.ConnectionError:
        # 连接错误
        response_time = time.time() - start_time
        return False, response_time, "CONNECTION_ERROR"
        
    except Exception as e:
        # 其他错误
        response_time = time.time() - start_time
        return False, response_time, f"ERROR: {e}"

def main():
    """主程序 - 持续监控"""
    
    url = "https://production-kul.unitedcaps.com/"
    ping_count = 0
    success_count = 0
    timeout_count = 0
    
    print("🚀 开始持续监控网站连接")
    print(f"🎯 目标网站: {url}")
    print(f"⏰ 超时阈值: 60秒 (1分钟)")
    print(f"📝 超时日志: timeout.txt")
    print("=" * 60)
    print("按 Ctrl+C 停止监控")
    print("=" * 60)
    
    try:
        while True:
            ping_count += 1
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"\n[{ping_count}] {current_time} - 正在检查连接...")
            
            # 执行ping测试
            success, response_time, status = ping_website()
            
            if success:
                # 连接成功
                success_count += 1
                print(f"✅ 连接成功 - 响应时间: {response_time:.2f}秒 - 状态码: {status}")
                
            else:
                # 连接失败或超时
                if status == "TIMEOUT" or response_time >= 60:
                    # 超时情况
                    timeout_count += 1
                    timeout_message = f"[{current_time}] 第{ping_count}次检查 - 超时 - 响应时间: {response_time:.2f}秒 - 状态: {status}"
                    
                    print(f"⏰ 超时! 响应时间: {response_time:.2f}秒")
                    write_timeout_log(timeout_message)
                    
                else:
                    # 其他错误
                    print(f"❌ 连接失败 - 响应时间: {response_time:.2f}秒 - 状态: {status}")
            
            # 显示统计信息
            success_rate = (success_count / ping_count) * 100
            print(f"📊 统计: 总计{ping_count}次, 成功{success_count}次, 超时{timeout_count}次, 成功率{success_rate:.1f}%")
            
            # 等待5秒再进行下一次检查
            print("⏳ 等待5秒后继续...")
            time.sleep(5)
            
    except KeyboardInterrupt:
        # 用户按Ctrl+C停止
        print(f"\n\n🛑 监控已停止")
        print("=" * 60)
        print(f"📊 最终统计:")
        print(f"   总检查次数: {ping_count}")
        print(f"   成功次数: {success_count}")
        print(f"   超时次数: {timeout_count}")
        if ping_count > 0:
            success_rate = (success_count / ping_count) * 100
            print(f"   成功率: {success_rate:.1f}%")
        print(f"📝 超时日志保存在: timeout.txt")
        print("=" * 60)

if __name__ == "__main__":
    main()