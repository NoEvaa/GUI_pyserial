# -*- coding: utf-8 -*-
"""
Welcome to NPark
"""
import time
class workSTA():
    def __init__(self):
        self.score = [0, 0] #比分
        self.timerstate = 0 #计时器状态 0关 1开
        self.reload_clock = 2880 #倒计时-时钟-重装值 单位秒  48min=2880s 
        self.clock = self.reload_clock #倒计时-时钟
        self.last_response_time = 0 #计时器响应时间记录
    def main(self, stream, met = 1): #met: 1 串口数据流输入stream  0 程序参数输入stream
        if met:
            #单片机传来数据格式 '%d\r\n'
            #传入 stream<<'%d\r'
            idx = stream.split()
            if len(idx) == 0:
                return
            idx = idx[0]
        else:
            idx = stream
            
        if idx == '0': #一队加一
            self.score[0] += 1
            return
        if idx == '1': #一队加二
            self.score[0] += 2
            return
        if idx == '3': #二队加一
            self.score[1] += 1
            return
        if idx == '4': #二队加二
            self.score[1] += 2
            return
        if idx == '9': #清零
            self.score = [0, 0]
            return
        if idx == '10': #暂停
            self.timerstate = 0
            return
        if idx == '11': #开始(重新计时)
            self.clock = self.reload_clock
            self.last_response_time = time.time()
            self.timerstate = 1
            return
        if idx == '12': #继续
            self.last_response_time = time.time()
            self.timerstate = 1
            return
    
    def datapool(self): #数据池
        return self.score, self.timerstate, self.clock
    def realtime_event(self): #实时事件(倒计时更新)
        if self.timerstate:
            now_time = time.time()
            self.clock -= now_time - self.last_response_time
            self.last_response_time = now_time
        