import threading

import sys
from os import curdir, sep

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# from cam import training
# from cam import state

PORT = 8000


class CameraHandler(BaseHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):

        global training
        global state

        if self.path == "/cam.jpg":
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        if self.path == "/":
            self.path = "/index.html"
            f = open(curdir + sep + self.path)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f.read())
            f.close()

        if self.path == "/test":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("test")

        if self.path == "/train":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write("train")

            training = True

        if self.path == "/state":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(state)


def run():

    server = HTTPServer(("", PORT), CameraHandler)
    thread = threading.Thread(target = server.serve_forever)
    # thread.daemon = True

    try:
        thread.start()
    except KeyboardInterrupt:
        server.shutdown()
        sys.exit(0)

    print ("Serving at port", PORT)