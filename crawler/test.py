# coding:utf-8
from bs4 import BeautifulSoup
import mechanize
from jft import f2j, f2j
__author__ = 'chin'

def is_cn_char(uchar):
    return uchar >= u'\u4e00' and uchar<=u'\u9fa5'
def is_alphabeta(uchar):
    return (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a')
def is_white(uchar):
    return uchar in u' \t\n\r'
def is_number(uchar):
    return uchar in u'0123456789[]{}()*&^%$#@!~`<>,./?'

def etao_f2j(src):
    dst = []
    for uchar in src:
        if is_cn_char(uchar):
            print uchar, '->',
            utf8_char = f2j('gbk','utf8', uchar.encode('gbk'))
            uchar = unicode(utf8_char, 'utf8')
            print uchar
        # else:
        #     if not is_alphabeta(uchar) and not is_white(uchar) and not is_number(uchar):
        #         print uchar
        dst.append(uchar)
    return ''.join(dst)

def main():
    url = 'http://etao.com'
    #etao_u_f = requests.get(url).text
    br = mechanize.Browser()
    br.open(url)
    response = br.response()
    r_read = response.read()
    print type(r_read) #r_read is a gbk stream
    soup = BeautifulSoup(r_read)
    u = soup.get_text()
    print type(u) #u is a unicode string
    short_u = u

    j_short_u = etao_f2j(short_u)
    # print short_u
    # print j_short_u
    pass


if __name__ == '__main__':
    main()
