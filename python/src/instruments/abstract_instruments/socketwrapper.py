#!/usr/bin/python
# -*- coding: utf-8 -*-
##
# socketwrapper.py: Wraps sockets into a filelike object.
##
# © 2013 Chris Granade (cgranade@cgranade.com).
#
# This file is a part of the GPIBUSB adapter project.
# Licensed under the AGPL version 3.
##
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
##
##

## IMPORTS #####################################################################

import io

## CLASSES #####################################################################

class SocketWrapper(io.IOBase):
    """
    Wraps a socket to make it look like a `file`. Note that this is used instead
    of `socket.makefile`, as that method does not support timeouts. We do not
    support all features of `file`-like objects here, but enough to make
    `~instrument.Instrument` happy.
    """
    
    def __init__(self, conn):
        self._conn = conn
        
    def __repr__(self):
        return "<SocketWrapper object at 0x{:X} "\
                "connected to {}>".format(id(self), self._conn.getpeername())
        
    def close(self):
        try:
            self._conn.shutdown()
        finally:
            self._conn.close()
        
    def read(self, size):
        return self._conn.recv(size)
        
    def write(self, string):
        self._conn.sendall(string)
        
    def seek(self, offset):
        return NotImplemented
        
    def tell(self):
        return NotImplemented
