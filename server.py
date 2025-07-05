from http.server import SimpleHTTPRequestHandler
import socketserver
import os
import cgi

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Đặt thư mục lưu trữ file là /home/nero/share
        base_directory = "/home/nero/share"
        file_path = os.path.join(base_directory, self.path.strip("/"))

        try:
            # Kiểm tra nếu file tồn tại thì trả về file
            if os.path.isfile(file_path):
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Disposition", f'attachment; filename="{os.path.basename(file_path)}"')
                self.end_headers()
                with open(file_path, "rb") as file:
                    self.wfile.write(file.read())
            else:
                self.send_error(404, "File not found")
        except Exception as e:
            self.send_error(500, f"Server encountered an error: {e}")

    def do_POST(self):
        # Nhận file và lưu vào thư mục /home/nero/share
        upload_directory = "/home/nero/share"
        content_type, pdict = cgi.parse_header(self.headers.get('Content-Type'))
        
        # Kiểm tra và sửa lỗi boundary nếu cần
        if 'boundary' in pdict:
            if isinstance(pdict['boundary'], str):  # Nếu boundary là str
                pdict['boundary'] = pdict['boundary'].encode('ascii')  # Chuyển thành bytes

        if content_type == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            file_data = fields.get("file")[0]  # Lấy nội dung file
            filename = fields.get("filename")[0]  # Lấy tên file từ form

	    # Xử lý tên file: thay thế khoảng trắng bằng dấu gạch dưới hoặc mã hóa URL
            filename = filename.replace(" ", "_")  # Hoặc dùng urllib.parse.quote_plus(filename)

            # Lưu file vào thư mục upload_directory
            file_path = os.path.join(upload_directory, filename)
            with open(file_path, "wb") as f:
                f.write(file_data)

            # Phản hồi thành công, thêm header CORS
            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")  # Cho phép tất cả nguồn
            self.end_headers()
            self.wfile.write(b"File uploaded successfully!")
        else:
            self.send_error(400, "Bad Request: Invalid content type")

PORT = 8081
with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Serving files from /home/nero/share on port {PORT}")
    httpd.serve_forever()