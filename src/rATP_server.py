#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rATP_server.py
#
# Copyright (C) 2017 Leonardo M. N. de Mattos <l@mattos.eng.br>
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
from ConfigParser import SafeConfigParser
from srv_routines import srvWorker
# from multiprocessing import Process

def main(args):

    # Read server conf file
    print "Reading file server...",
    parser = SafeConfigParser()
    parser.read('server.conf')
    address = parser.get('main', 'address')
    port = int(parser.get('main', 'port'))
    max_conn = int(parser.get('main', 'max_conn'))
    workdir = parser.get('ATP', 'workdir')
    atp_exec = parser.get('ATP', 'exec')
    print "OK"

    # Server settings
    print "Binding port...",
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (address,port)
    sock.bind(server)
    sock.listen(max_conn)
    print "OK"

    # Initialize server
    print "Initializing server and waiting for clients...",
    while True:

        # Connect to new client
        connection, address_client = sock.accept()
        srvWorker(connection,workdir,atp_exec)

        # Launch thread to deal with the new client
        # worker = Process(target=srvWorker, args=(connection,workdir,atp_exec))
        # worker.start()

        print "CONNECTED!"

    # Finish server
    sock.close()

    return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
