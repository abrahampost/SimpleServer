import server as Server

server = Server.Server(log_requests=True)

server.set_port(8080)

def hello(request):
    name = request["QueryParams"]["name"]
    if not name:
        name = "anonymous"
    return "Hello {}, thank you for coming to my website. This was a query param.".format(name)

server.post("/hello", hello)

server.listen()