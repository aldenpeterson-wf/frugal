import uuid
from atomic import AtomicLong
from copy import copy

_C_ID = "_cid"
_OP_ID = "_opid"
_DEFAULT_TIMEOUT = 60 * 1000


class FContext(object):
    """FContext is the message context for a frugal message."""

    _NEXT_OP_ID = AtomicLong(0)

    def __init__(self, correlation_id=None):
        self._request_headers = {}
        self._response_headers = {}

        if not correlation_id:
            correlation_id = self._generate_cid()

        self._request_headers[_C_ID] = correlation_id
        self._NEXT_OP_ID += 1
        self._request_headers[_OP_ID] = str(self._NEXT_OP_ID.value)

    def get_correlation_id(self):
        return self._request_headers[_C_ID]

    def get_op_id(self):
        return self._request_headers[_OP_ID]

    def set_response_headers_op_id(self, op_id):
        self._response_headers[_OP_ID] = op_id

    def _generate_cid(self):
        return str(uuid.uuid4()).replace('-', '')

    def get_request_headers(self):
        return copy(self._request_headers)

    def get_request_header(self, key):
        return self._request_headers[key]

    def put_request_header(self, key, value):
        self._check_string(key)
        self._check_string(value)

        self._request_headers[key] = value

    def get_response_headers(self):
        return copy(self._response_headers)

    def get_response_header(self, key):
        return self._response_headers[key]

    def put_response_header(self, key, value):
        self._check_string(key)
        self._check_string(value)

        self._response_headers[key] = value

    def _check_string(self, string):
        if not isinstance(string, str):
            raise TypeError("Value should be a string.")
