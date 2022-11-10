import sys
import os
import getopt
from http.server import BaseHTTPRequestHandler, HTTPServer
from base64 import b64decode
import requests
import json
from okera import context

hostName = os.environ.get('HOSTNAME', '0.0.0.0')
serverPort = int(os.environ.get('PORT', 5010))
tokenServiceHost = os.environ.get('TOKEN_SERVICE_HOST', 'localhost')
tokenServicePort = int(os.environ.get('TOKEN_SERVICE_PORT', 5001))
plannerHost = os.environ.get('PLANNER_HOST')
plannerPort = int(os.environ.get('PLANNER_PORT', 12050))

def get_okera_token(user):
    print("Getting token...")
    response = requests.get("http://%s:%s/%s" % (tokenServiceHost, tokenServicePort, user))
    if response.status_code == 200:
        print("Got token in", response.text)
        with open(response.text) as f:
            token = ''.join(f.readlines())
        print("Got token data: ", token[:20], "...")
        return token
    else:
        print("An error (%d) occurred getting token: %s" % (response.status_code, response.text))
        return None


def get_user_from_auth(auth):
    payload = auth.split(' ')[1] # e.g. "Basic dGVzdDp0ZXN0"
    decoded = b64decode(payload).decode('utf-8')
    return decoded.split(':')[0]


def list_databases(auth):
    ctx = context()
    user = get_user_from_auth(auth)
    token = get_okera_token(user)
    ctx.enable_token_auth(token_str=token)
    with ctx.connect(host=plannerHost, port=plannerPort) as conn:
        dbs = conn.list_databases()    
    return dbs


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if 'authorization' in self.headers:
            try:
                print(self.headers)
                dbs = list_databases(self.headers['authorization'])
            except Exception as e:
                print("ERROR:", e)
                self.send_response(500)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(bytes("Internal Server Error!", "utf-8"))
                return
            self.send_response(200)
            self.send_header("Content-type", "text/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps(dbs), "utf-8"))
        else:
            self.send_response(401)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(bytes("Unauthorized!", "utf-8"))


def main(argv):
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")


# Main entrypoint
if __name__ == "__main__":
    main(sys.argv[1:])