from time import sleep
import requests
import time
from datetime import datetime
from requests.exceptions import RequestException
from urllib3.exceptions import NameResolutionError

"""
    核心要点
    * 重复的代码可以创建函数调用
        with open () as f:
            f.write()
            
    * 函数的注释类型
        def func(url: str, status: str, error: str):                                                    参数的类型是字符串
        def func(url: str=None, status: str=None, error: str=None):                                     参数默认值是None，代表可以不传参
        def func(url: Option[str]=None, status: Option[str]=None, error: Option[str]=None):             有注释类型 + 指定默认实参为 None，
                                                                                                        最好写成 Option[str]=None, 在静态类型检查工具（如 mypy）会报 warning，说 str 和 None 类型不匹配
                                                                                                        Option[str] 可以是 字符串，但是不建议
        def func(url: str=None, status: str=None, error: str=None) -> None:                             返回值为空值，不会返回有用的代码
        
    * 参数传递规则回顾
      1. 位置参数（positional arguments）必须放在前面，
      2. 关键字参数（keyword arguments）放在后面，
      3. 不能出现“先关键字再位置参数”的形式，否则会报 SyntaxError: positional argument follows keyword argument。
      
        def func(easy=None, middle=None, hard): ❌
        def func(hard, esy=None, middle=None):  ✅
        
    * 外层 try 包裹 while	整个 while 被中断，直接进入 except	❌ 不会继续 [ 就像“公交车一旦爆胎，整条线路停运”。 ]
    * while 内部 try	本次异常被捕获，下一轮 while 继续	✅ 会继续 [ 就像“公交车爆胎后修好，再继续下一趟”。 ]
"""

odoo_web = "https://production-kul.unitedcaps.com"
google_web = "https://www.google.com"

# Define a function to output a file record
def log_timeout(url: str = None, status: str = None, error: str = None) -> None:
    timestamp = datetime.now().strftime("%d-%m-%Y - %H:%M:%S")
    with open('timeout.txt', mode='a', encoding='UTF-8') as f:
        f.write(f"{timestamp} {url}， Return code: {status} failed access\n")

# Print the head line when execute the process
print(f"开始测试 {odoo_web} 时间 : {datetime.now().strftime("%d-%m-%Y - %H:%M:%S")}")
with open('.\\timeout.txt', mode='a', encoding='UTF-8') as f:
    f.write(f"开始测试 {odoo_web} 时间 : {datetime.now().strftime("%d-%m-%Y - %H:%M:%S")}\n")

# First layer try
try:
    # Execute while loop
    while True:
        # Second layer try
        try:

            # Odoo link connection test
            odoo_respone = requests.get(odoo_web, timeout=5)
            odoo_status = odoo_respone.status_code

            if odoo_status != 200:
                log_timeout(url=odoo_web, status=odoo_status, error=None)
            else:
                print(
                    f"Return code: {odoo_status} {odoo_web} {datetime.now().strftime("%d-%m-%Y (%H:%M:%S)")} access normal🍀"
                )

        except RequestException as e:
            print(f"⚠️ Odoo请求错误: {e}")
            log_timeout(url=odoo_web, status=None, error=str(e))

        try:

            # Google link connection test
            google_respone = requests.get(google_web, timeout=5)
            google_status = google_respone.status_code

            if google_status != 200:
                log_timeout(url=google_web, status=google_status, error=None)
            else:
                print(
                    f"Return code: {google_status} {google_web} {datetime.now().strftime("%d-%m-%Y (%H:%M:%S)")} access normal🍀"
                )

        except RequestException as e:
            print(f"⚠️ Google请求错误: {e}")
            log_timeout(url=google_web, status=None, error=str(e))

        # Continue execution after 10 seconds
        sleep(10)

# Exit the process when detect ctrl + c
except KeyboardInterrupt:
    print("\n检测到 Ctrl+C，程序即将退出。")
