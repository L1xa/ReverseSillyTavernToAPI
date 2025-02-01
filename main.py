import threading
import argparse
import signal
import time
from src.chat.chat_api import ChatAPI
from src.server.server import run_server

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
                print("\n正在关闭服务...")
                chat.close()
                exit(0)
            
            signal.signal(signal.SIGINT, signal_handler)
            print("服务器已启动，按 Ctrl+C 退出...")
            
            # 保持程序运行
            while True:
                time.sleep(1)
            
    finally:
        chat.close()

if __name__ == "__main__":
    main()
