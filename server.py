import os
import cgi
import time
import shutil
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'  # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8081  # Maybe set this to 9000.


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()

    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        f = open("index.html", "r+")
        html = f.read()
        html = html.format(s.path)
        s.wfile.write(html.encode('UTF-8'))

    def do_POST(s):
        """Respond to a POST request."""
        print("This was a POST request.")
        if s.path == '/stripe':
            s.deal_post_data()
            r= True
            info="a mers"
            print(r, info, "by: ", s.client_address)


    def deal_post_data(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'})

        self.send_response(200)
        self.end_headers()

        saved_fns = "csv/"

        fileitem = form["csv_file"]
        if fileitem.file:
            # It's an uploaded file; count lines
            linecount = 0
            while 1:
                line = fileitem.file.readline()
                print(line)
                if not line: break
                linecount = linecount + 1
            print(linecount)

    def save_file(self, file):
        outpath = os.path.join("csv", file.filename)
        with open(outpath, 'wb') as fout:
            shutil.copyfileobj(file.file, fout, 100000)


if __name__ == '__main__':
    server_class = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        server_class.serve_forever()
    except KeyboardInterrupt:
        pass
    server_class.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))
