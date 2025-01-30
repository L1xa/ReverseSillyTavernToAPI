from http.server import HTTPServer
from .handler import ChatRequestHandler
from ..config import SERVER_HOST, SERVER_PORT

def run_server(chat_api):
    ChatRequestHandler.chat_api = chat_api
    server = HTTPServer((SERVER_HOST, SERVER_PORT), ChatRequestHandler)
    print(f"服务器启动在端口 {SERVER_PORT}")
    server.serve_forever() 