import socket
import ssl


def log(*args, **kwargs):
    print("log: ", *args, **kwargs)


def get(url):
    port = 443
    u = url.split("://")
    host = u[1]
    path = "/"
    query = []
    f = host.find("/")
    if f != -1:
        path = host[f:]
        host = host[:f]
        q = path.find("?")
        if q != -1:
            query = path[q:]
            path = path[:q]
    log("host,path,query,port: {},{},{},{}".format(host, path, query, port))

    s = ssl.wrap_socket(socket.socket())
    s.connect((host, port))
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\n\r\n'.format(path, host)
    # log('request:', request)
    s.send(request.encode('utf-8'))

    response = b''
    while True:
        r = s.recv(256)
        response += r
        if len(r) < 256:
            break
    response = response.decode('utf-8')
    # log(response)
    return response


def Gn_find(body, start, end):
    start_lct = body.find(start) + len(start)
    end_lct = body.find(end, start_lct)
    Gnwants = []
    while body.find('</body>') > start_lct > body.find('<body>'):
        # log(body.find(end, start_lct))
        if "&nbsp" not in body[start_lct:end_lct]:
            Gnwants.append(body[start_lct:end_lct])
        start_lct = body.find(start, end_lct) + len(start)
        end_lct = body.find(end, start_lct)
    # log(Gnwants)
    # log(len(Gnwants))
    return Gnwants


def judge_find(body, start, end):
    start_lct = body.find(start) + len(start)
    end_lct = body.find(end, start_lct)
    Gnwants = []
    Gnwants.append(body[start_lct:end_lct])
    # log(Gnwants)
    return Gnwants

def htmls_from_douban():
    index = 0
    html = []
    h = ''
    url = """https://movie.douban.com/top250?start={}&filter="""
    for index in range(0, 250, 25):
        url.format(index)
        r = get(url)
        html.append(r)
    log("html",html)
    for i in html:
        h += str(i)
    log("h",h)
    return h


def movie_name():
    # url = 'https://movie.douban.com/top250'
    body = htmls_from_douban()
    # log("body",body)
    n = Gn_find(body, "<span class=\"title\">", "</span>")
    r = Gn_find(body, "<span class=\"rating_num\" property=\"v:average\">", "</span>")
    d = Gn_find(body, "<span class=\"inq\">", "</span>")
    p = Gn_find(body, "<div class=\"star\">", "</div>")
    q = []
    for i in p:
        j = judge_find(i, "<span>", "</span>")
        q.append(j)
    return n, r, q, d


def Gn_print(n, r, q, d):
    for i in range(0, 250):
        print("No: {}".format(i + 1))
        print("电影名称: {}".format(n[i]))
        print("电影评分: {}".format(r[i]))
        jg = ''.join(q[i])
        print("评价人数: {}".format(jg))
        print("电影简介: {}".format(d[i]))
        print("")


if __name__ == "__main__":
    n, r, q, d = movie_name()
    # Gn_print(n, r, q, d)
