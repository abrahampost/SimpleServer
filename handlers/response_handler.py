import json

default_responses = {
    "100": "Continue",
    "101": "Switching Protocols",
    "200": "OK",
    "201": "Created",
    "202": "Accepted",
    "203": "Non-Authoritative Information",
    "204": "No Content",
    "205": "Reset Content",
    "206": "Partial Content",
    "300": "Multiple Choices",
    "301": "Moved Permanently",
    "302": "Found",
    "303": "See Other",
    "304": "Not Modified",
    "305": "Use Proxy",
    "307": "Temporary Redirect",
    "400": "Bad Request",
    "401": "Unauthorized",
    "402": "Payment Required",
    "403": "Forbidden",
    "404": "Not Found",
    "405": "Method Not Allowed",
    "406": "Not Acceptable",
    "407": "Proxy Authentication Required",
    "408": "Request Time-out",
    "409": " Conflict",
    "410": " Gone",
    "411": " Length Required",
    "412": " Precondition Failed",
    "413": " Request Entity Too Large",
    "414": " Request-URI Too Large",
    "415": " Unsupported Media Type",
    "416": " Requested range not satisfiable",
    "417": " Expectation Failed",
    "500": "Internal Server Error",
    "501": "Not Implemented",
    "502": "Bad Gateway",
    "503": "Service Unavailable",
    "504": "Gateway Time-out",
    "505": "HTTP Version not supported"
}

def make_response(body, code=200, response_type="text/plain"):
    if body is None:
        body = ""
    if type(body) is dict:
        body = json.dumps(body)
    content_length = len(body)
    content_type = response_type
    response = get_response_header(code)
    response += "Content-Length: {}\r\nContent-Type: {}\r\n\r\n".format(content_length, content_type)
    response += body
    return response

def err_request():
    return get_response_header(400)

def get_response_header(code):
    if type(code) is int:
        code = str(code)
    return "HTTP/1.1 {} {}\r\n".format(code, default_responses[code])

def get_default_response(status_code):
    return make_response("", code=status_code)