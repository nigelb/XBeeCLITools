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

import time
import serial
import struct
from xbee import ZigBee

from xbeecli.cli import create_base_arg_parser, get_config


def network_discover():
    p = create_base_arg_parser()

    args = p.parse_args()
    configuration = get_config(args)


    ser = serial.Serial(configuration.port, configuration.baud,
                        timeout=configuration.timeout,
                        parity=configuration.parity,
                        stopbits=configuration.stop_bits
                        )

    radio = ZigBee(ser, escaped=True)

    radios = {}
    sleep_time = None

    def radio_callback(frame):

        if frame['frame_id'] == '\x02':
            global sleep_time
            sleep_time = struct.unpack(">H", frame['parameter'])[0] * 100
            print sleep_time
        if frame['frame_id'] == '\x03':
            if frame['parameter']['source_addr_long'] not in radios:
                radios[frame['parameter']['source_addr_long']] = ""
                print "Found Radio: %s"%" ".join([format(ord(x), "02x") for x in frame['parameter']['source_addr_long']])
        # else:
        #     print frame

    radio._callback = radio_callback
    radio._thread_continue = True
    radio.setDaemon(True)
    radio.start()
    radio.send("at", command="AI", frame_id="\x01")
    radio.send("at", command="NT", frame_id="\x02")
    radio.send("at", command="ND", frame_id="\x03")

    while True:
        if sleep_time is None:
            time.sleep(1)
        else:
            time.sleep(float(sleep_time)/1000)
            print "Searching again..."
            radio.send("at", command="ND", frame_id="\x03")

if __name__ == "__main__":
    network_discover()
