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

import glob

from setuptools import setup, find_packages

setup(name='xbeecli',
      version='0.0.1',
      description='Provides a number of XBee configuration and diagnostic utilities.',
      author='NigelB',
      author_email='nigel.blair@gmail.com',
      packages=find_packages(),
      zip_safe=False,
      install_requires=["pyserial", "xbee"],
      entry_points={
          "console_scripts": [
              "network_discover = xbeecli.network_discover:network_discover",
              "send_remote_at = xbeecli.send_remote_at:send_remote_at",
              "send_at = xbeecli.send_at:send_at",
          ]
      },
)
