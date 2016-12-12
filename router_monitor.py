# -*- coding: utf-8 -*-
__author__ = 'huafeng'
import logging
import os
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=os.path.join(PATH, 'router_monitor.log'),
                filemode='a')

from TP_LINK import TP_LINK
tp_link = TP_LINK(logging)
pwd = ''
ip_port = ''
tp_link.router_reboot(pwd, ip_port)