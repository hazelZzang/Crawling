# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from WebCrawling.items import AjaxscrapyItem
from scrapy.http import FormRequest
import re


class WcSpider(scrapy.Spider):
    name = "test"
    start_urls = [
        "http://www.11st.co.kr/html/main.html",
    ]

    def __init__(self):
        scrapy.Spider.__init__(self)
        self.browser = webdriver.Chrome("C:\Users\kimhyeji\Desktop\chromedriver.exe")

    def parse(self, response):
        item = AjaxscrapyItem()
        url = "http://www.11st.co.kr/html/main.html"
        self.browser.get(url)
        self.browser.find_element_by_class_name('gnb_btn_all').click()

        navCtgrRow = self.browser.find_elements_by_xpath('//div[@class = "gnb_total_category"]/div')
        for navCtgrRowNum in range(len(navCtgrRow)):      #전체보기 창
            bigCtgr = self.browser.find_elements_by_xpath('//div[@class = "gnb_total_category"]/div[@id = "navCtgrRow'+str(navCtgrRowNum + 1)+'"]//strong[@class = "tit"]')
            for i in range(len(bigCtgr)):       #  1번째 카테고리 (big)
                bigCtgrText = bigCtgr[i].text
                smaCtgr = self.browser.find_elements_by_xpath('//div[@class = "gnb_total_category"]/div[@id = "navCtgrRow'+str(navCtgrRowNum + 1)+'"]//div[@class = "box"][' + str(i + 1) + ']//li')
                smaCtgrList = self.browser.find_elements_by_xpath('//div[@class = "gnb_total_category"]/div[@id = "navCtgrRow'+str(navCtgrRowNum + 1)+'"]//div[@class = "box"][' + str(i + 1) + ']//li//a')

                for j in range(len(smaCtgr)):  # 2번째 카테고리 (small)
                    request = scrapy.Request(smaCtgrList[j].get_attribute("href"), callback=self.parseSsCtgr)
                    smaCtgrText = smaCtgr[j].text
                    request.meta['bigCtgrText'] = bigCtgrText
                    request.meta['smaCtgrText'] = smaCtgrText
                    request.meta['item'] = item
                    yield request

        self.browser.close()

    def parseSsCtgr(self, response):
        item = response.meta['item']
        item['smaCtgr'] = {}
        bigCtgrText = response.meta['bigCtgrText']
        smaCtgrText = response.meta['smaCtgrText']

        # 3번째 카테고리 (ss)
        ssCtgrText = response.xpath('//div[@class = "lnb_defconts"]/ul//li/a/text()').extract()
        check = response.xpath('//div[@class = "lnb_defconts"]/ul//li/a/text()').extract_first()

        if check is None:
            pass

        else:
            item['bigCtgr'] = bigCtgrText
            item['smaCtgr'] = smaCtgrText
            item['ssCtgr'] = ssCtgrText

        nextPage = response.xpath('//div[@class = "lnb_defconts"]//li/a[@href]')
        yield item
