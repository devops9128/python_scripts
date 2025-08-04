#!/usr/bin/env python3

"""
    Smart monitoring system script
    functions: check thershold value, warning, log record

"""

import psutil
import datetime
import json
import os
import sys


class SystemMonitor:

    def __init__(self, config_file='./monitor_config.json'):
        """initial monitor"""
        self.load_config(config_file)
        self.alerts = []

    def load_config(self, config_file):
        """load config file"""
        try:
            with open(config_file, mode='r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"config file not found: {config_file}")
            sys.exit(1)
        except json.JSONDecodeError:
            print(f"config file format error: {config_file}")
            sys.exit(1)

    def get_system_stats(self):
        """collect system statistic info"""
        stats = {
            'timestamp': datetime.datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory': psutil.virtual_memory().percent,
            'disk_percent': (psutil.disk_usage('/').used / psutil.disk_usage('/').total) * 100,
            'load_average': self.get_load_average()
        }

        return stats

    def get_load_average(self):
        """collect load average thresholds"""
        try:
            return list(psutil.getloadavg())
        except AttributeError:
            return [0, 0, 0]

    def check_thresholds(self):
        """check thresholds and raise warining"""
        thresholds = self.config['thresholds']

        # CPU check
        if stats['cpu_percent'] >= thresholds['cpu_critical']:
            self.alerts.append({
                'level': 'CRITICAL',
                'type': 'CPU',
                'message': f'CPU usage extreamly overload {stats['cpu_percent']:.1f}%'
            })

        elif stats['cpu_percent'] >= thresholds['cpu_warning']:
            self.alerts.append({
                'level': 'WARNING',
                'type': 'CPU',
                'message': f'CPU usage overload: {stats['cpu_percent']:.1f}%'
            })

        # Memory check
        if stats['memory_percent'] >= thresholds['memory_critical']:
            self.alerts.append({
                'level': 'CRITICAL',
                'type': 'MEMORY',
                'message': f'MEMORY usage extreamly overload {stats['memory_percent']:.1f}%'
            })

        elif stats['memory_percent'] >= thresholds['memory_warning']:
            self.alerts.append({
                'level': 'WARNING',
                'type': 'MEMORY',
                'message': f'MEMORY usage overload: {stats['memory_percent']:.1f}%'
            })

        # Harddisk check
        if stats['disk_percent'] >= thresholds['disk_critical']:
            self.alerts.append({
                'level': 'CRITICAL',
                'type': 'DISK',
                'message': f'DISK usage extreamly overload {stats['disk_percent']:.1f}%'
            })

        elif stats['disk_percent'] >= thresholds['disk_warning']:
            self.alerts.append({
                'level': 'WARNING',
                'type': 'DISK',
                'message': f'DISK usage overload: {stats['disk_percent']:.1f}%'
            })

    def print_report(self, stats):
        """打印监控报告"""
        print("=" * 60)
        print(f"🖥️  系统监控报告 - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # 系统状态
        status = "🟢 正常"
        if any(alert['level'] == 'CRITICAL' for alert in self.alerts):
            status = "🔴 严重"
        elif any(alert['level'] == 'WARNING' for alert in self.alerts):
            status = "🟡 警告"

        print(f"系统状态: {status}")
        print(f"CPU使用率: {stats['cpu_percent']:.1f}%")
        print(f"内存使用率: {stats['memory_percent']:.1f}%")
        print(f"磁盘使用率: {stats['disk_percent']:.1f}%")

        if stats['load_average'][0] > 0:
            print(f"系统负载: {stats['load_average'][0]:.2f}")

        # 显示告警
        if self.alerts:
            print("\n⚠️  告警信息:")
            for alert in self.alerts:
                icon = "🔴" if alert['level'] == 'CRITICAL' else "🟡"
                print(f"  {icon} [{alert['level']}] {alert['message']}")
        else:
            print("\n✅ 无告警信息")

        print("=" * 60)

    def log_data(self, stats):
        """记录数据到日志文件"""
        log_date = datetime.date.today().strftime('%Y%m%d')
        log_file = f"logs/monitor_{log_date}.log"

        # 确保logs目录存在
        os.makedirs('logs', exist_ok=True)

        log_entry = {
            'timestamp': stats['timestamp'],
            'cpu_percent': stats['cpu_percent'],
            'memory_percent': stats['memory_percent'],
            'disk_percent': stats['disk_percent'],
            'alerts': self.alerts
        }

        with open(log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')

    def run_monitoring(self):
        """运行监控"""
        print("🚀 启动系统监控...")

        # 获取系统统计
        stats = self.get_system_stats()

        # 检查阈值
        self.check_thresholds(stats)

        # 打印报告
        self.print_report(stats)

        # 记录日志
        self.log_data(stats)

        # 如果有告警，返回非零退出码
        if self.alerts:
            return 1
        return 0

if __name__ == "__main__":
    monitor = SystemMonitor()
    exit_code = monitor.run_monitoring()
    sys.exit(exit_code)

            