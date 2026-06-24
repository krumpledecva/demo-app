from http.server import BaseHTTPRequestHandler
import random
import json


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        die1 = random.randint(1, 6)
        die2 = random.randint(1, 6)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps({"die1": die1, "die2": die2, "total": die1 + die2}).encode())

    def log_message(self, *args):
        pass
