# -*- coding: utf-8 -*-
__author__ = 'huafeng'
import requests
import codecs
import os, re, time,PyV8, json
from bs4 import BeautifulSoup

PATH = os.path.dirname(os.path.abspath(__file__))
xiaomi_encrypt_js_file = os.path.join(PATH, 'xiaomi_encrypt.js')
encrypt_str = codecs.open(xiaomi_encrypt_js_file).read()

def get_login_param(pwd):
    '''加密并生成登录所需参数
    {'username': 'admin', 'logtype': 2, 'password': '0ed0b002bc6afde97b886c22262eac7d61b48120', 'nonce': '0_b8:27:eb:d7:f7:fd_1479780778_4924'}
    '''
    PyV8.JSExtension("u/javascript", encrypt_str)
    with PyV8.JSContext(extensions=['u/javascript']) as ctxt:
        js_ret = ctxt.eval('''encrypt_pwd("%s")'''%pwd)
        encrypt_param_dic = dict(js_ret)
    return encrypt_param_dic
# print get_login_param('@rong360')

def login_reboot(ip_port, login_param):
    '''登录并重启路由'''
    proxies = {
        'http':'http://%s'%ip_port
    }
    login_url = 'http://192.168.31.1/cgi-bin/luci/api/xqsystem/login'
    ss = requests.session()
    ss.proxies=proxies
    try:
        login_ret_content = ss.post(login_url, data=login_param, timeout=10, proxies=proxies).content
    #{u'url': u'/cgi-bin/luci/;stok=9a478fb85e855b2f4265e60ad9374aa0/web/home', u'token': u'9a478fb85e855b2f4265e60ad9374aa0', u'code': 0}
        login_info = json.loads(login_ret_content)
        if login_info.get('code') != 0:
            print 'login failed... %s' % ip_port
            return False
        print '%s, login sucess...' % ip_port
    except Exception, e:
        print 'login failed, connect timeout  %s'%ip_port
        return False
    #重启路由
    reboot_url = 'http://192.168.31.1/cgi-bin/luci/;stok=%s/api/xqsystem/reboot?client=web' %   login_info.get('token')
    try:
        reboot_res = ss.get(reboot_url, timeout=10).content#{"lanIp":[{"mask":"255.255.255.0","ip":"192.168.31.1"}],"code":0}
        reboot_json = json.loads(reboot_res)
        if reboot_json.get('code') != 0:
            print 'reboot failed... %s'%ip_port
        else:
            print 'reboot sucess... %s' %ip_port
    except Exception, e:
        print 'reboot failed, %s' %e

if __name__ == '__main__':
    ip_port = ''
    pwd = ''
    login_param = get_login_param(pwd)
    login_reboot(ip_port, login_param)