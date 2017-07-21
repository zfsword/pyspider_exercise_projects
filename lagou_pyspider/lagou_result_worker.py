# -*- coding:utf-8 -*-

from pyspider.result import ResultWorker


class LagouResultWorker(ResultWorker):

    def on_result(self, task, result):
        assert task['taskid']
        assert task['project']
        assert task['url']
        assert result # your processing code goes here 
