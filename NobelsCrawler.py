# -*- coding: utf-8 -*-
"""
Created on Sun Feb 15 17:20:24 2015

@author: Luca
"""

import urllib2
import urlparse
import re
from HTMLParser import HTMLParser

global nobel_prizes_list 

def extract_list_from_html(html, regex):
    htmlParser = HTMLParser()
    l = []
    regex = re.compile(regex)
    match = regex.findall(html)
    if match:
        for group in match:
            l.append(str(htmlParser.unescape(group)))
                
    return l


def get_nobel_prizes_list():
    nobel_prizes_url = 'http://www.nobelprize.org/nobel_prizes/medicine/laureates/'
    response = urllib2.urlopen(nobel_prizes_url)
    nobel_html = response.read()
    nobels_list = extract_list_from_html(nobel_html, r'<a\s+href="[^\"]*facts.html">([^<>]+)<\/a>')
    nobel_names_list1 = []    
    nobel_names_list2 = []
    nobel_names_list3 = []
    for x in nobels_list:
        name = [s.rstrip(',') for s in x.split(' ')]
        if len(name[0]) > 2 and name[0] != 'Sir':
            nobel_names_list1.append(name[0])
        else:
            nobel_names_list1.append(name[1])
            
        if len(name[-1]) > 2 and name[-1][-1] != '.':
            nobel_names_list2.append(name[-1])
        else:
            nobel_names_list2.append(name[-2])
            
        name_str = ''
        for n in name:
            if len(n) > 2 and n[-1] != '.':
                name_str += n + ' '
        
                
        nobel_names_list3.append(name_str[:-1])
        
    nobel_names_list4 = [' '.join([x, y]) for x, y in zip(nobel_names_list1, nobel_names_list2) ]
        
    
    with open(r'd:\nobel_list.txt', 'w') as f:
        f.write('\n'.join(nobels_list))
        f.write('\n\n\n')
        f.write('\n'.join(nobel_names_list3))
        f.write('\n\n\n')
        f.write('\n'.join(nobel_names_list4))
    
    return nobels_list + nobel_names_list4 + nobel_names_list3
    
    
def find_page_links(html):
    return extract_list_from_html(html, r'<a\s+[^>]*href="((?!http)[^\"#]+)"[^>]*>')
    
def crawl(domain, url, crawl_dict, fn):
    if url not in crawl_dict and not url.endswith('.jpg') and not url.endswith('.pdf') and not url.endswith('.png'):
        crawl_dict[url] = 1
        print 'crawling {0}'.format(url)
        try:
            response = urllib2.urlopen(url)
            if(response.info().maintype == 'text'):
                html = response.read()
                fn(url, html)
                for link in find_page_links(html):
                    crawl(domain, urlparse.urljoin(url, link), crawl_dict, fn)
        except urllib2.URLError:
            print 'not an url: {0}'.format(url)
            
def contains_nobel_name(page_url, html):
    global nobel_prizes_list
    global filename
    
    for prize in nobel_prizes_list:
        if prize in html:
            l = 'the page {0} page contains: {1}'.format(page_url, prize)
            print l
            with open(filename, 'a') as f:
                f.write(l + '\n')
            

if __name__ == '__main__':
    global filename
    global nobel_prizes_list
    
    filename = r'd:\nobel.txt'
    
    nobel_prizes_list = get_nobel_prizes_list()
    print len(nobel_prizes_list)
       
    crawl(r'http://cgmone.cgm.ag/cgm_com/', r'http://cgmone.cgm.ag/cgm_com/index.en.jsp', {}, contains_nobel_name)
    
    
    
    
    
        
        