#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-07-04 08:41:20
# Project: jobTong

from pyspider.libs.base_handler import *
import math


class Handler(BaseHandler):
    headers = {
        "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Cookie": "jobtong.id=Fe26.2**e8d1d1aa1081c54ac1a6a9e36c7c59117b44bc7355a29bedadd12d735d01761d*-2-k33iidc5Nh5GZoLTTFw*5NR4_e1k2G_2b8FPPAEhMbrvRGS-5eQHerFVmrLJJyRmDTqCO3v4efmafzg66Mus**b4bfe06ba61a8970a20a1b9ac434cb296b3d6a7fffc8794b94a8e3450fa284fb*cMloM0lYDanB_iGh-RY46P4kMyW32vtU9Wi9ccRMobc"
    }
    
    crawl_config = {
        "validate_cert" : False,
        "headers": headers
    }
    
    citys = {"11": '北京', "12": '上海', "13": '广州', "14": '深圳', "15": '杭州', "19": '成都', "17": '南京', "42": '武汉', "33": '厦门', "21": '天津', "51": '西安', "16": '苏州'}
    
    #industries = {'1': '互联网', '2': '移动互联网', '3': '游戏', '4': '电子商务', '5': '新媒体', '6': '广告', '7': '金融', '8': 'IT/软件', '9': '通信', '10': '教育', '11': '健康医疗', '12': '智能硬件'}
    
    degrees = {'0': '不限', '1': '专科', '2': '本科', '3': '硕士', '4': '博士'}
    experiences = {'0':'不限', '1': '应届生', '2': '1年以下', '3': '1-3年', '4': '3-5年', '5': '5-10年', '6': '10年以上'}
    
    
    def __init__(self):
        self.keyword = 'Python'

        # 工作地点 北京11, 上海12, 广州13
        
        self.city = 11
        # 行业领域: 互联网1 移动互联网2 游戏3 电子商务4 新媒体5 广告6 金融7 IT/软件8 通信9 教育10 健康医疗11 智能硬件12
        self.industry = 0
        # 职业技能
        self.category = 10
        # 薪资待遇 全部0, 3K以下 1, 3K-5K 2, 5K-8K 3, 8K-15K 4, 15K-20K 5, 20K-30K 6, 30K-50K 7, 50K以上 8
        self.salary = 0
        # 学历要求 全部0 专科1 本科2 硕士3 博士4
        self.degree = 0
        # 工作经验 全部0 应届生 1, 1年以下 2, 1-3年 3, 3-5年 4, 5-10年 5, 10年以上 6
        self.experience = 0

        self.page = 1

        self.params = {"city": self.city, "keyword": self.keyword, 'page': 1}
        
#        self.params = {"city": self.city, "industry": self.industry,\
#                        "category": self.category, "salary": self.salary, "degree": self.degree, "experience": self.experience, "query": self.keyword}
        
        self.baseUrl = 'http://www.jobtong.com/api/jobs?'

        
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.baseUrl, params=self.params, callback=self.index_page)

        
    
    @config(age=10 * 24 * 60 * 60)
    def index_page(self, response):
        print(response.url)
        print(response.json['count'])
        totalPage = math.ceil(response.json['count'] / 20)
        print(totalPage)
        
        while self.params['page'] <= totalPage:
            self.crawl(self.baseUrl, params=self.params, callback=self.detail_page)
            self.params['page'] += 1

            
    @config(priority=2)
    def detail_page(self, response):
        currentPageInfo = []
        for item in response.json['items']:
            company = item['company']
            jobInfo = {
                '职位名称': item['name'],
                '标题': item['thread_title'],
                '工资': item['salary'],
                '学历': self.degrees.get(item['min_degree']),
                '工作经验': self.experiences.get(item['min_experience']),
                '工作描述': item['description'],
                '工作地点': self.citys.get(item['city_id']),
                '行业': item['industry_name'],
                '城市': item['city_name'],
                '分类': item['category_name'],
                '地址': item['address'],
                '公司全称': company['name'],
                '公司简称': company['alias'],
                '公司描述': company['description'],
            }
            currentPageInfo.append(jobInfo)

        return currentPageInfo
