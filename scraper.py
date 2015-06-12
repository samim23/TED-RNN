#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2, urllib
from lxml import html  
import urlparse  
import collections

STARTING_URL = 'http://www.ted.com/talks?page=1'
urls_queue = collections.deque()  
urls_queue.append(STARTING_URL)  
processed_urls = set()  
processed_urls.add(STARTING_URL)
counter = 0

def getTedTalkText(url):
    global counter

    try:
        response = urllib2.urlopen(url)
        res = response.read()
        
        parsed_body = html.fromstring(res)
        tedtalk = parsed_body.xpath('//span[@class="talk-transcript__fragment"]/text()')
       
        if tedtalk:
            finalText = ''
            talkTitle = parsed_body.xpath('//*[@id="shoji"]/div[2]/div/div[2]/div/div/div/div[2]/div[1]/div/div[2]/div/div[2]/h4[2]/a/text()')[0].replace('\n', '')
            speakerName = parsed_body.xpath('//h4[@class="h12 talk-link__speaker"]/text()')[0]
            finalText += talkTitle + '\n' + 'by ' + speakerName + '\n\n'

            finaltalk = ''
            for txt in tedtalk:
                finaltalk += txt + ' '

            finalText += finaltalk + '\n\n\n\n'
            encode_str = finalText.encode('utf-8')

            counter += 1
            print 'TED Talks found: ' + str(counter)

            with open("tedtalks.txt", "a") as myfile:
                myfile.write(encode_str)

    except urllib2.HTTPError, e:
        print e.code   


while len(urls_queue):  
    url = urls_queue.popleft()
    response = urllib2.urlopen(url)
    request = response.read()
    parsed_body = html.fromstring(request)
    links = parsed_body.xpath('//a/@href')
    
    for link in links:
        if link not in processed_urls:
            processed_urls.add(link)

            if("/talks/" in link):
                link = link.replace('.html', '')
                link = link.replace('/lang/eng/', '/')
                link = link + '/transcript?language=en'
                link = 'http://www.ted.com' + link
                getTedTalkText(link)
            if("/talks?" in link):
                link = 'http://www.ted.com' + link
                urls_queue.append(link)
        
