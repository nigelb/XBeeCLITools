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
import struct
import time

from xbeecli.cli import create_base_arg_parser, get_config

packets = {}

def radio_callback(frame):
    global packets
    print frame
    del packets[frame['frame_id']]

def encode_paramater(at_command, paramater):
    if at_command == "PL":
        return struct.pack("B", int(paramater))

def send_at_command():
    global packets
    p = create_base_arg_parser()
    p.add_argument("at_command", type=str)
    p.add_argument("paramater", type=str, nargs='?', default=None)
    p.add_argument("--write", const=True, default=False, action='store_const', help="Send write (WR) AT command as well.")
    args = p.parse_args()
    configuration = get_config(args)


    ser = serial.Serial(configuration.port, configuration.baud,
                        timeout=configuration.timeout,
                        parity=configuration.parity,
                        stopbits=configuration.stop_bits
                        )

    radio = ZigBee(ser, escaped=True)


    radio._callback = radio_callback
    radio._thread_continue = True
    radio.setDaemon(True)
    radio.start()
    radio.send("at", command="AI", frame_id="\x11")
    packets["\x11"] = True
    if args.paramater is None:
        radio.send("at", command=args.at_command, frame_id="\x12")
        packets["\x12"] = True
    else:
        radio.send("at", command=args.at_command, frame_id="\x13", parameter=encode_paramater(args.at_command, args.paramater))
        packets["\x13"] = True
    if args.write:
        radio.send("at", command="WR", frame_id="\x14")
        packets["\x14"] = True


if __name__ == "__main__":
    global packets
    send_at_command()
    while len(packets) > 0:
        time.sleep(1)
