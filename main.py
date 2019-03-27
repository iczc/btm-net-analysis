#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import getopt
import logging
import sys


assert sys.version_info >= (3, 6, 0), 'btm-net-analysis requires Python 3.6+'  # check Python version

def parse_args(argv):
    try:
        opts, args = getopt.getopt(argv, 'hb:t:', ['help', 'block=', 'transaction='])
    except getopt.GetoptError as err:
        logging.error('%s', str(err))

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('help')
        elif opt in ('-b', '--block'):
            print('block')
        elif opt in ('-t', '--transaction'):
            print('transaction')
        else:
            logging.error('unhandled option')
            sys.exit()


if __name__ == '__main__':
    parse_args(sys.argv[1:])