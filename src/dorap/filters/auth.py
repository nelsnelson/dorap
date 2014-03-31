from pyrox import filtering, http
from chuckbox.log import get_logger

from ConfigParser import ConfigParser
from keystoneclient.v2_0.client import Client as KeystoneClient


"""
Configuration Example
---------------------

[auth.openstack.keystone]

service_tenant = tenant
service_user = user
password = password
keystone_url = http://127.0.0.1:35357/v2.0
"""

_LOG = get_logger(__name__)

_CONFIG_KEY = 'auth.openstack.keystone'

_CONFIG = ConfigParser()
_CONFIG.read("/etc/pyrox/keystone.conf")

AUTH_TENANT_ID = 'Auth-Tenant-ID'
X_AUTH_TOKEN = 'X-Auth-Token'


def _header_is_set(header):
    return header is not None and len(header.values) >= 1


def keystone_token_validator():
    """
    Factory method for token validation filters
    """
    service_user = _CONFIG.get(_CONFIG_KEY, 'service_user')
    service_tenant = _CONFIG.get(_CONFIG_KEY, 'service_tenant')
    password = _CONFIG.get(_CONFIG_KEY, 'password')
    auth_url = _CONFIG.get(_CONFIG_KEY, 'keystone_url')

    keystone_client = KeystoneClient(
        username=service_user,
        password=password,
        tenant_name=service_tenant,
        auth_url=auth_url)

    return KeystoneAuthFilter(keystone_client)


class KeystoneAuthFilter(filtering.HttpFilter):

    def __init__(self, keystone_client):
        self.client = keystone_client

    @filtering.handles_request_head
    def on_request_head(self, request_head):
        tenant_header = request_head.get_header(AUTH_TENANT_ID)
        token_header = request_head.get_header(X_AUTH_TOKEN)

        if _header_is_set(tenant_header) and _header_is_set(token_header):
            try:
                auth_result = self.client.authenticate(
                    token=token_header.values[0],
                    tenant_id=tenant_header.values[0])

                if auth_result is not False:
                    return filtering.next()
            except Exception as ex:
                _LOG.exception(ex)

        return filtering.reject()
