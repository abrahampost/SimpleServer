import socket
import sys
import json

import handlers.request_parser as request_parser
import handlers.response_handler as response_handler
import handlers.Router as Router

# TODO: Add interceptor ability
# TODO: Add ability for subrouters
class Server:
    """This file is the actual server we are using to register routes"""
    def __init__(self, log_requests=False, log_responses=False):
        self.port_num = None
        self.socket = None
        self.router = Router.Router()
        self.log_requests = log_requests
        self.log_responses = log_responses
    
    def set_port(self, port=8080):
        self.port_num = port

    def route(self, request_type, route, function):
        self.router.register_route(request_type, route, function)
    
    def listen(self):
        if self.port_num == None:
            print("ERROR -- no port set. Set with .set_port(<port_num>)")
            sys.exit(1)
        print("Server starting on port {}".format(self.port_num))
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("", self.port_num))
            self.socket.listen(1)
        except socket.error:
            print("Unable to bind to socket. exiting...")
            sys.exit(1)
        
        while True:
            conn, addr = self.socket.accept()
            request_raw = conn.recv(1024).decode()
            if request_raw == "":
                continue
            request_parsed = request_parser.parse(request_raw)
            response = self.router.handle_request(request_parsed) #make_response("", code=200, response_type="application/json")
            if self.log_requests:
                print(request_parsed)
            if self.log_responses:
                print("\n" + response)
            conn.send(response.encode())
            conn.close()
        self.socket.close()
    
    def get(self, route, function):
        self.router.register_route("get", route, function)
    
    def post(self, route, function):
        self.router.register_route("post", route, function)
    
    def put(self, route, function):
        self.router.register_route("put", route, function)
    
    def patch(self, route, function):
       self.router.register_route("patch", route, function)
    
    def delete(self, route, function):
        self.router.register_route("delete", route, function)
    
    @staticmethod
    def read_file(file_name):
        with open(file_name, "r") as file:
            return file.read()


if __name__ == "__main__":
    server = Server(log_requests=True, log_responses=True)
    server.set_port()
    print(server.read_file("test.py"))
    server.listen()
