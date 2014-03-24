import os
import sys
import argparse

import chuckbox.project as project

import dorap.daemon as daemon


args_parser = argparse.ArgumentParser(
    prog='dorap',
    description='dorap: The Docker-Rackspace Plugin.')

args_parser.add_argument(
    '-v', '--version',
    dest='wants_version',
    action='store_true',
    default=False,
    help="""Prints the version.""")

args_parser.add_argument(
    '-d', '--debug',
    dest='wants_debug',
    action='store_true',
    default=False,
    help="""Enables debug output and code paths.""")

args_parser.add_argument(
    '-q', '--quiet',
    dest='wants_quiet',
    action='store_true',
    default=False,
    help="""
        Sets the logging output to quiet. This supercedes enabling the
        debug output switch.""")


if len(sys.argv) > 1:
    args = args_parser.parse_args()

    if args.wants_version:
        version = project.about('dorap').version
        print('dorap version: {}'.format(version))
    else:
        daemon.start(args)
else:
    args_parser.print_help()
