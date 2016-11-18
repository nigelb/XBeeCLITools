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

import serial
from xbee import ZigBee

from xbeecli.cli import create_base_arg_parser, get_config


def send_remote_at_command():
    p = create_base_arg_parser()

    args = p.parse_args()
    configuration = get_config(args)


    ser = serial.Serial(configuration.port, configuration.baud,
                        timeout=configuration.timeout,
                        parity=configuration.parity,
                        stopbits=configuration.stop_bits
                        )

    radio = ZigBee(ser, escaped=True)

