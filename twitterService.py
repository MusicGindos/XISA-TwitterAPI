from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from modules import celebs
from modules import celeb
from modules import file_reader


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        print('got GET request: ' + self.path)
        data = {}
        if self.path == "/getCelebs":
            # time_diffrence = file_reader.calculate_differences_between_datetime(file_reader.read_from_times_json("celebs_time"))
            # if time_diffrence > 70:
            #     file_reader.update_time_by_key("celebs_time")
            #     data = celebs.celebs()
            #     file_reader.write_to_data_json("celebs", data)
            # else:
            #     data = file_reader.read_from_data_json("celebs")
            data = celebs.celebs()
        elif self.path.startswith("/celeb/"):
            name = self.path.split("/")[2]
            print(self.path.split("/")[2])
            data = celeb.celeb_tweets(name)

        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def run(server_class=HTTPServer,handler_class=S, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd... on port ' + str(port))
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(os.environ.get("PORT", 5000)))
    else:
        run()
