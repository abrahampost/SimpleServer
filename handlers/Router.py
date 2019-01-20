import handlers.response_handler as response_handler
import sys

class Router():
    def __init__(self):
        self.get = {}
        self.post = {}
        self.put = {}
        self.patch = {}
        self.delete = {}
    
    def register_route(self, request_type, route, function):
        if request_type.lower() == "get":
            self.get[route] = function
        elif request_type.lower() == "post":
            self.post[route] = function
        elif request_type.lower() == "put":
            self.put[route] = function
        elif request_type.lower() == "patch":
            self.patch[route] = function
        elif request_type.lower() == "delete":
            self.delete[route] = function
        else:
            print("Route type: {} not supported. Exiting...".format(request_type))
            sys.exit(1)
    
    def handle_request(self, request):
        """Takes a request, and parses it to find what type of route
        and what specific route a request is going to. It then returns an http
        response object based on what route it hit"""
        try:
            request_type = request["RequestType"]
            route = request["Route"]
        except Exception:
            return response_handler.get_default_response(500)
        response = None
        try:
            if request_type.lower() == "get":
                response = self.get[route](request)
            elif request_type.lower() == "post":
                response = self.post[route](request)
            elif request_type.lower() == "put":
                response = self.put[route](request)
            elif request_type.lower() == "patch":
                response = self.patch[route](request)
            elif request_type.lower() == "delete":
                response = self.delete[route](request)
            else:
                return response_handler.make_response("Request type: {} not supported".format(request_type.upper()), code=501)
            #after the response has been received
            # if it is a tuple, do some parsing to figure out what sort of data is returned
            #make it so that functions can return void, a number, a tuple of body and number
            if type(response) is tuple:
                if len(response) == 2:
                    if type(response[1]) is int:
                        return response_handler.make_response(response[0], code=response[1])
                    elif type(response[1]) is str:
                        return response_handler.make_response(response[0], response_type=response[1])
                    else:
                        raise Exception()
                if len(response) == 3:
                    if type(response[1]) is not int or type(response[2]) is not str:
                        raise Exception()
                    else:
                        return response_handler.make_response(response[0], code=response[1], response_type=response[2])
                else:
                    raise Exception()
            else:
                if type(response) is int:
                    return response_handler.make_response("", code=response)
                else:
                    return response_handler.make_response(response)
        except KeyError:
            #if it can't find something it is supposed to, it is a 404
            return response_handler.get_default_response(404)
        except Exception:
            #if something actually does throw an exception back up, default to a 500 server error
            return response_handler.get_default_response(500)