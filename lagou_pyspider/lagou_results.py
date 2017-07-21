# coding:utf-8 -*-

from pyspider.database import connect_database


mongodbURI = "mongodb+resultdb://resultUser:nGd6MTbqApc1ZRH3wGhN@localhost:27017/resultdb"
resultdb = connect_database(mongodbURI)

for project in resultdb.projects:
    for result in resultdb.select(project):
        assert result['taskid']
        assert result['url']
        assert result['result']
