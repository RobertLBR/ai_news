from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import os
from datetime import datetime

class NewsHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/news':
            today = datetime.now().strftime('%Y-%m-%d')
            file_path = f"../data/news_{today}.json"
            
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    news_data = json.load(f)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(news_data).encode())
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'No news found for today'}).encode())
        else:
            super().do_GET()

def run_server():
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, NewsHandler)
    print('Server running on port 8000...')
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()