import uuid
from atomic import AtomicLong

_C_ID = "_cid"
_OP_ID = "_opid"
_DEFAULT_TIMEOUT = 60 * 1000


class FContext(object):
    """FContext is the message context for a frugal message."""

    _NEXT_OP_ID = AtomicLong(0)

    def __init__(self, correlation_id=""):
        if (correlation_id == ""):
            self._correlation_id = self._generate_cid()
        else:
            self._correlation_id = correlation_id

        self._request_headers = {}
        self._response_headers = {}

        self._request_headers[_C_ID] = correlation_id
        self._NEXT_OP_ID += 1
        self._request_headers[_OP_ID] = str(self._NEXT_OP_ID.value)

    def get_correlation_id(self):
        return self._correlation_id

    def get_op_id(self):
        return self._request_headers[_OP_ID]

    def _generate_cid(self):
        return str(uuid.uuid4()).replace('-', '')

    def get_request_header(self, key):
        return self._request_headers[key]

    def put_request_header(self, key, value):
        self._request_headers[key] = value

    def get_response_header(self, key):
        return self._response_headers[key]

    def put_response_header(self, key, value):
        self._response_headers[key] = value
