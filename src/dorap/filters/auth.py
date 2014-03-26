from pyrox import filtering
from chuckbox.log import get_logger

_LOG = get_logger(__name__)


class AuthFilter(filtering.HttpFilter):

    @filtering.handles_request_head
    def on_request_head(self, request_head):
        _LOG.info('Got request head with verb: {}'.format(request_head.method))

    @filtering.handles_response_head
    def on_response_head(self, response_head):
        _LOG.info('Got response head with status: {}'.format(response_head.status))
