import os
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

GIT_SHA = os.environ.get("GIT_SHA", "local-dev")

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.client_address[0]
        print(f"Request received from {client_ip} → {self.path}")

        if self.path == "/":
            message = "Hello from Python server"
            self._respond(200, "text/plain", message)

        elif self.path == "/whoami":
            message = f"Your IP address is {client_ip}"
            self._respond(200, "text/plain", message)

        elif self.path == "/status":
            payload = json.dumps({
                "status": "ok",
                "server": "Python HTTP Server",
                "container": "backend",
                "version": GIT_SHA,
                "ip_seen": client_ip
            })
            self._respond(200, "application/json", payload)

        elif self.path == "/pipeline":
            payload = json.dumps({
                "pipeline": [
                    { "step": 1, "name": "Code Push",         "detail": "Developer pushes code to GitHub main branch" },
                    { "step": 2, "name": "CI Triggered",       "detail": "GitHub Actions runner spins up automatically" },
                    { "step": 3, "name": "Docker Build",       "detail": "Backend & frontend images built from source" },
                    { "step": 4, "name": "Integration Test",   "detail": "curl --fail verifies the full stack is alive" },
                    { "step": 5, "name": "Push to Registry",   "detail": "Verified images pushed to Docker Hub with SHA tag" },
                    { "step": 6, "name": "SSH Deploy",         "detail": "CD job SSHes into AWS EC2 and restarts containers" },
                    { "step": 7, "name": "You're Here",        "detail": "You're seeing the exact image that passed CI — nothing else" }
                ],
                "deployed_sha": GIT_SHA
            })
            self._respond(200, "application/json", payload)

        else:
            self._respond(404, "text/plain", "404 Not Found")

    def _respond(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body.encode())

    def log_message(self, format, *args):
        print(f"[{self.address_string()}] {format % args}")

server = HTTPServer(("0.0.0.0", 8000), MyHandler)
print(f"Server running | version={GIT_SHA}")
server.serve_forever()
