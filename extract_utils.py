#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'liuzhijun'
import re
import urllib2
import gzip

try:
    from cStringIO import StringIO  # py2
except ImportError:
    from io import StringIO  # py3

#正则表达式元字符
meta_chars = [
    '+', '*', '?', '[', ']', '.', '{', '}', '(', ')'
]
meta_regex = '([' + '\\'.join(meta_chars) + '])'


def escape_regex_meta(text):
    """
     text中正则表达式元字符替换成普通成字符
    """
    return re.sub(meta_regex, lambda matchobj: '\\' + matchobj.group(), text)


def url_validate(url):
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return regex.match(url) is not None


def html_escape(text):
    """
    html转义
    """
    text = (text.replace("&quot;", "\"").replace("&ldquo;", "“").replace("&rdquo;", "”")
            .replace("&middot;", "·").replace("&#8217;", "’").replace("&#8220;", "“")
            .replace("&#8221;", "\”").replace("&#8212;", "——").replace("&hellip;", "…")
            .replace("&#8226;", "·").replace("&#40;", "(").replace("&#41;", ")")
            .replace("&#183;", "·").replace("&amp;", "&").replace("&bull;", "·")
            .replace("&lt;", "<").replace("&#60;", "<").replace("&gt;", ">")
            .replace("&#62;", ">").replace("&nbsp;", " ").replace("&#160;", " ")
            .replace("&tilde;", "~").replace("&mdash;", "—").replace("&copy;", "@")
            .replace("&#169;", "@").replace("♂", "").replace("\r\n|\r", "\n"))
    return text


def get_html(url):
    assert url_validate(url), "invalid url"
    request = urllib2.Request(url)
    request.add_header("Accept-encoding", 'gzip')
    request.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.2; WOW64) '
                                     'AppleWebKit/537.36 '
                                     '(KHTML, like Gecko) Chrome/34.0.1847.131')
    response = urllib2.urlopen(request)
    html = response.read()

    def encode(html):
        try:
            html = unicode(html, 'utf-8').encode('utf-8')
        except UnicodeDecodeError:
            html = unicode(html, 'gbk').encode('utf-8')
        return html

    if response.info().get("Content-Encoding") == 'gzip':
        buf = StringIO(html)
        f = gzip.GzipFile(fileobj=buf)
        html = f.read()
        f.close()
        buf.close()
    html = encode(html)
    return html