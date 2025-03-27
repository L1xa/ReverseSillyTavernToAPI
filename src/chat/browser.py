from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService  # 修改1：使用 Edge 的 Service
from selenium.webdriver.edge.options import Options as EdgeOptions  # 修改2：使用 Edge 的 Options
from ..config import CHROME_PATH, CHROME_DRIVER_PATH
import os

def create_browser():
    # 使用 EdgeOptions 替代 ChromeOptions
    options = EdgeOptions()
    
    # 设置 Edge 浏览器路径（如果自定义安装位置）
    if hasattr(CHROME_PATH, 'path') and CHROME_PATH.path:  # 检查配置是否存在
        options.binary_location = CHROME_PATH  # Edge 的可执行文件路径
    
    # Edge 的日志配置（与 Chrome 不同）
    options.set_capability('ms:edgeOptions', {
        'args': [
            '--log-level=0',           # 只显示致命错误
            '--enable-logging',        # 启用日志（但级别为0时不输出）
            '--no-sandbox',
            '--disable-dev-shm-usage'  # 避免 /dev/shm 不足的问题
        ],
        'excludeSwitches': ['enable-logging']  # 排除无关日志
    })
    
    # 初始化 Edge 服务（注意使用 EdgeService）
    service = EdgeService(
        executable_path=CHROME_DRIVER_PATH,  # Edge 驱动路径
        log_output=os.devnull              # 禁用驱动日志
    )
    
    # 启动 Edge 浏览器
    driver = webdriver.Edge(service=service, options=options)
    return driver
