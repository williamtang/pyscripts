#!/usr/bin/env python
#encoding:utf-8

import sys
import socket
from urllib import urlretrieve
from multiprocessing import Pool

def parse(line):
    # parse each line,return image url
    # and image name
    lst = line.split()
    url = lst[1]
    lst = url.split('/')
    img_name = lst[-1]
    return [url, img_name]

def fetch_img(*lst):
    full_path = lst[2]+lst[1]
    count = 0
    while True:
        try:
            print 'picture', lst[1], 'begin...'
            urlretrieve(lst[0], full_path)
        except socket.timeout:
            #print 'timeout:', lst[1], 'count:', count
            count += 1
        except Exception, e:
            #print lst[1], 'other fault:', e
            count += 1
        else:
            print 'picture', lst[1], 'save successfully! it has tried to download', count, 'times'
            break

def save_pictures(urls,path):
    print 'save pictures start'
    p = Pool(4)
    count = 0
    totalnum = len(urls)
    for item in urls:
        #print item[0], item[1]
        url,img_name = parse(item)
        count += 1
        p.apply_async(fetch_img,args=(url,img_name,path))
    p.close()
    p.join()
    print 'all save successfully!!!'

if __name__ == "__main__":
    fp = open(sys.argv[1])  # input url text
    path = sys.argv[2]
    print path,
    socket.setdefaulttimeout(5)
    while 1:
        line = fp.readlines(100000) # fetch 100000 lines
        if not line:
            break
        save_pictures(line, path)
        #for s in line:
        #    # print s,
        #    url, img_name = parse(s) # split the url and image name
        #    print [url, img_name]
        #    fetch_img(url, img_name)

    fp.close()
