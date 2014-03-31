import re
import unittest

import pyrox.http as http
import pyrox.filtering as filtering

from mock import MagicMock
from dorap.filters.auth import KeystoneAuthFilter


class WhenAuthenticatingRequests(unittest.TestCase):

    def setUp(self):
        self.client = MagicMock()

        self.client.authenticate.side_effect = lambda token, tenant_id: {
            '12345': True,
            '22222': False
        }.get(token)

        self.request = MagicMock()
        self.request.url = '/v1/tenant/resource'
        self.keystone_filer = KeystoneAuthFilter(self.client)

        self.auth_tenant_header = http.HttpHeader('Auth-Tenant-ID')
        self.auth_tenant_header.values.append('tenant')

        self.auth_token_header = http.HttpHeader('X-Auth-Token')
        self.auth_token_header.values.append('12345')

        self.headers = {
            'X-Auth-Token': self.auth_token_header,
            'Auth-Tenant-ID': self.auth_tenant_header
        }

        self.request.get_header.side_effect = lambda x: self.headers.get(x)

    def test_should_authenticate_good_requests(self):
        action = self.keystone_filer.on_request_head(self.request)

        self.assertTrue(action.kind == filtering.pipeline.NEXT_FILTER)

    def test_should_reject_requests_without_id(self):
        del self.headers['Auth-Tenant-ID']
        action = self.keystone_filer.on_request_head(self.request)

        self.assertTrue(action.kind == filtering.pipeline.REJECT)

    def test_should_reject_requests_without_auth_token(self):
        del self.headers['X-Auth-Token']
        action = self.keystone_filer.on_request_head(self.request)

        self.assertTrue(action.kind == filtering.pipeline.REJECT)

    def test_should_reject_requests_with_invalid_auth_token(self):
        del self.auth_token_header.values[:]
        self.auth_token_header.values.append('22222')
        action = self.keystone_filer.on_request_head(self.request)

        self.assertTrue(action.kind == filtering.pipeline.REJECT)
