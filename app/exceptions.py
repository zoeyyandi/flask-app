# class ClientError(Exception):
#    status_code: int = None
#    message: str = ""

#    def __init__(self, message: str, status_code:int):
#       self.status_code = status_code
#       self.message = message 



# class NotFoundClientError(ClientError):
   
#    def __init__(self):
#       super(NotFoundClientError, self).__init__(message="Not Found", status_code=404)
      

# class BadRequesClientError(ClientError):
   
#    def __init__(self):
#       super(BadRequesClientError, self).__init__(message="Bad Request", status_code=400)
      

class ClientError(Exception):
   status_code: int = 500
   message: str = "INTERNAL_SERVER_ERROR"

   def __init__(self, message: str = None):
      if message is not None:
         self.message = message

   def to_json(self):
      return { "status_code": self.status_code, "message": self.message }

class NotFoundClientError(ClientError):
   status_code = 404
   message = "NOT_FOUND"

class BadRequestClientError(ClientError):
   status_code = 400
   message = "BAD_REQUEST"
