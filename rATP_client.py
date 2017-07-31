#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  rATP_client.py
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

import argparse
import socket
import sys

def main(args):

    # Input arguments
    parser = argparse.ArgumentParser(description='rATP Client',prog='rATP')
    parser.add_argument("server",help="server address")
    parser.add_argument("atp_file",help="ATP File")
    parser.add_argument("-p",help="server port (default 10000)",default=10000)
    args,unknown = parser.parse_known_args()

    # Connecting to server
    print "Connecting to server...",
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((args.server,int(args.p)))
        print "OK"

        # Sending ATP file
        try:
            atp_file = open(args.atp_file,'r')
            sock.sendall(args.atp_file)
            sock.sendall(atp_file.read())
            
        except:
            print "ATP file not found!"
            sys.exit()

        # Close server connection
        sock.close()
    except:
        print "FAIL! Server not found!"

    return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
