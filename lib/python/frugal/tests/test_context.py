import unittest

from frugal.context import Context


class TestContext(unittest.TestCase):

    def test_correlation_id(self):
        context = Context("fooid")
        self.assertEqual("fooid", context.correlation_id)

    def test_empty_correlation_id(self):
        context = Context()
        self.assertEqual("12345", context.correlation_id)

    def test_op_id(self):
        context = Context("fooid")
        context.request_headers['_opid'] = "12345"
        self.assertEqual("12345", context.request_headers['_opid'])

    def test_request_header(self):
        context = Context("fooid")
        context.request_headers['foo'] = "bar"
        self.assertEqual("bar", context.request_headers['foo'])
        self.assertEqual("fooid", context.request_headers['_cid'])

    def test_response_header(self):
        context = Context("fooid")
        context.response_headers['foo'] = "bar"
        self.assertEqual("bar", context.response_headers['foo'])
        self.assertEqual("fooid", context.request_headers['_cid'])

