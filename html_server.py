from http.server import SimpleHTTPRequestHandler
import socketserver
import os

class CustomHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path):
        # Gửi lỗi 403 Forbidden nếu người dùng cố gắng xem danh sách thư mục
        self.send_error(403, "Directory listing not allowed")
        return None

PORT = 9090
DIRECTORY = "/home/nero"

class CustomHTMLHandler(CustomHandler):
    def do_GET(self):
        # Chỉ phục vụ file upload_form.html nếu truy cập trực tiếp
        if self.path == "/":
            self.path = "/upload_form.html"
        return super().do_GET()

with socketserver.TCPServer(("", PORT), CustomHTMLHandler) as httpd:
    os.chdir(DIRECTORY)  # Thư mục chứa file HTML
    print(f"Serving HTML on port {PORT}")
    httpd.serve_forever()