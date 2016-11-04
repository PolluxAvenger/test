#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: sharpsec
# @Date:   2016-11-01 09:51:22
# @Last Modified by:   sharpsec
# @Last Modified time: 2016-11-03 11:09:26
import pyshark
import sys
import datetime
import os
import hashlib
import binascii
reload(sys)
sys.setdefaultencoding('utf-8')


def extra_cert(p):

    cer = str(p['ssl'].handshake_certificate).replace(':','')
    cer = binascii.a2b_hex(cer)
    md5cert = hashlib.md5(cer).hexdigest()
    cer_name = p['ip'].src_host + '_' +  md5cert
    #print cer_name
    with open('cer\\'+ cer_name + '.cer', 'wb') as f:
        f.write(cer)
if __name__ == '__main__':
    info = "pcap"
    begin_time = datetime.datetime.now()
    for root, dirs, files in os.walk(info):
        if len(dirs) == 0:
            for fl in files:
                info = "%s\%s" % (root, fl)
                cap = pyshark.FileCapture(info)
                for p in cap:
                    if p.highest_layer == "SSL":
                        try:
                            if p['ssl'].handshake == "Handshake Protocol: Certificate" or p['ssl'].handshake == "Handshake Protocol: Server Hello":
                                #print info
                                extra_cert(p)
                        except Exception,e:
                            continue

    end_time = datetime.datetime.now()
    print "alltime: %s"%(end_time-begin_time)