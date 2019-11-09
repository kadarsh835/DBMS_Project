import http.server
import socketserver
import os
from main_app import config

web_dir = os.path.join(os.path.dirname(__file__), 'main_app\\templates\\')
os.chdir(web_dir)

PORT = 8000
Handler = http.server.SimpleHTTPRequestHandler


with socketserver.TCPServer(("", PORT), Handler) as httpd:
    config.connect()
    print("Server at port: ", PORT)
    print("Quit the server by Ctrl+C")
    httpd.serve_forever()