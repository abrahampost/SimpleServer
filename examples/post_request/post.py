import server as Server

server = Server.Server(log_requests=True)

server.set_port(8080)

def hello(request):
    name = request["Body"]["name"]
    if not name:
        name = "anonymous"
    return "Hello {}, thank you for coming to my website. This was pulled from the post body.".format(name)

server.post("/hello", hello)

server.listen()