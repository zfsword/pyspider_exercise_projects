#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-07 06:45:30
# Project: ZhiLian

from pyspider.libs.base_handler import *


class Handler(BaseHandler):
    headers = {
        "Cookie":"dywez=95841923.1499381113.1.1.dywecsr=(direct)|dyweccn=(direct)|dywecmd=(none)|dywectr=undefined; urlfrom=121126445; urlfrom2=121126445; adfcid=none; adfcid2=none; adfbid=0; adfbid2=0; LastCity=%e5%8c%97%e4%ba%ac; LastCity%5Fid=530; JSSearchModel=0; LastSearchHistory=%7b%22Id%22%3a%2221a286f4-7f9c-418c-bb11-f1b6a1a1ccce%22%2c%22Name%22%3a%22python+%2b+%e5%8c%97%e4%ba%ac%22%2c%22SearchUrl%22%3a%22http%3a%2f%2fsou.zhaopin.com%2fjobs%2fsearchresult.ashx%3fjl%3d%25e5%258c%2597%25e4%25ba%25ac%26kw%3dpython%26sm%3d0%26p%3d5%22%2c%22SaveTime%22%3a%22%5c%2fDate(1499382382895%2b0800)%5c%2f%22%7d; dywea=95841923.2634686049428664000.1499381113.1499381113.1499381113.1; dywec=95841923; dyweb=95841923.6.10.1499381113",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    
    crawl_config = {
        "headers": headers,
        "validate_cert" : False
    }
    
    def __init__(self):
        self.baseUrl = 'http://sou.zhaopin.com/jobs/searchresult.ashx?'

#        self.page = {'p': 1}
        self.params = {'kw': 'Python', 'jl': '北京', 'p': 1, 'sm': 0}

    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.baseUrl, params=self.params, callback=self.index_page)

    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        for each in response.doc('td.zwmc a').items():
            self.crawl(each.attr.href, callback=self.detail_page)
        
        
        nextPage = response.doc('.pagesDown .next-page')
#        print(nextPage.text())
#        if not nextPage.is_('.nopress2'):
        if nextPage.attr.href:
            self.crawl(nextPage.attr.href, callback=self.index_page)


    @config(priority=2)
    def detail_page(self, response):

        data = {
#            "url": response.url,
#            "title": response.doc('title').text(),
            "职位名称": response.doc('.inner-left h1').text(),
            "福利待遇": response.doc('.welfare-tab-box').text(),
            "职位月薪": response.doc('.terminalpage-left .terminal-ul li:nth-child(1) strong').text(),
            "工作地点": response.doc('.terminalpage-left .terminal-ul li:nth-child(2) strong').text(),
            "发布日期": response.doc('.terminalpage-left .terminal-ul li:nth-child(3) strong').text(),
            "工作性质": response.doc('.terminalpage-left .terminal-ul li:nth-child(4) strong').text(),
            "工作经验": response.doc('.terminalpage-left .terminal-ul li:nth-child(5) strong').text(),
            "最低学历": response.doc('.terminalpage-left .terminal-ul li:nth-child(6) strong').text(),
            "招聘人数": response.doc('.terminalpage-left .terminal-ul li:nth-child(7) strong').text(),
            "职位类别": response.doc('.terminalpage-left .terminal-ul li:nth-child(8) strong').text(),
            "职位描述": response.doc('.terminalpage-left .terminalpage-main .tab-cont-box div:nth-child(1) p').text(),
            "工作地址": response.doc('.terminalpage-left .terminalpage-main .tab-cont-box div:nth-child(1) h2').text().split(' ')[0],
            "公司简介": response.doc('.terminalpage-left .terminalpage-main .tab-cont-box div:nth-child(2)').text(),
            "公司名称": response.doc('.terminalpage-right .company-name-t a').text(),
#            "公司规模": response.doc('.terminalpage-right .terminal-ul li:nth-child(1) strong').text(),
#            "公司性质": response.doc('.terminalpage-right .terminal-ul li:nth-child(2) strong').text(),
#            "公司行业": response.doc('.terminalpage-right .terminal-ul li:nth-child(3) strong').text(),
#            "公司地址": response.doc('.terminalpage-right .terminal-ul li:nth-child(4) strong').text(),
            
                  
        }
        # 公司信息
        companyInfo = response.doc('.terminalpage-right .terminal-ul li')
        for item in companyInfo.items():
            data.update({item('span').text():item('strong').text()})
            
        return data
