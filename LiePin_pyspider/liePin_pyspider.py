#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-06 07:41:59
# Project: LiePin

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    headers = {"Cookie":
        "verifycode=56b6e04b68fd438b99c0c3cba3848db8; _fecdn_=1; __uuid=1499296406433.20; _uuid=15079D44FFA8480C0B80949411857216; _mscid=00000000; abtest=0; __tlog=1499296406434.72%7C00000000%7CR000000075%7Cs_o_009%7Cs_o_009; __session_seq=6; __uv_seq=6",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    crawl_config = {
        "headers": headers,
        "validate_cert" : False
    }
    

    def __init__(self):
        self.baseUrl = 'https://www.liepin.com/zhaopin/?industries=&dqs=010&salary=&jobKind=&pubTime=&compkind=&compscale=&industryType=&clean_condition=&isAnalysis=&init=1&sortFlag=15&flushckid=1&headckid=b9bb34190cb05623'

#        self.curPage = {'curPage': 0}
        self.params = {'key': 'Python', 'fromSearchBtn': 2, 'searchType': 1}

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.baseUrl, params=self.params, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.job-info h3 a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        
        nextPage = response.doc('.pagerbar .current+a')
#        lastPage = response.doc('.pagerbar a.last').text()
#        print(nextPage.text(), lastPage)
        if not nextPage.is_('.disabled'):
            self.crawl(nextPage.attr.href, callback=self.index_page)
        else:
            print('Last Page Finished')

        

    @config(priority=2)
    def detail_page(self, response):
        return {
            "url": response.url,
            "职位名称": response.doc('.title-info h1').text(),
            "企业名称": response.doc('.title-info h3 a').text(),
            "薪资待遇": response.doc('.job-item-title').text().split(' ')[0],
            "反馈时间": response.doc('.job-item-title span').text(),
            "工作地点": response.doc('.basic-infor a').text(),
            "学历要求": response.doc('.job-qualifications span:nth-child(1)').text(),
            "工作经验": response.doc('.job-qualifications span:nth-child(2)').text(),
            "语言能力": response.doc('.job-qualifications span:nth-child(3)').text(),
            "年龄": response.doc('.job-qualifications span:nth-child(4)').text(),
            "职位标签": response.doc('.tag-list').text(),
            "职位描述": response.doc('div.about-position > div:nth-child(3) > div').text(),
            "企业行业": response.doc('.company-infor ul li:nth-child(1)').text(),
            "企业阶段": response.doc('.company-infor ul li:nth-child(2)').text(),
            "企业规模": response.doc('.company-infor ul li:nth-child(3)').text(),
            "企业性质": response.doc('.company-infor ul li:nth-child(4)').text(),
            "企业地址": response.doc('.company-infor p').text(),
            "企业介绍": response.doc('div.about-position > div.job-item.main-message.noborder > div').text()    
        }
