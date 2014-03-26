import os
import sys
import time
import errno
import signal
import psutil
import multiprocessing

from chuckbox.log import get_logger, get_log_manager

from pyrox.server.daemon import start_pyrox
from pyrox.util.config import load_config, ConfigurationError

_LOG = get_logger(__name__)


def load_pyrox_config(upstream_host, location='/etc/pyrox/pyrox.conf'):
    defaults = {
        'routing': {
            'upstream_hosts': upstream_host
        }
    }

    return load_config('pyrox.server.config', location, defaults)


def start(args):
    # Init logging
    if not args.wants_quiet:
        log_level = 'DEBUG' if args.wants_debug else 'INFO'

        get_log_manager().configure({
            'level': log_level,
            'console_enabled': True})

    # Let the user know we're in debug mode
    if args.wants_debug:
        _LOG.debug('Debug mode enabled.')

    # Start Pyrox
    start_pyrox(cfg=load_pyrox_config(args.upstream_host))
