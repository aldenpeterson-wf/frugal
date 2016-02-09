import unittest
from mock import patch

from frugal.context import FContext


class TestContext(unittest.TestCase):

    correlation_id = "fooid"

    def test_correlation_id(self):
        context = FContext("fooid")
        self.assertEqual("fooid", context.get_correlation_id())

    @patch('uuid.uuid4')
    def test_empty_correlation_id(self, mock_uuid):
        mock_uuid.return_value = "12345"

        context = FContext()
        self.assertEqual("12345", context.get_correlation_id())

    def test_op_id(self):
        context = FContext(self.correlation_id)
        context.put_request_header("_opid", "12345")
        self.assertEqual(self.correlation_id, context.get_correlation_id())
        self.assertEqual("12345", context.get_request_header("_opid"))

    def test_request_header(self):
        context = FContext(self.correlation_id)
        context.put_request_header("foo", "bar")
        self.assertEqual("bar", context.get_request_header("foo"))
        self.assertEqual(self.correlation_id,
                         context.get_request_header("_cid"))

    def test_response_header(self):
        context = FContext(self.correlation_id)
        context.put_response_header("foo", "bar")
        self.assertEqual("bar", context.get_response_header("foo"))
        self.assertEqual(self.correlation_id,
                         context.get_request_header("_cid"))

