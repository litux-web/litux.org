# Python 3 server example
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import re

# ROOT = "docs"
hostName = ""  # "localhost"
serverPort = 80


def get_csp():
    if os.path.exists("resources/csp.txt"):
        with open("resources/csp.txt", "r") as f:
            csp = "".join(f.readlines())
    else:
        raise Exception("Missing resources/csp.txt")

    csp = re.sub(r"\s+", " ", csp).strip()
    print(csp)
    return csp


class MyServer(SimpleHTTPRequestHandler):
    def __init__(self, request, client_address, server, directory="."):
        directory = "docs"  # ROOT
        SimpleHTTPRequestHandler.__init__(
            self,
            request=request,
            client_address=client_address,
            server=server,
            directory=directory,
        )

    def end_headers(self):
        self.send_header("Content-Security-Policy", get_csp())
        SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        file = self.path
        if "?" in file:
            file = file.split("?", 2)[0]
        if "#" in file:
            file = file.split("#", 2)[0]
        # print(file)
        if os.path.exists(f"docs{file}.html"):
            self.path = self.path.replace(file, file + ".html", 1)
        # print(self.path)
        SimpleHTTPRequestHandler.do_GET(self)

    pass


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
