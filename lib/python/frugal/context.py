

class TimeoutError(Exception):
    """Indicats the Request has timed out"""
    pass


class Context:
    C_ID = "_cid"
    OP_ID = "_opid"
    DEFAULT_TIMEOUT = ""

    request_headers = {}
    response_headers = {}

    def __init__(self, correlation_id=""):
        self.correlation_id = correlation_id

        if (self.correlation_id == ""):
            self.correlation_id = self.generate_cid()

        self.request_headers[self.C_ID] = correlation_id
        # request_headers[OP_ID] = "12345"

    def generate_cid(self):
        return "12345"

