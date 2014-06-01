#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'
import re
import os
from urlparse import urlparse
import extract_utils


class BodyExtractor(object):
    """
    url:链接地址
    body:正文内容
    depth:行块深度
    """

    def __init__(self, url):
        self.url = url
        self.domain = ''
        self.body = ''    #正文内容
        self.depth = 3    #行块的深度
        self.html = ''
        self.plain_text = ''
        self.html_text = ''
        self.margin = 35  #从text的margin长度开始去匹配text_a_p，数值越大匹配越精确，效率越差

    def execute(self):
        self._pre_process()
        self._extract()
        self._post_process()

    def _pre_process(self):
        html = extract_utils.get_html(self.url)
        self.html = html
        parsed_uri = urlparse(self.url)
        self.domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)

        plain_text, html_text = clean_html(self.html)
        self.html_text = html_text
        self.plain_text = plain_text

    def _post_process(self):
        """
        把资源链接的相对路径改为完整路径
        清空标签的无用属性，比如class, style
        """
        #TODO: 清空标签无用属性，比如class

        def repl(match):
            s = match.group()
            return s.replace('="', '="' + self.domain)
        self.body = re.sub(r'(?:href=["\']/(.*?)["\'])|(?:src=["\']/(.*?)["\'])', repl, self.body)

    def _extract(self):
        lines = tuple(self.plain_text.split('\n'))
        #lines对应每行的长度
        len_per_lines = [len(re.sub(r'\s+', '', line)) for line in lines]

        #每个块对应的长度
        len_per_blocks = []
        for i in range(len(len_per_lines) - self.depth + 1):
            word_len = sum([len_per_lines[j] for j in range(i, i + self.depth)])
            len_per_blocks.append(word_len)

        text_list = []
        text_begin_list = []
        text_end_list = []

        for i, value in enumerate(len_per_blocks):
            if value > 0:
                text_begin_list.append(i)
                tmp = lines[i]
                while i < len(len_per_blocks) and len_per_blocks[i] > 0:
                    i += 1
                    tmp += lines[i] + "\n"
                text_end_list.append(i)
                text_list.append(tmp)

        result = reduce(lambda str1, str2: str1 if len(str1) > len(str2) else str2, text_list)
        result = result.strip()
        i_start = self._start(result)
        i_end = self._end(result)
        if i_start == 0 or i_end == 0 or i_start > i_end:
            i_start = self._start(result, position=30) - 47
        if i_start < i_end:
            self.body = self.html_text[i_start:i_end]
        else:
            self.body = []
        self.body = ''.join(self.body.splitlines())
        return self.body

    def _start(self, result, position=0):
        i_start = 0
        for i in range(self.margin)[::-1]:
            start = result[position:i + position]
            start = extract_utils.escape_regex_meta(start)
            p = re.compile(start, re.IGNORECASE)
            match = p.search(self.html_text)
            if match:
                s = match.group()
                i_start = self.html_text.index(s)
                break
        return i_start

    def _end(self, result):
        i_end = 0
        for i in range(1, self.margin)[::-1]:
            end = result[-i:]
            end = extract_utils.escape_regex_meta(end)
            p = re.compile(end, re.IGNORECASE)
            match = p.search(self.html_text)
            if match:
                s = match.group()
                i_end = self.html_text.index(s) + len(s)
                break
        return i_end


def clean_html(html):
    """
    清洗html文本，去掉无用标签
    1. "script","style",注释标签<!-->整行用空格代替
    2. 特殊字符转义
    return:(pure_text,html_text):纯文本和包含标签的html文本
    """
    regex = re.compile(
        r'(?:<!DOCTYPE.*?>)|'  #doctype
        r'(?:<head[\S\s]*?>[\S\s]*?</head>)|'
        r'(?:<!--[\S\s]*?-->)|'  #comment
        r'(?:<script[\S\s]*?>[\S\s]*?</script>)|'  # js...
        r'(?:<style[\S\s]*?>[\S\s]*?</style>)', re.IGNORECASE)  # css

    html_text = regex.sub('', html)  #保留html标签
    plain_text = re.sub(r"(?:</?[\s\S]*?>)", '', html_text)  #不包含任何标签的纯html文本
    html_text = extract_utils.html_escape(html_text)
    plain_text = extract_utils.html_escape(plain_text)
    return plain_text, html_text


if __name__ == "__main__":
    # url = "http://sports.sina.com.cn/j/2014-05-09/00227155725.shtml"
    # url = "http://sports.qq.com/a/20140509/011085.htm"
    # url ='http://sports.sina.com.cn/j/2014-05-09/23267157241.shtml?from=hao123_sports_nq'
    # url = 'http://sports.ifeng.com/gnzq/zc/hengda/detail_2014_05/10/36245019_0.shtml'
    url = 'http://sports.sohu.com/20140509/n399370219.shtml'
    # url = 'http://sports.sina.com.cn/nba/2014-05-07/09207153447.shtml'
    # url = 'http://foofish.net/blog/73/stringio'
    # url = 'http://www.importnew.com/11309.html'
    # url = 'http://gd.qq.com/a/20140511/003265.htm?qq=0&ADUIN=253421576&ADSESSION=1399776075&ADTAG=CLIENT.QQ.5323_.0&ADPUBNO=26323'
    # url = 'http://gd.qq.com/a/20140511/009231.htm'
    url = 'http://sports.qq.com/a/20140510/018805.htm'
    # url = 'http://www.qwolf.com/?p=791'
    url = 'http://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html'
    url = 'http://cn.uefa.com/memberassociations/news/newsid=2104522.html'
    url = 'http://cn.uefa.com/memberassociations/association=esp/news/newsid=2104513.html'
    # url = 'http://ballpo.com/detail/182560.html'  #OK
    url = 'http://news.arsenal.com.cn/html/a/3QEGT/'  #比较ok
    # url = 'http://www.barca.cn/portal.php?mod=view&aid=1175'  #ok
    # url = 'http://www.usportnews.com/goal/pl/60288.html' #ok
    # url = 'http://spurscn.com/forum.php?mod=viewthread&tid=3307'  #ok
    # url = 'http://www.mureds.com/thread-77077-1-1.html'  #ok
    # url = 'http://www.lfc.org.cn/Article/201309/20130905203950546.html'  #ok
    url = 'http://www.espnstar.com.cn/pub/international/2014/0422/323408.htm' #ok
    # url = 'http://www.bvbfans.net/forum.php?mod=viewthread&tid=10403&extra=page%3D1'  #ok
    url = 'http://blog.sina.com.cn/s/blog_4e8581890102ep9u.html'
    # url = 'http://news.sina.com.cn/c/2014-05-13/110530125372.shtml'  #no
    url = 'http://www.oschina.net/news/51692/ubuntukylin-is-not-a-china-linux-system' #ok
    url = 'http://joy2everyone.iteye.com/blog/930342'
    url = 'http://gd.qq.com/a/20140511/009231.htm'
    url = 'http://ballpo.com/detail/182560.html'
    te = BodyExtractor(url)
    te.execute()
    print te.body
    # print te.img
    # print te.title






