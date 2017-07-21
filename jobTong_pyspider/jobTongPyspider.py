#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-04 08:41:20
# Project: jobTong

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

        # 工作地点 北京11, 上海12, 广州13
        self.region = '11'
        # 行业领域: 互联网1 移动互联网2 游戏3 电子商务4 新媒体5 广告6 金融7 IT/软件8 通信9 教育10 健康医疗11 智能硬件12
        self.domain = '0'
        # 职业技能
        self.skill = '10'
        # 薪资待遇 全部0, 3K以下 1, 3K-5K 2, 5K-8K 3, 8K-15K 4, 15K-20K 5, 20K-30K 6, 30K-50K 7, 50K以上 8
        self.salary = '0'
        # 学历要求 全部0 专科1 本科2 硕士3 博士4  academic qualification
        self.aq = '0'
        # 工作经验 全部0 应届生 1, 1年以下 2, 1-3年 3, 3-5年 4, 5-10年 5, 10年以上 6
        self.experience = '0'
        self.page = '16'
        
        self.condition = self.region + '.' + self.domain + '.' + self.skill + '.' + self.salary + '.' + self.aq + '.' + self.experience + '.' + self.page
        
        self.params = {"query": self.keyword}
        
        self.baseUrl = 'http://www.jobtong.com/jobs/'

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.baseUrl+self.condition+'?', params=self.params, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
#        for each in response.doc('.job-rampage-item > h3 > a').items():
#            self.crawl(each.attr.href, callback=self.detail_page)
        
        nextPage = response.doc('.pagination .active+li>a')
        disabledButton = response.doc('.pagination li.disabled')
#        print(nextPage.text())
#        print(nextButton.text())
        if disabledButton.text() != '下一页':
            print(nextPage.text())
            self.crawl(nextPage.attr.href, callback=self.index_page)

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
#            "title": response.doc('title').text(),
            "职位名称": response.doc('div.content > div:nth-child(1) > h2:nth-child(1)').text(),
            "职位亮点": response.doc('div.content > div:nth-child(1) > h3 > span:nth-child(2)').text(),
            "薪资": response.doc('div.tags > span.r > span:nth-child(2)').text(),
            "学历要求": response.doc('div.content > div:nth-child(1) > div.tags > span:nth-child(2)').text(),
            "工作地点": response.doc('div.content > div:nth-child(1) > div.tags > span:nth-child(3)').text(),
            "公司简称": response.doc('div.sidebar > div > h3 > a').text(),
            "公司全称": response.doc('div.sidebar > div > div:nth-child(3) > p:nth-child(1)').text(),
            "公司地址": response.doc('div.sidebar > div > div:nth-child(3) > p:nth-child(3)').text(),
            "职位详情": response.doc('.details').text()
        }
