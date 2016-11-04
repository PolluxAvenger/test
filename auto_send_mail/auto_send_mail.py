#!/usr/bin/python
# -*- coding: UTF-8 -*-

import smtplib
import logging
import datetime
import email.MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.header import Header
import mimetypes
import os.path

ip_set = set()
def send_mail(file_name):
    logger = logging.getLogger('[hfs]')

    #content = get_content(date,ip_count,hfs_count)
    sender = u'hfs_scan@xxxx.com'

    receivers = ['xiaping_hu@xxxx.com']
    for line in open(file_name).readlines():
	ip_set.add(line.strip())
    ip_len = len(ip_set)
    main_msg = email.MIMEMultipart.MIMEMultipart()
    text_msg = MIMEText("threatexpert_ip numbert:  %s"%ip_len, 'plain', 'utf-8')
    main_msg.attach(text_msg)
    data = open(file_name, 'rb')
    ctype,encoding = mimetypes.guess_type(file_name)
    if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
    maintype,subtype = ctype.split('/',1)
    file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close(  )
    email.Encoders.encode_base64(file_msg)
    basename = os.path.basename(file_name)
    file_msg.add_header('Content-Disposition','attachment', filename = basename)#修改邮件头
    main_msg.attach(file_msg)

    main_msg['From'] = Header("threatexpert_scan@xxx.com")
    main_msg['To'] =  Header('xiaping_hu@xxxx.com')


    subject = 'Threatexpert Scan Result'
    main_msg['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('localhost')
        smtpObj.sendmail(sender, receivers, main_msg.as_string())
        logger.info('the mail send success')
    except smtplib.SMTPException as e:
	print e
        logger.info('the mail send failed')



if __name__ == '__main__':
    str_time = datetime.datetime.today().strftime("%Y%m%d")
    file_name = '/home/sunys/threatexpert_get_hfs_ip/lastweek_threatexpert_ip' + str_time + '.txt'
    send_mail(file_name)
