import threading
import argparse
import signal
import time
import os
from src.chat.chat_api import ChatAPI
from src.server.server import run_server

# 添加关闭标志和上次按下Ctrl+C的时间
is_shutting_down = False
last_sigint_time = 0
FORCE_QUIT_INTERVAL = 1  # 1秒内按两次Ctrl+C将强制退出

def console_chat(chat):
    print("开始对话（输入 !!!exit 结束对话）...")
    while True:
        user_input = input("你: ")
        if user_input.strip() == "!!!exit":
            print("结束对话")
            break
            
        response = chat.send_message(user_input)
        print("AI回复:", response)
        print()

def main():
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='SillyTavernAPI对话')
    parser.add_argument('--console', action='store_true', 
                      help='是否启用控制台对话模式')
    args = parser.parse_args()

    chat = ChatAPI()
    try:
        # 启动HTTP服务器
        server_thread = threading.Thread(target=run_server, args=(chat,))
        server_thread.daemon = True
        server_thread.start()
        
        # 根据参数决定是否启动控制台对话
        if args.console:
            console_chat(chat)
        else:
            # 添加信号处理，使得可以通过Ctrl+C优雅地退出
            def signal_handler(signum, frame):
                global is_shutting_down, last_sigint_time
                current_time = time.time()
                
                # 检查是否在短时间内按下两次Ctrl+C
                if current_time - last_sigint_time < FORCE_QUIT_INTERVAL:
                    print("\n检测到连续两次Ctrl+C，强制退出...")
                    os._exit(1)  # 强制退出所有进程
                
                last_sigint_time = current_time
                
                if is_shutting_down:
                    print("\n正在强制退出...")
                    os._exit(1)  # 如果正常退出卡住，强制退出
                    return
                    
                is_shutting_down = True
                print("\n正在关闭服务...")
                try:
                    chat.close()
                    exit(0)
                except:
                    os._exit(1)  # 如果关闭出错，强制退出
            
            signal.signal(signal.SIGINT, signal_handler)
            print("服务器已启动，按 Ctrl+C 退出，连按两次 Ctrl+C 强制退出...")
            
            # 保持程序运行
            while True:
                time.sleep(1)
            
    finally:
        chat.close()

if __name__ == "__main__":
    main()
