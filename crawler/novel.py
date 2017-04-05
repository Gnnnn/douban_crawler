# encoding: utf-8

import socket
import ssl
import urllib2
def html():
    req = urllib2.Request("http://www.bxwx9.org/b/82/82712/13916007.html")
    res = urllib2.urlopen(req)
    html = res.read()
    res.close()
    html = unicode(html, "gbk").encode("utf8")  # gb2312--->utf-8
    print html

#输入需要查找的，开始的，结束的字符串，返回之间的字符
def findall_in_html(html, startpart, endpart):
    all_strings = []
    start = html.find(startpart) + len(startpart)
    end = html.find(endpart, start)
    string = html[start:end]
    while html.find('</html>') > start > html.find('<html'):
        all_strings.append(string)
        start = html.find(startpart, end) + len(startpart)
        end = html.find(endpart, start)
        string = html[start:end]
    return all_strings


def find_content_in_html(html, startpart, endpart):
    all_strings = []
    start = html.find(startpart) + len(startpart)
    end = html.find(endpart, start+30)
    string = html[start:end]
    while html.find('</html>') > start > html.find('<html'):
        all_strings.append(string)
        start = html.find(startpart, end) + len(startpart)
        end = html.find(endpart, start)
        string = html[start:end]
    return all_strings


# 得到豆瓣电影top250的html，以列表形式保存，每个元素为一个页面的字符串
#需改url地址
def htmls_from_douban():
    index = 0
    html = []
    # url = """https://movie.douban.com/top250?start={}&filter="""
    url = """http://www.bxwx9.org/b/82/82712/{}.html"""
    for index in range(13915906, 13916007, 1):
        url.format(index)
        r = get(url)
        html.append(r)
    return html


# 得到页面中所有的影片名字
# 得到小说章节名字
def movie_name(html):
    name = findall_in_html(html, '<title>', '</title>')
    return name


# 得到页面中所有电影的打分
# 得到小说本章内容
def movie_score(html):
    score = find_content_in_html(html, '<div id="content">', '</div>')
    return score



# 分析页面， 打包返回电影的名字、打分、引言
# 分析页面， 打包返回小说名字，内容
def movie_data_from_html(htmls):
    movie = []
    score = []
    for h in htmls:
        m = movie_name(h)
        s = movie_score(h)
        movie.extend(m)
        score.extend(s)
    data = zip(movie, score)
    return data


# 发请求，得响应
def get(url):
    # print('URL:', url)
    u = url.split('://')[1]
    protocol = url.split('://')[0]
    i = u.find('/')
    host = u[:i]
    path = u[i:]
    if protocol == 'https':
        s = ssl.wrap_socket(socket.socket())
        port = 443
        # print('use    https')
    else:
        s = socket.socket()
        port = 80
        # print(protocol)
    s.connect((host, port))
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\n\r\n'.format(path, host)
    # print('request', request)
    encoding = 'utf-8'
    s.send(request.encode(encoding))
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        response += r
        if len(r) < buffer_size:
            break
    response = response.decode(encoding)
    return response


def main():
    # 请求页面
    htmls = htmls_from_douban()
    # 分析页面，得到电影数据
    movie_data = movie_data_from_html(htmls)
    # 写入小说内容
    #小说名字需改
    new_path_filename = r'G:\娱乐\文档\小说\法师三定律.txt'
    read = open(new_path_filename, 'a+')
    counter = 0
    for item in movie_data:
        counter = counter + 1
        read.write('第' + str(counter)+'章')
        read.write('章节名:'+item[0])
        read.write(item[1]+'\n\n')
    read.close

def test():
    html()
    # re = get("http://www.bxwx9.org/b/82/82712/13916007.html")
    # htmls = htmls_from_douban()

if __name__ == '__main__':
    test()
    # main()
    print("It is all right!")
