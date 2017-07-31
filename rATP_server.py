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
import hashlib
import subprocess
import os
import shutil

def readChunks(fp, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = fp.read(chunk_size)
        if not data:
            break
        yield data

def main(args):

    # Read server conf file
    print "Reading file server...",
    parser = SafeConfigParser()
    parser.read('server.conf')
    print "OK"

    # Server settings
    print "Binding port...",
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server = (parser.get('main', 'address'),int(parser.get('main', 'port')))
    sock.bind(server)
    sock.listen(int(parser.get('main', 'max_conn')))
    print "OK"

    # Initialize server
    print "Initializing server and for connection...",
    connection, address_client = sock.accept()
    print "CONNECTED!"
    try:
        print "Receiving ATP file...",
        atp_file_name = os.path.basename(connection.recv(1024))
        atp_file = connection.recv(1024)
        atp_hash = hashlib.md5(atp_file).hexdigest()
        print "OK"

        print "Write ATP file to disk...",
        atp_root = parser.get('ATP', 'workdir') + atp_hash +'/'
        cmd = 'mkdir '+atp_root
        subprocess.call(cmd,shell=True)
        try:
            fp_atp = open(atp_root+atp_file_name,'w+')
            fp_atp.write("%s"%(atp_file))
            fp_atp.close()
            print "OK"

        except:
            print "ERROR"

        print "Processing ATP data case...",
        cmd = 'cd '+atp_root+'; '+parser.get('ATP', 'exec')+' '+atp_file_name
        subprocess.call(cmd,shell=True)
        print "OK"

        print "Compressing results...",
        shutil.make_archive(parser.get('ATP', 'workdir')+'/'+atp_hash, 'zip', parser.get('ATP', 'workdir'), base_dir=atp_hash)
        print "OK"

        print "Sending back the results...",
        res_file = parser.get('ATP', 'workdir')+'/'+atp_hash+'.zip'
        fp_res = open(res_file,'rb')
        for chunk in readChunks(fp_res):
            connection.sendall(chunk)

        fp_res.close()
        print "OK"

        # print "Cleaning cache...",
        # cmd = 'rm -rf '+atp_root+'; rm -f '+atp_root[0:-1]+'.zip'
        # subprocess.call(cmd,shell=True)
        # print "OK"

        print "EOL"

    finally:
        connection.close()

    return(0)

if __name__ == '__main__':
	import sys
	sys.exit(main(sys.argv))
