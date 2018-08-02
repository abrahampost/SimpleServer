import sys
sys.path.append('../../')
import server

server = server.Server(log_requests=True)

server.set_port(8080)

def return_page(request):
    res = """
    <html>
        <h1>Wow, this response was parsed correctly and sent as html!</h1>
        <ul>
            <li>list element</li>
        </ul>
    </html>"""
    return res, 200, "text/html"

def load_html(request):
    res = server.read_file("serve.html")
    print(res)
    return res, "text/html"

server.get("/", return_page)
server.get("/hello", load_html)

server.listen()