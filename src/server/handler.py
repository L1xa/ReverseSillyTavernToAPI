from http.server import BaseHTTPRequestHandler
import json

class ChatRequestHandler(BaseHTTPRequestHandler):
    chat_api = None

    def do_GET(self):
        if self.path == '/status':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = "ready" if self.chat_api.is_ready() else "initializing"
            response_data = json.dumps({
                'status': status
            }).encode('utf-8')
            self.wfile.write(response_data)
            return

        self.send_error(404, "Not Found")

    def do_POST(self):
        if not self.chat_api.is_ready():
            self.send_response(503)  # Service Unavailable
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response_data = json.dumps({
                'error': '聊天系统正在初始化，请稍后再试'
            }, ensure_ascii=False).encode('utf-8')
            self.wfile.write(response_data)
            return

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data.decode('utf-8'))
        
        message = request_data.get('message', '')
        if not message:
            self.send_error(400, "Message is required")
            return
            
        response = self.chat_api.send_message(message)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response_data = json.dumps({
            'response': response
        }, ensure_ascii=False).encode('utf-8')
        self.wfile.write(response_data) 