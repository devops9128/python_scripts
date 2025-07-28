import wmi
import platform
import psutil

# 初始化 WMI 对象
c = wmi.WMI()

print("========= 系统基础信息 =========")
print("系统名称:", platform.system())
print("系统版本:", platform.version())
print("发行版本:", platform.release())
print("主机名称:", platform.node())
print("CPU 架构:", platform.machine())

print("\n========= CPU 信息 =========")
for processor in c.Win32_Processor():
    print("CPU 型号:", processor.Name.strip())
    print("逻辑核心数:", psutil.cpu_count(logical=True))
    print("物理核心数:", psutil.cpu_count(logical=False))

print("\n========= 内存信息 =========")
for mem in c.Win32_PhysicalMemory():
    print("厂商:", mem.Manufacturer.strip() if mem.Manufacturer else "未知")
    print("容量 (GB):", round(int(mem.Capacity) / (1024 ** 3), 2))
    print("序列号:", mem.SerialNumber.strip() if mem.SerialNumber else "未知")
    print("速度 (MHz):", mem.Speed)

print("\n========= 硬盘信息 =========")
for disk in c.Win32_DiskDrive():
    print("硬盘型号:", disk.Model.strip())
    print("接口类型:", disk.InterfaceType)
    print("硬盘大小 (GB):", round(int(disk.Size) / (1024 ** 3), 2))

print("\n========= 主板信息 =========")
for board in c.Win32_BaseBoard():
    print("主板型号:", board.Product.strip() if board.Product else "未知")
    print("厂商:", board.Manufacturer.strip() if board.Manufacturer else "未知")

print("\n========= BIOS 信息 =========")
for bios in c.Win32_BIOS():
    print("电脑序列号（Serial Number）:", bios.SerialNumber.strip() if bios.SerialNumber else "未知")
    print("BIOS 版本:", " / ".join(bios.BIOSVersion))

