class LoginException(Exception):
    def __init__(self, apikey, userkey, username):
        super().__init__("Login error")
        self.apikey = apikey
        self.userkey = userkey
        self.username = username

class AuthorizationError(Exception):
    def __init__(self, message=None, route=None):
        super().__init__("Authorization error: {}".format(route))
        self.message = message
        self.route = route
        
class UnknownResponseException(Exception):
    def __init__(self, response):
        super().__init__("Unknown response")
        self.response = response
    
    def __str__(self):
        return f"UnknownResponse(status={self.response.status_code})"
    
    def __repr__(self):
        return self.__str__()