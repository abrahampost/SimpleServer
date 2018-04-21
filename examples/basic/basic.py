import sys
sys.path.append('../')
for p in sys.path:
    print(p)
from server import Server

server = Server(log_requests=True)

server.set_port(8080)

def basic(request):
    res = "Hello, world!"
    return res, "text/html"

server.get("/hello", basic)

server.listen()