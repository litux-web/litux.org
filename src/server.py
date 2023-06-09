# Python 3 server example
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import re

# ROOT = "docs"
hostName = ""  # "localhost"
serverPort = 80

csp = """
frame-ancestors 'none'; base-uri 'self'; default-src 'self';
style-src 'self'
'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU='
'sha256-S7JeKectYc6cbuYmMu0sGEb2ApwTg7MEiY1vjaaiCyQ='
'sha256-MpoKUwOK6CzOmKMt8YdxFGobEFY32yQh8qiDEPgaz2w='
'sha256-MiFtFjQ2fIMLg4oJ4xqXP5BJNMsImIZ/Gd/s9UwISEs='
'sha256-fiOwm2C2XBdD65LEz2htmvpmCsnubAoSdDtB43Mkavw='
'sha256-+46x8lShh4s8u2L5RA+bTmi0jpo+d+ST4IgK6wLmgAQ='
'sha256-OWmlaHRCxu2ZM+W0u5jqZQSTcBEjgGgZRtRunVnMBGs='
'sha256-3QbC6ukBrWKUr9CA9uuyPEBix8bCjn5jMeDC0cfkR7o='
;
script-src 'strict-dynamic' 'self'
'sha256-OpxdHpKUnEk+HfoX1DDFde4L5T65QoFewIp9NrLMnV0='
'nonce-OpxdHpKUnEk+HfoX1DDFde4L5T65QoFewIp9NrLMnV0='
https://www.freeprivacypolicy.com/public/cookie-consent/4.1.0/cookie-consent.js
'sha256-OGDE6f5pho6o70mPjWpfPov6nl3FHTfBN3LrUHmtWjU='
'nonce-OGDE6f5pho6o70mPjWpfPov6nl3FHTfBN3LrUHmtWjU='
https://www.googletagmanager.com/gtag/js
'sha256-KAuo7kiq40bnRDQySsvQQx5/t5mnjm2bwP06UGXcb3o='
'nonce-KAuo7kiq40bnRDQySsvQQx5/t5mnjm2bwP06UGXcb3o='
;
frame-src
https://disqus.com/embed/comments/
;
connect-src 'self'
https://www.google.com/ads/ga-audiences
https://www.google.pt/ads/ga-audiences
https://*.analytics.google.com/g/collect
https://*.analytics.google.pt/g/collect
https://*.google-analytics.com/g/collect
https://stats.g.doubleclick.net/g/collect
https://geo.privacymanager.io/
;
img-src 'self'
https://www.googletagmanager.com
https://www.google.com/ads/ga-audiences
https://www.google.pt/ads/ga-audiences
https://*.analytics.google.com/g/collect
https://*.analytics.google.pt/g/collect
https://*.disqus.com/juggler/
https://*.disquscdn.com/next/embed/assets/img/
;
font-src 'self';
worker-src 'self'; media-src 'self'; object-src 'none'; form-action 'none';
report-uri https://www.litux.org/_/csp; report-to csp;
"""
csp = re.sub(r"\s+", " ", csp).strip()
print(csp)


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
        global csp
        self.send_header("Content-Security-Policy", csp)
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
