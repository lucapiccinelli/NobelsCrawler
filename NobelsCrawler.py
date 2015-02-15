# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 17:20:24 2015

@author: Luca
"""

import urllib2
import re
from HTMLParser import HTMLParser

global nobel_prizes_list 

def extraxt_list_from_html(html, regex):
    htmlParser = HTMLParser()
    l = []
    regex = re.compile(regex)
    for line in html.splitlines():
        match = regex.findall(line)
        if match:
            for group in match:
                l.append(htmlParser.unescape(group))
                
    return l


def get_nobel_prized_list():
    nobel_prizes_url = 'http://www.nobelprize.org/nobel_prizes/medicine/laureates/'
    response = urllib2.urlopen(nobel_prizes_url)
    nobel_html = response.read()
    return extraxt_list_from_html(nobel_html, r'<a\s+href="[^\"]*facts.html">([^<>]+)<\/a>')
    
    
def find_page_links(html):
    return extraxt_list_from_html(html, r'<a\s+href="((?!http)/[^\"]{2,})">')
    
def crawl(domain, url, crawl_dict, fn):
    if url not in crawl_dict:
        crawl_dict[url] = 1
        print 'crawling {0}'.format(url)
        response = urllib2.urlopen(url)
        html = response.read()
        fn(html)
        for link in find_page_links(html):
            crawl(domain, '{0}{1}'.format(domain, link), crawl_dict, fn)
            
def contains_nobel_name(html):
    global nobel_prizes_list
    
    for prize in nobel_prizes_list:
        if prize in html:
            print 'this page contains: {0}'.format(prize)

if __name__ == '__main__':
    global nobel_prizes_list
    nobel_prizes_list = get_nobel_prized_list()
    print len(nobel_prizes_list)    
       
    crawl('http://www.nobelprize.org', 'http://www.nobelprize.org/nobel_prizes/medicine/laureates/', {}, contains_nobel_name)
    
    
    
    
    
        
        