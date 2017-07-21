
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2017-06-15 09:23:40
# Project: lagou_python_job

from pyspider.libs.base_handler import *
import math


class Handler(BaseHandler):

    headers = {'X-Requested-With': 'XMLHttpRequest',
         "User-Agent": r"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
          }
    
    crawl_config = {
        "validate_cert" : False,
        "headers": headers   
    }
    

    def __init__(self):
        self.search_word = 'python'
        self.city = '北京'
        self.district = '朝阳区'
        self.gj = '' # 工作经验
        self.hy = '' #行业

        
        self.ajax_url = r'https://www.lagou.com/jobs/positionAjax.json?'
        # url传递参数
        self.params = {"city": self.city, "district": self.district, "hy": self.hy, "gj": self.gj}
        # POST 数据
        self.data = {"first": "true", "pn": 1, "kd": self.search_word}
        
        # 工作细节基础地址
        self.jobDetailBaseUrl = 'https://www.lagou.com/jobs/'
        
        # 工作信息
        self.jobInfo = []
        
        # 工作详细信息
        self.jobDetail = []
        
        
    
    
    @every(minutes=24 * 60)
    def on_start(self):
        self.crawl(self.ajax_url, params=self.params, method="POST", data=self.data, callback=self.json_info)
       

    @config(age=0)
    def json_info(self, response):
        if response.json['success']:
            content = response.json["content"]
            for x in content['positionResult']['result']:
                currentJobInfo = {
                '职位名称':x['positionName'],
                '工作经验':x['workYear'],
                '学历':x['education'],
                '工作地点':x['district'],
                '职位标签':x['positionLables'],
                '工作类型1':x['firstType'],
                '工作类型2':x['secondType'],
                '职位类型':x['jobNature'],
                '薪资待遇':x['salary'],
                '职位诱惑':x['positionAdvantage'],
                '职位ID':x['positionId'],
                '公司简称':x['companyShortName'],
                '公司全称':x['companyFullName'],
                '公司标签':x['companyLabelList'],
                '行业领域':x['industryField'],
                '行业标签':x['industryLables'],
                '公司规模':x['companySize'],
                '发展阶段':x['financeStage'],
                '发布时间':x['formatCreateTime']
                }
                #"pageNumber":x['pageNumber'],
                #"companyId":x['companyId'],
    #           gradeDescription:null
    #           imState:"threeDays"
    #           lastLogin:1497595353000
    #           pcShow:0
    #           plus:null
    #           promotionScoreExplain:null
    #           publisherId:68086
    #           score:0

                self.crawl(self.jobDetailBaseUrl + str(x['positionId']) + '.html', callback=self.detail_page, save=currentJobInfo)
            
            infoCount = content['positionResult']['totalCount']
            pageSize = content['pageSize']
            totalPageCount = math.ceil(infoCount / pageSize)
            nextPageNum = content['pageNo']+1
            print("total Page count", totalPageCount)
            
            if nextPageNum <= totalPageCount:
                self.data = {"first": "true", "pn": nextPageNum, "kd": self.search_word}
                self.crawl(self.ajax_url, params=self.params, method="POST", data=self.data, callback=self.json_info)
        else:
            print(response.json['success'], response.json['msg'])    
    #        [{"信息条数": response.json['content']['positionResult']['totalCount']},
    #        {"消息分析信息": response.json['content']['positionResult']['queryAnalysisInfo']},
    #        {"位置信息:": response.json['content']['positionResult']['locationInfo']},
    #        {"页面显示信息条数": response.json['content']['pageSize']},
    #        {"当前页": response.json['content']['pageNo']},
    #        ]
    
    
    @config(priority=2)
    def detail_page(self, response):
        info = response.save
        print(info['职位ID'])


        info.update({
            "url": response.url,
            "工作地址": response.doc('div.work_addr').text().replace(' 查看地图', ''),
            "职位描述": response.doc('dd.job_bt > div').text()
            })        
        return info


#    def on_result(self, result):
#        print(result)



    
             