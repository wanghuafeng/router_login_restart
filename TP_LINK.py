# -*- coding: utf-8 -*-
__author__ = 'huafeng'
import requests
import codecs, logging
import os, re, time,PyV8, json
from bs4 import BeautifulSoup
encrypt_str= r'''
function utf8_encode (string)
{
	string = string.replace(/\r\n/g,"\n");
	var utftext = "";
	for (var n = 0; n < string.length; n++) {
		var c = string.charCodeAt(n);
		if (c < 128) {
			utftext += String.fromCharCode(c);
		}
		else if((c > 127) && (c < 2048)) {
			utftext += String.fromCharCode((c >> 6) | 192);
			utftext += String.fromCharCode((c & 63) | 128);
		}
		else {
			utftext += String.fromCharCode((c >> 12) | 224);
			utftext += String.fromCharCode(((c >> 6) & 63) | 128);
			utftext += String.fromCharCode((c & 63) | 128);
		}
	}
	return utftext;
}

function Base64Encoding(input)
{
	var keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
	var output = "";
	var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
	var i = 0;
	input = utf8_encode(input);
	while (i < input.length)
	{
		chr1 = input.charCodeAt(i++);
		chr2 = input.charCodeAt(i++);
		chr3 = input.charCodeAt(i++);
		enc1 = chr1 >> 2;
		enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
		enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
		enc4 = chr3 & 63;
		if (isNaN(chr2)) {
			enc3 = enc4 = 64;
		} else if (isNaN(chr3)) {
			enc4 = 64;
		}
		output = output +
		keyStr.charAt(enc1) + keyStr.charAt(enc2) +
		keyStr.charAt(enc3) + keyStr.charAt(enc4);

	}
	return output;
}
function get_cookie(password)
{
    var auth = "Basic "+Base64Encoding("admin:"+password);
    //cookie = "Authorization="+escape(auth)+";path=/";
    cookie = escape(auth);
    return cookie
}
'''
try:
    PATH = os.path.dirname(os.path.abspath(__file__))
except:
    PATH = os.getcwd()

class TP_LINK(object):

    def __init__(self, logging):
        self.logging = logging

    def get_login_param(self, pwd):
        self.logging.info('-----------------')
        exit()
        PyV8.JSExtension("u/javascript", encrypt_str)
        with PyV8.JSContext(extensions=['u/javascript']) as ctxt:
            js_ret = ctxt.eval('''get_cookie("%s")''' % pwd)
        return js_ret

    def login_reboot(self, ip_port, login_param):
        '''tp_link登录并重启，此处登录并非必须完成，为了验证密码多加了一步登录请求'''
        url = 'http://192.168.1.1/'
        ss = requests.session()
        proxies = {'http':'http://%s' % ip_port}
        cookies = {'Authorization':login_param,'path':'/'}
        ss.proxies = proxies
        try:
            tp_content = ss.get(url, cookies=cookies, timeout=10).content
            if re.search(r'userRpm/Index.htm', tp_content):
                logging.info('login sucess...')
            else:
                logging.error('login failed...')
                return False
            headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
                'Referer':'http://192.168.1.1/userRpm/MenuRpm.htm'#必填参数
            }
            reboot_url = 'http://192.168.1.1/userRpm/SysRebootRpm.htm?Reboot=%D6%D8%C6%F4%C2%B7%D3%C9%C6%F7'#Reboot参数为:重启路由器
            ss.get(reboot_url, cookies=cookies, timeout=10, headers=headers)
        except:
            logging.error('request timeouted out...')

    def router_reboot(self, pwd, ip_port):
        login_param = self.get_login_param(pwd)
        self.login_reboot(ip_port, login_param)

if __name__ == "__main__":
    ip_port = ''
    pwd = ''
    logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s ip_port:{}, %(message)s'.format(ip_port),
                datefmt='%Y-%m-%d %H:%M:%S',
                filename=os.path.join(PATH, 'tp_link.log'),
                filemode='a')
    tp_link = TP_LINK(logging)
    tp_link.router_reboot(pwd, ip_port)

