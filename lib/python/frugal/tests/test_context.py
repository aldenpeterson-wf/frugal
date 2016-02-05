import unittest
from mock import patch

from frugal.context import Context


class TestContext(unittest.TestCase):

    correlation_id = "fooid"

    def test_correlation_id(self):
        context = Context(self.correlation_id)
        self.assertEqual(self.correlation_id, context.correlation_id)

    @patch('uuid.uuid4')
    def test_empty_correlation_id(self, mock_uuid):
        mock_uuid.return_value = "12345"

        context = Context()
        self.assertEqual("12345", context.correlation_id)

    def test_op_id(self):
        context = Context(self.correlation_id)
        context.request_headers['_opid'] = "12345"
        self.assertEqual(self.correlation_id, context.correlation_id)
        self.assertEqual("12345", context.request_headers['_opid'])

    def test_request_header(self):
        context = Context(self.correlation_id)
        context.request_headers['foo'] = "bar"
        self.assertEqual("bar", context.request_headers['foo'])
        self.assertEqual(self.correlation_id, context.request_headers['_cid'])

    def test_response_header(self):
        context = Context(self.correlation_id)
        context.response_headers['foo'] = "bar"
        self.assertEqual("bar", context.response_headers['foo'])
        self.assertEqual(self.correlation_id, context.request_headers['_cid'])

