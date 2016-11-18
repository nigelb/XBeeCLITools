#XBeeCLITools provides a number of XBee configuration and diagnostic utilities.
#Copyright (C) 2016  NigelB
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os, json
from argparse import ArgumentParser

import serial

config_file='config_file'
baud='baud'
port='port'
parity='parity'
stop_bits='stop_bits'
timeout='timeout'

def create_base_arg_parser():
    argParse = ArgumentParser(description="XBee CLI Tool ")
    argParse.add_argument("--config-file",metavar="<config_file>", dest="config_file", default="~/.config/xbeecli.conf", action="store", help="The location of the config directory, file: ~/.config/xbeecli.conf")
    argParse.add_argument("--baud",metavar="<baud>", dest="baud", action="store", help="The baud rate for the XBee Module, default: 9600")
    argParse.add_argument("--port",metavar="<port>", dest="port", action="store", help="The port for the XBee Module, default: /dev/ttyUSB0")
    argParse.add_argument("--parity",metavar="<parity>", dest="parity", action="store", help="The parity for the XBee Module, default: PARITY_NONE. Values are PARITY_NONE, PARITY_EVEN, PARITY_ODD, PARITY_MARK, PARITY_SPACE = 'N', 'E', 'O', 'M', 'S'")
    argParse.add_argument("--stop-bits",metavar="<stop_bits>", dest="stop_bits", action="store", help="The stop bits for the XBee Module, default: 1")
    argParse.add_argument("--timeout",metavar="<timeout>", dest="timeout", action="store", help="The timeout for the XBee Module, default: 1")
    return argParse

def get_config(args):
    args.config_file = os.path.expanduser(args.config_file)

    if os.path.exists(args.config_file):
        with open(args.config_file, 'rb') as config:
            cfg = json.load(config)
            print cfg
            for key in cfg:
                if key not in args or getattr(args, key) is None:
                    args.__setattr__(key, cfg[key])

    else:

        if baud not in args or args.baud is None:
            args.baud = 9600
        if port not in args or args.port is None:
            args.port = '/dev/ttyUSB0'
        if parity not in args or args.parity is None:
            args.parity = serial.PARITY_NONE
        if stop_bits not in args or args.stop_bits is None:
            args.stop_bits = 1
        if timeout not in args or args.timeout is None:
            args.timeout = 1

        with open(args.config_file, 'wb') as config:
            json.dump(vars(args), config)
    print args
    return args
