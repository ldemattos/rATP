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
    parser.add_argument("-p",help="server port (default 2207)",default=2207)
    args,unknown = parser.parse_known_args()

    print "Connecting to server...",
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((args.server,int(args.p)))
        print "OK"

        print "Reding ATP file...",
        try:
            atp_file = open(args.atp_file,'r')
            print "OK"

        except:
            print "ATP file not found!"
            sys.exit()

        print "Sending ATP file...",
        sock.sendall(args.atp_file)
        sock.sendall(atp_file.read())
        atp_file.close()
        print "OK"

        print "Waiting for the results...",
        fp_res = open('resultado.zip','wb+')
        while True:
            res_chunk = sock.recv(1024)
            if res_chunk:
                fp_res.write(bytearray(res_chunk))
            else:
                break

        fp_res.close()
        print "OK"

        # Close server connection
        sock.close()
    except:
        print "ERROR!"

    return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
