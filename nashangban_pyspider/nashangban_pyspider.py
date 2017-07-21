#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-03 13:54:52
# Project: NaShangBan

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    headers = {
         "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    
    crawl_config = {
        "validate_cert" : False,
        "headers": headers   
    }
    
    
    def __init__(self):
        self.keyword = 'Python'
        # 职位类型 设计design, 产品product, 市场销售marketing 
        self.category = 'engineering'
        # 工作地点 北京1,上海11, 广州267
        self.region = 1
        self.page = 1
        self.params = {"keyword": self.keyword, 'category': self.category, 'region': self.region, 'page': 1}
        self.baseUrl = 'https://www.nashangban.com/job_list?'
#        self.searchUrl = 'https://www.nashangban.com/search?search_type=job'
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.baseUrl, params=self.params, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('div.job-list div.job.clearfix a.title').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        
        nextPage = response.doc('.widget-pager span+a')
        if nextPage is not None:
            self.crawl(nextPage.attr.href, callback=self.index_page)


    @config(priority=2)
    def detail_page(self, response):
        
        return {
            "url": response.url,
            "title": response.doc('title').text(),
            "职位名称": response.doc('div.job-info h3').text(),
            "工作地点": response.doc('.location b').text(),
            "工作性质": response.doc('.type b').text(),
            "起薪": response.doc('.salary-start b').text(),
            "工作描述": response.doc('.job-describe').text(),
            "公司": response.doc('a.cmpy-card-name').text(),
            "公司成立时间": response.doc('div.nsb-block-content > div > div:nth-child(4) > span.body').text(),
            "公司融资阶段": response.doc('div.nsb-block-content > div > div:nth-child(5) > span.body').text(),
            "公司规模": response.doc('div.nsb-block-content > div > div:nth-child(6) > span.body').text()
            
        }
