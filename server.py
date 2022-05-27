from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import random

from content_based_filtering import content_based_filtering
from sqlite import close, connect, create_table, insert_user, list_all, list_users, exist_user
from user_based_filtering import user_based_fitering

serverPort = 8080


class Server(SimpleHTTPRequestHandler):
    conn = connect("./db/test.db")

    def do_GET(self):
        if(self.path == "/list-all"):
            list = list_all(self.conn)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(list).encode("utf-8"))
        if(self.path == "/init-db"):
            create_table(self.conn)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
        if(self.path == "/create-user"):
            id = 0
            user = "user_" + str(id)
            while(len(exist_user(self.conn, user)) > 0):
                id = random.randint(0, 9999)
                user = "user_" + str(id)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(user).encode("utf-8"))
        if(self.path == "/users"):
            users = list_users(self.conn)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(users).encode("utf-8"))
        if(self.path == "/other"):
            items = content_based_filtering([], "item")
            # print(json.dumps(movies.values.tolist()))
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(items.values.tolist()).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        data_string = self.rfile.read(int(self.headers["Content-Length"]))
        data = json.loads(data_string)
        if(self.path == "/content-based"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            items = content_based_filtering(data["items"], data["item"])
            self.wfile.write(json.dumps(items.values.tolist()).encode("utf-8"))
        elif(self.path == "/user-based"):
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            insert_user(self.conn, data["user"], data["item"], data["rate"])
            items = user_based_fitering(self.conn, data["user"])
            self.wfile.write(json.dumps(items).encode("utf-8"))
        else:
            self.send_response(404)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        SimpleHTTPRequestHandler.end_headers(self)


if __name__ == "__main__":
    webServer = HTTPServer(("", serverPort), Server)
    print("Running at port: ", serverPort)

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    close(webServer.conn)
    print("Server stopped.")
