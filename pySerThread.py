# -*- coding: utf-8 -*-
"""
Welcome to NPark
"""
import serial
import threading
import time
from workstation import workSTA
class SerComThread(workSTA):
    def __init__(self):
        workSTA.__init__(self) #工作站
        self.ser = serial.Serial()
        #配置
        self.ser.port = 'COM3' #串口号
        self.ser.baudrate = 9600 #波特率
        self.ser.bytesize = 8 #数据长度
        self.ser.parity = serial.PARITY_NONE
        self.ser.stopbits = 1 #停止位
        
        self.ser_state = False #串口开启状态 F未开启 T开启
        self.termflag = False #终止信号 为F时所有线程终止
        self.recv_stream = '' #数据接收流
        self.recv_state = 0 #串口接收状态
        
        self.processes = None #线程列表
    def __del__(self):
        self.stop()
        self.com_close()
    def com_open(self): #开启串口
        if self.ser_state:
            return 0
        try:
            self.ser.open() #开启串口
            self.ser_state = True
        except:
            return 1
        return 0
    def com_close(self): #关闭串口
        if not self.ser_state:
            return 0
        try:
            self.ser_state = False
            self.ser.close()
        except:
            return 1
        return 0
    def com_receive(self, flag): #串口接收数据线程
        if flag:
            return
        while self.termflag:
            stream = ''
            while self.ser_state:
                #接收串口通信发来的数据流方式
                ch = self.ser.read() # 只收一个bytes
                if ch.decode(encoding='ascii') == '\n': #回车终止
                    self.recv_stream = stream #保存数据流
                    self.recv_state = True #更改接收状态
                    break
                stream += ch.decode(encoding='ascii')
                
            while self.recv_state:
                time.sleep(0.01)
            #self.ser.flushInput()
    def stream_process(self, flag): #串口接收数据线程
        if flag:
            return
        while self.termflag:
            if self.recv_state:
                stream = self.recv_stream #保存数据流
                self.recv_state = False #继续接收数据流
                self.main(stream) #处理数据流>>>workstation.workSTA.main
            else:
                time.sleep(0.001)
            
    def run(self): #运行线程
        if self.termflag:
            return
        self.termflag = True
        self.processes = [threading.Thread(target=self.com_receive, args=(0,)),
                          threading.Thread(target=self.stream_process, args=(0,)),
                          ]

        [process.start() for process in self.processes]
        print("Start all Process")
        
    def stop(self): #终止线程
        if not self.termflag:
            return
        self.termflag = False
        print("Stop all Process")
        self.processes = None
if __name__ == '__main__':
    scom = SerComThread()
    scom.com_open()
    scom.run()
    print(scom.termflag,scom.ser_state)
    while 1:
        print(scom.recv_state, scom.recv_stream)
        time.sleep(0.5)
        if scom.recv_state:
            scom.recv_state = False
    scom.stop()
    scom.com_close()