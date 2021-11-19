# -*- coding: utf-8 -*-
"""
Welcome to NPark
"""
import PySimpleGUI as sg
import time
from pySerThread import SerComThread

def inner_window(exe_ope_list):
    inf_table = sg.Column([[sg.Text('倒计时:', font=('宋体', 40)),sg.T(' '  * 10), sg.Text('00 : 00', font=('宋体', 40), key='-Timer-')], 
                            [sg.T(' '  * 1)],[sg.T(' '  * 1)], 
                            [sg.T(' '  * 50),sg.Text('比分', font=('宋体', 40))], 
                            [sg.T(' '  * 1)],
                            [sg.Text('A队:', font=('宋体', 40)),sg.T(' '  * 20), sg.Text(font=('宋体', 40), key='-TeamA-')],
                            [sg.T(' '  * 1)],
                            [sg.Text('B队:', font=('宋体', 40)),sg.T(' '  * 20), sg.Text(font=('宋体', 40), key='-TeamB-')]])
    oper_table = sg.Column([[sg.Listbox(values=exe_ope_list, font=('宋体', 16), size=(30, 16), key='-LIST-', enable_events=True)], 
                            [sg.T(' '  * 1)],
                            [sg.T(' '  * 20), sg.Button('执行', size=(16, 3), font=('宋体', 12), key='-OPER-')], ])
    layout = [[sg.Text('当前时间:'), sg.Text(size=(20, 1), key='-TIME-')],
              [sg.T('   串口： '), sg.Button('开启', size=(10, 2), font=('宋体', 10), key='-Com-')],  
              [sg.T(' '  * 1)], 
              [sg.T(' '  * 1)], 
              [sg.T(' '  * 1)],
              [sg.T(' '  * 50), inf_table, sg.T(' '  * 40), oper_table],
              [sg.T(' '  * 1)], 
              [sg.T(' '  * 1)], 
              [sg.T(' '  * 1)],
              [sg.T(' '  * 10), sg.Button('开始', size=(10, 2), font=('宋体', 10), key='start'),sg.T(' '  * 10), sg.Button('暂停', size=(10, 2), font=('宋体', 10), key='suspend'),sg.T(' '  * 10), sg.Button('继续', size=(10, 2), font=('宋体', 10), key='continue')],
              ]

    return sg.Window('Score Indicator', layout, no_titlebar=True, finalize=True, right_click_menu=[[''], ['Exit',]])

oper_list = ['A队加一分','A队加二分','A队加三分','B队加一分'] #操作列表
win = inner_window(oper_list)
win.Maximize()
scom = SerComThread()

def get_countdown(cd): #计算倒计时时间 Output:  'min:sec'
    if cd <= 0:
        return '00:00'
    outp = ''
    m = int(cd/60)
    if m<10:
        outp += '0'
    outp += str(m)
    outp += ' : '
    s = int(cd-m*60)
    if s<10:
        outp += '0'
    outp += str(s)
    return outp

while True:
    scom.realtime_event()
    win['-TIME-'].update(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())) #更新时间
    sco, ti, ck = scom.datapool() #获取数据池
    #更新数据
    win['-TeamA-'].update(str(sco[0]))
    win['-TeamB-'].update(str(sco[1]))
    
    if ti:
        if ck <= 60: #小于60s倒计时变红
            win['-Timer-'].update(get_countdown(ck), text_color='red')
        else:
            win['-Timer-'].update(get_countdown(ck))
            
    event, values = win.read(timeout=100)
    if event == '-Com-': #串口开启&关闭
        if scom.ser_state:
            scom.stop()
            if scom.com_close():
                sg.popup_error("串口关闭失败")
                continue
            win['-Com-'].update('开启')
        else:
            if scom.com_open():
                sg.popup_error("串口开启失败")
                continue
            scom.run()
            win['-Com-'].update('关闭')
        continue
    elif event in (sg.WIN_CLOSED, 'Exit', None):
        scom.stop()
        scom.com_close()
        break
    elif event == '-OPER-':
        try:
            scom.main(str(oper_list.index(values['-LIST-'][0])), met=0)
        except:
            continue
    elif event == 'start':
        scom.main('11', 0)
        continue
    elif event == 'continue':
        scom.main('12', 0)
        continue
    elif event == 'suspend':
        scom.main('10', 0)
        continue

win.close()


