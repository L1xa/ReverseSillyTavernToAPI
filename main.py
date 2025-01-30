import threading
from src.chat.chat_api import ChatAPI
from src.server.server import run_server

def main():
    chat = ChatAPI()
    try:
        # 启动HTTP服务器
        server_thread = threading.Thread(target=run_server, args=(chat,))
        server_thread.daemon = True
        server_thread.start()
        
        print("开始对话（输入 !!!exit 结束对话）...")
        while True:
            user_input = input("你: ")
            if user_input.strip() == "!!!exit":
                print("结束对话")
                break
                
            response = chat.send_message(user_input)
            print("AI回复:", response)
            print()
            
    finally:
        chat.close()

if __name__ == "__main__":
    main()
