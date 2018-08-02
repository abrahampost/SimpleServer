import json

class BadCharacter(Exception):
    #Error raised when there is an invalid character in a request
    pass

def parse(request_raw):
    request = {}
    (headers, body) = seperate_body(request_raw)
    parse_headers(request, headers)
    parse_body(request, body)
    return request

def seperate_body(request_raw):
    split_request = request_raw.split("\r\n\r\n")
    if len(split_request) == 1:
        return (request_raw, None)
    elif len(split_request) == 2:
        return (split_request[0], split_request[1])
    else:
        return (split_request[0], "".join(split_request[1:]))

def parse_headers(request, headers):
    split_headers = headers.split("\r\n")
    http_info = split_headers[0].split(" ")
    request_type = http_info[0]
    route = None
    query_params = {}
    if '?' in http_info[1]:
        route = http_info[1].split("?")[0]
        query = http_info[1].split("?")[1]
        for param in query.split("&"):
            try:
                key, value = param.split("=")
                if not value.isalnum():
                    raise BadCharacter()
                query_params[key] =  value
            except Exception:
                continue
    else:
        route = http_info[1]

    http_version = http_info[2]
    request["RequestType"] = request_type
    request["Route"] = route
    request["HTTPVersion"] = http_version
    request["QueryParams"] = query_params
    parse_header_fields(request, split_headers[1:])

def parse_header_fields(request, fields):
    split_fields = [x.split(":") for x in fields]
    for field in split_fields:
        request[field[0].strip()] = field[1][1:]


def parse_body(request, body):
    if not body:
        return
    try:
        if request["Content-Type"] == "application/json":
            try:
                parsed_body = json.loads(body)
                request["Body"] = parsed_body
            except Exception:
                raise KeyError()
        else:
            request["Body"] = body
    except KeyError:
        request["Body"] = "Unable to parse body"