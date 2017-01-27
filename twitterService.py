from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from modules import celebs
from modules import celeb
from modules import users
from modules import user
from modules import json_reader_writer


class S(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            print('got GET request: ' + self.path)
            data = {}
            if self.path.startswith("/getCelebs"):
                try:
                    category = self.path.split("/")[2]
                except IndexError:
                    category = "Default"
                if json_reader_writer.is_category(category):
                    print(category)
                    time_difference = json_reader_writer.calculate_differences_between_datetime(json_reader_writer.read_from_times_with_categories("celebs_catergories", category))
                    print("Last updated json was " + str(time_difference/60) + ' hours ago')
                    if time_difference > 70:
                        json_reader_writer.update_time_by_key("celebs_categories", category)
                        data = celebs.celebs(category)
                        if data:
                            json_reader_writer.write_to_data_json("celebs", data, category)
                        else:
                            data = json_reader_writer.read_from_data_json("celebs", category)
                    else:
                        data = json_reader_writer.read_from_data_json("celebs", category)
                else:
                    data = {'error': "wrong category"}
            elif self.path.startswith("/celeb"):
                name = ''
                category = ''
                try:
                    if self.path.split("/")[2] is not None and self.path.split("/")[3] is not None:
                        name = self.path.split("/")[2]
                        category = self.path.split("/")[3]
                except IndexError:
                    name = self.path.split("/")[2]
                    category = "Default"
                data = celeb.celeb_tweets(name, category)
                if not data:
                    data = {'error': 'wrong category'}
            elif self.path == "/getUsers":
                time_difference = json_reader_writer.calculate_differences_between_datetime(json_reader_writer.read_from_times_json("users_time"))
                if time_difference > 1440:
                    json_reader_writer.update_time_by_key("users_time")
                    data = users.get_users()
                    if data:
                        json_reader_writer.write_to_data_json("users", data)
                    else:
                        data = json_reader_writer.read_from_data_json("users")
                else:
                    data = json_reader_writer.read_from_data_json("users")
            elif self.path.startswith("/user/"):
                if self.path.split("/")[2] is not None:
                    name = self.path.split("/")[2]
                    data = user.get_user(name)
                if not data:
                    data = {'error': 'Wrong user name'}
            elif self.path == "/favicon.ico":
                print("favicon.ico")
            else:
                data = {'error': 'Wrong path: ' + self.path, "API": "https://github.com/MusicGindos/XISA-TwitterAPI"}
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))
        except Exception as e:
            print('Exception in do_get error message:' + str(e))
            data = {'error': 'Error in server'}
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))


def run(server_class=HTTPServer, handler_class=S, port=8080):
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
