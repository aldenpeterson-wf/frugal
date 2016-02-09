
class FException(Exception):

    def __init__(self, message=None):
        Exception.__init__(self, message)
        self.message = message

