import uuid


_C_ID = "_cid"
_OP_ID = "_opid"
_DEFAULT_TIMEOUT = ""


class FContext(object):
    """FContext is the message context for a frugal message."""

    def __init__(self, correlation_id=""):
        if (correlation_id == ""):
            self._correlation_id = self._generate_cid()
        else:
            self._correlation_id = correlation_id

        self._request_headers = {}
        self._response_headers = {}

        self._request_headers[_C_ID] = correlation_id
        # request_headers[OP_ID] = "12345"

    def get_correlation_id(self):
        return self._correlation_id

    def _generate_cid(self):
        return str(uuid.uuid4()).replace('-', '')

    def get_request_headers(self):
        return self._request_headers

    def get_response_headers(self):
        return self._response_headers
