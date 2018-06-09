from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from urlparse import unquote
import os, re, platform, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="0.0.0.0", type=str, help="IP to listen on (0.0.0.0 by default")
parser.add_argument("--port", default="8080", type=int, help="port to listen on (8080 by default)")

args = parser.parse_args()

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("OK")
        
    def do_POST(self):
        content_length = int(self.headers.getheader("content-length", 0))
        body = self.rfile.read(content_length)

        url = getParameter("url", body)
        cookies = getParameter("cookies", body)

        self._set_headers()
        self.wfile.write(LinkFinder(url, cookies))

    def log_message(self, format, *args):
        # Prevent the python script from logging every request.
        return
    
def getParameter(param, body):
    return unquote(re.findall("%s=([^&]*)" % param, body).pop(0))

def LinkFinder(url, cookies):
    output = os.popen("python -u %s -o cli -i %s -c %s" % (path_linkfinder, ('"' + url.replace('"', '\\"') + '"'), ('"' + cookies.replace('"', '\\"') + '"'))).read()
    print("JS File: %s\n\n%s\n---------------------" % (url, output))

    return output

def run(server_class=HTTPServer, handler_class=S, port=args.port, ip=args.ip):
    global path_linkfinder
    
    # Change this path to where linkfinder.py is located, Example path:
    # path_linkfinder = "C:\\Users\\karel\\Documents\\LinkFinder\\linkfinder.py"

    # Default path
    path_linkfinder = "./linkfinder.py"
    
    if os.path.isfile(path_linkfinder) == False:
        print("Path '%s' is invalid" % path_linkfinder)
        raise SystemExit

    server_address = (ip, port)
    httpd = server_class(server_address, handler_class)
    print("Listening on %s:%s" % (ip, port))
    httpd.serve_forever()

run()
