from pyrox import filtering, http
from chuckbox.log import get_logger

_LOG = get_logger(__name__)


"""
Okay so this is the entry point for auth. Right now it doesn't really do
much except auto-reject all requests with a 401. More complex logic can be
inserted from here!
"""

class AuthFilter(filtering.HttpFilter):

    @filtering.handles_request_head
    def on_request_head(self, request_head):
        _LOG.info('Got request head with verb: {}'.format(request_head.method))


    @filtering.handles_response_head
    def on_response_head(self, response_head):
        _LOG.info('Got response head with status: {}'.format(response_head.status))

