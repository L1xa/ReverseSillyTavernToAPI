from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
import time
import os

# 配置常量
CHAT_URL = "http://127.0.0.1:8880"  # 替换为实际的聊天页面URL
MAX_WAIT_TIME = 30  # 最大等待时间（秒）

class ChatAPI:
    def __init__(self, chat_url=None):
        self.ready = False
        self.last_response = None
        self.chat_url = chat_url or CHAT_URL
        
        print("正在打开聊天界面...")
        self.driver = self._create_edge_browser()
        self.driver.get(self.chat_url)
        self._wait_for_chat_ready()
        self._setup_response_listener()

    def _create_edge_browser(self):
        """创建并配置Edge浏览器实例"""
        options = EdgeOptions()
        
        # Edge浏览器配置
        options.use_chromium = True
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        # 设置Edge驱动路径
        edge_driver_path = self._get_edge_driver_path()
        service = EdgeService(executable_path=edge_driver_path)
        
        return webdriver.Edge(service=service, options=options)

    def _get_edge_driver_path(self):
        """获取Edge驱动路径"""                                              #在这里设置edge路径
        possible_paths = [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedgedriver.exe",
            r"D:\sillyAPI\edgedriver_win64\msedgedriver.exe",
            os.path.join(os.getcwd(), "drivers", "msedgedriver.exe")
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
                
        raise FileNotFoundError("无法找到msedgedriver.exe")

    def _setup_response_listener(self):
        """设置响应监听器"""
        try:
            script = """
            window._apiResponses = [];
            const originalFetch = window.fetch;
            window.fetch = async function(...args) {
                const response = await originalFetch(...args);
                if(args[0].includes('/api/backends/')) {
                    const clone = response.clone();
                    const data = await clone.json();
                    window._apiResponses.push(data);
                }
                return response;
            };
            
            const originalXHROpen = XMLHttpRequest.prototype.open;
            XMLHttpRequest.prototype.open = function(method, url) {
                if(url.includes('/api/backends/')) {
                    this.addEventListener('load', function() {
                        try {
                            const data = JSON.parse(this.responseText);
                            window._apiResponses.push(data);
                        } catch(e) {}
                    });
                }
                originalXHROpen.apply(this, arguments);
            };
            true;
            """
            self.driver.execute_script(script)
        except Exception as e:
            print(f"设置响应监听器失败: {str(e)}")

    def _wait_for_chat_ready(self):
        """等待聊天界面准备就绪"""
        try:
            WebDriverWait(self.driver, MAX_WAIT_TIME).until(
                EC.presence_of_element_located((By.ID, "send_textarea"))
            )
            print("聊天界面已就绪")
            self.ready = True
        except TimeoutException:
            print("等待聊天界面超时")
            self.ready = False

    def is_ready(self):
        """检查聊天界面是否就绪"""
        return self.ready

    def get_chat_response(self):
        """获取聊天响应"""
        try:
            script = """
            if(window._apiResponses && window._apiResponses.length > 0) {
                return window._apiResponses.pop();
            }
            return null;
            """
            response = self.driver.execute_script(script)
            return self._parse_response(response)
        except Exception as e:
            print(f"获取响应时出错: {str(e)}")
            return None

    def _parse_response(self, response):
        """解析API响应"""
        if not response:
            return None
            
        if isinstance(response, str):
            try:
                response = json.loads(response)
            except json.JSONDecodeError:
                return None
                
        if isinstance(response, dict):
            if 'response' in response:
                return response['response']
            elif 'choices' in response and len(response['choices']) > 0:
                return response['choices'][0].get('message', {}).get('content')
                
        return None

    def send_message(self, message):
        """发送消息并获取响应"""
        if not self.ready:
            return "聊天系统尚未就绪，请稍后再试"
        
        try:
            self.driver.execute_script("window._apiResponses = [];")
            
            input_box = self.driver.find_element(By.ID, 'send_textarea')
            input_box.clear()
            input_box.send_keys(message)
            input_box.send_keys(Keys.RETURN)
            
            start_time = time.time()
            while True:
                response = self.get_chat_response()
                if response:
                    return response
                    
                if time.time() - start_time > MAX_WAIT_TIME:
                    return "等待响应超时"
                    
                time.sleep(0.5)
        except Exception as e:
            return f"发生错误：{str(e)}"

    def close(self):
        """关闭浏览器"""
        if hasattr(self, 'driver'):
            self.driver.quit()