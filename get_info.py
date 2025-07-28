import wmi
import platform
import psutil
import os

# 初始化 WMI 对象
c = wmi.WMI()

# 获取当前用户桌面路径
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
output_file = os.path.join(desktop_path, "system_info.txt")

# 写入文件
with open(output_file, "w", encoding="utf-8") as f:

    def log(text):
        print(text)
        f.write(text + "\n")

    log("========= 系统基础信息 =========")
    log("系统名称: " + platform.system())
    log("系统版本: " + platform.version())
    log("发行版本: " + platform.release())
    log("主机名称: " + platform.node())
    log("CPU 架构: " + platform.machine())

    log("\n========= CPU 信息 =========")
    for processor in c.Win32_Processor():
        log("CPU 型号: " + processor.Name.strip())
        log(f"逻辑核心数: {psutil.cpu_count(logical=True)}")
        log(f"物理核心数: {psutil.cpu_count(logical=False)}")

    log("\n========= 内存信息 =========")
    for mem in c.Win32_PhysicalMemory():
        log("厂商: " + (mem.Manufacturer.strip() if mem.Manufacturer else "未知"))
        log("容量 (GB): " + str(round(int(mem.Capacity) / (1024 ** 3), 2)))
        log("序列号: " + (mem.SerialNumber.strip() if mem.SerialNumber else "未知"))
        log("速度 (MHz): " + str(mem.Speed))

    log("\n========= 硬盘信息 =========")
    for disk in c.Win32_DiskDrive():
        log("硬盘型号: " + disk.Model.strip())
        log("接口类型: " + disk.InterfaceType)
        log("硬盘大小 (GB): " + str(round(int(disk.Size) / (1024 ** 3), 2)))

    log("\n========= 主板信息 =========")
    for board in c.Win32_BaseBoard():
        log("主板型号: " + (board.Product.strip() if board.Product else "未知"))
        log("厂商: " + (board.Manufacturer.strip() if board.Manufacturer else "未知"))

    log("\n========= BIOS 信息 =========")
    for bios in c.Win32_BIOS():
        log("电脑序列号: " + (bios.SerialNumber.strip() if bios.SerialNumber else "未知"))
        log("BIOS 版本: " + " / ".join(bios.BIOSVersion))

print(f"\n✅ 信息已保存到：{output_file}")
