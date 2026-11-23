import os
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote

UUID = os.environ["UUID"]
WS_PATH = os.environ["WS_PATH"]
NODE_HOST = os.environ["NODE_HOST"]
SUB_TOKEN = os.environ["SUB_TOKEN"]
PORT = int(os.environ.get("PORT", "8080"))

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/sub/" + SUB_TOKEN:
            self.send_error(404)
            return

        name = "Altare-Stockholm"
        params = (
            "encryption=none"
            "&security=tls"
            "&sni=" + quote(NODE_HOST, safe="")
            "&type=ws"
            "&host=" + quote(NODE_HOST, safe="")
            "&path=" + quote(WS_PATH, safe="")
            "&fp=chrome"
        )

        link = (
            "vless://" + UUID + "@" + NODE_HOST +
            ":443?" + params + "#" + quote(name)
        )

        result = base64.b64encode(link.encode()).decode()

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(result.encode())

    def log_message(self, format, *args):
        print(format % args)

server = HTTPServer(("0.0.0.0", PORT), Handler)
print("Subscription server listening on", PORT)
server.serve_forever()
