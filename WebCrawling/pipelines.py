import json
# -*- coding: utf-8 -*-

# Define your item pipelines here

# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WebCrawlingPipeline(object):
    global ctgr
    ctgr = {}

    def __init__(self):
        global file
        file = open("test.json","w")

    def process_item(self, item, spider):
        ctgr[item['bigCtgr']] = { item['smaCtgr'] : item['ssCtgr'] }

    def __del__(self):

        b = json.dumps(ctgr, ensure_ascii=False).encode('utf-8')
        file.write(b)
        file.write('\n')
        file.close()