#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-08-12 06:50:35
# Project: ZhongHuaYingCai

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    crawl_config = {
        "validate_cert" : False,
        "headers": {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:54.0) Gecko/20100101 Firefox/54.0"}

    }

    def __init__(self):
        self.baseUrl = "http://www.chinahr.com/sou/?"
        self.city = "34,398"
        self.keyword = "python"
        self.params = {"city":self.city, "keyword": self.keyword}


    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.baseUrl, params=self.params, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('.jobList .l1 .e1>a').items():
            self.crawl(each.attr.href, callback=self.detail_page)

        nextPage = response.doc('.pageList a:last-child')
        if nextPage.attr.href:
            self.crawl(nextPage.attr.href, callback=self.index_page)



    @config(priority=2)
    def detail_page(self, response):
        return {
            "jobName": response.doc('.job_name').text(),
            "salary": response.doc('.job_price').text(),
            "jobLocation": response.doc('.job_require .job_loc').text(),
            "jobTpye": response.doc('.job_require span:nth-of-type(3)').text(),
            "education": response.doc('.job_require span:nth-of-type(4)').text(),
            "experience": response.doc('.job_exp').text(),
            "jobTags": response.doc('.job_fit_tags').text(),
            "jobDescribe": response.doc('.job_intro_info').text(),

            "companyName": response.doc('.job-company h4>a').text(),
            "inderstry": response.doc('.job-company tbody tr:nth-of-type(2) td:nth-child(2)').text(),
            "companySize": response.doc('.job-company tbody tr:nth-of-type(3) td:nth-child(2)').text(),
            "companyTpye": response.doc('.job-company tbody tr:nth-of-type(4) td:nth-child(2)').text(),
            "companyDescribe": response.doc('.company_service').text()


        }
