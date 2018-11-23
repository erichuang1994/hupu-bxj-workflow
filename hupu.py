# coding:utf8
import sys
sys.path.insert(0, './lib')

import urllib2
from xml.etree import ElementTree as ET
from multiprocessing.dummy import Pool as ThreadPool
from bs4 import BeautifulSoup
reload(sys)
sys.setdefaultencoding('utf-8')


def get_items(uri='https://bbs.hupu.com/bxj', query=None):
    contents = urllib2.urlopen(uri).read()
    soup = BeautifulSoup(contents, "html5lib")
    res = soup.select("#ajaxtable > div.show-list > ul > li")
    items = []
    for x in res[1:]:
        item = {}
        item['uid'] = x.find(class_="truetit").get("href")[1:]
        item['arg'] = "https://bbs.hupu.com" + \
            x.find(class_="truetit").get("href")
        item['title'] = x.find(class_="truetit").text
        item['subtitle'] = '回复/浏览:%s 作者:%s' % (x.find(
            class_="ansour").text, x.find(class_="aulink").text)
        item['icon'] = 'icon.png'
        items.append(item)
    xml = generate_xml(items)
    return xml


def generate_xml(items):
    xml_items = ET.Element('items')
    for item in items:
        xml_item = ET.SubElement(xml_items, 'item')
        for key in item.keys():
            if key is 'uid' or key is 'arg':
                xml_item.set(key, item[key])
            else:
                child = ET.SubElement(xml_item, key)
                child.text = item[key]
    return ET.tostring(xml_items)


def parse_item(item):
    return {
        'uid': '%s' % (item['id']),
        'arg': item['url'],
        'title': item['title'],
        'subtitle': 'author by %s ' % (item['by']),
        'icon': 'icon.png'
    }