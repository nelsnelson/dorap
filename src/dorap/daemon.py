import os
import sys
import time
import errno
import signal
import psutil
import multiprocessing

from chuckbox.log import get_logger, get_log_manager


_LOG = get_logger(__name__)
_active_children_pids = list()


def _live_pids(pids):
    live = []

    if len(pids) > 0:
        for pid in pids:
            if psutil.pid_exists(pid):
                live.append(pid)
    return live


def stop_parent(signum, frame):
    global _active_children_pids

    still_alive = _live_pids(_active_children_pids)

    if len(still_alive) > 0:
        for pid in still_alive:
            os.kill(pid, signal.SIGINT)

        _LOG.info('Waiting for children to clean up...')


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

    # Global var for child pids
    global _active_children_pids

    # Spin a process for each mount
#    for mount_config in configuration['mounts']:
#        pid = os.fork()
#
#        if pid == 0:
#            _LOG.info('Starting process {pid}'.format(pid=pid))
            # START PROCESS HOOK
#            sys.exit(0)
#        else:
#            _active_children_pids.append(pid)

    _LOG.info('Your plugin was started and exited! The daemon hooks are not quite there yet :)')

    # Take over SIGTERM and SIGINT
    signal.signal(signal.SIGTERM, stop_parent)
    signal.signal(signal.SIGINT, stop_parent)

    # Wait for the children to retire
    while len(_active_children_pids) > 0:
        try:
            pid, status = os.wait()
        except OSError as oserr:
            if oserr.errno != errno.EINTR:
                _LOG.exception(oserr)
            continue
        except Exception as ex:
            _LOG.exception(ex)
            continue

        _LOG.info('Child process {} exited with status {}'.format(
            pid, status))
        _active_children_pids.remove(pid)
