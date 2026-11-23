
import os
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import quote, urlencode

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

        params = urlencode({
            "encryption": "none",
            "security": "tls",
            "sni": NODE_HOST,
            "type": "ws",
            "host": NODE_HOST,
            "path": WS_PATH,
            "fp": "chrome"
        })

        link = (
            f"vless://{UUID}@{NODE_HOST}:443?"
            f"{params}#{quote('Altare-Stockholm')}"
        )

        result = base64.b64encode(
            link.encode("utf-8")
        ).decode("ascii")

        self.send_response(200)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(result.encode("ascii"))

    def log_message(self, format, *args):
        print(format % args)

server = HTTPServer(("0.0.0.0", PORT), Handler)
print("Subscription server listening on", PORT)
server.serve_forever()
