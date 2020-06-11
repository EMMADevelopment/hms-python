
class ApiCallError(Exception):
    def __init__(self, message, detail=None):
        Exception.__init__(self, message)
        self.detail = detail
