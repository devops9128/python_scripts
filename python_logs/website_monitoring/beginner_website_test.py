# 最简单的网站测试脚本
# 适合Python初学者学习

# 第一步：导入requests库（用来访问网站）
import requests

# 第二步：定义要测试的网站地址
website_url = "https://production-kul.unitedcaps.com/"

# 第三步：打印开始信息
print("开始测试网站...")
print("网站地址:", website_url)

# 第四步：尝试访问网站
try:
    # 发送请求到网站
    response = requests.get(website_url)
    
    # 检查返回的状态码
    status_code = response.status_code
    
    # 第五步：判断结果
    if status_code == 200:
        print("✅ 成功! 网站有响应终端")
        print("状态码:", status_code)
        print("这意味着网站正常工作")
    else:
        print("⚠️ 网站有响应，但可能有问题")
        print("状态码:", status_code)

except:
    # 如果出现任何错误
    print("❌ 失败! 网站无法访问")

print("测试结束")

# 额外信息：状态码的含义
print("\n状态码说明:")
print("200 = 成功")
print("404 = 页面不存在") 
print("500 = 服务器错误")
print("其他 = 各种不同情况")