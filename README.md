# GUI_pyserial
python+PySimpleGUI+pyserial+threading

## 功能

1.利用PySimpleGUI制作图形用户界面

2.利用threading实现多线程调用pyserial处理串口通信

## 模块版本

PySimpleGUI 4.46.0

pyserial 3.5

## 使用方式

1.运行 serUI.py 文件

## 目录结构描述

├── README.md          // help

├── serUI.py           // UI界面

├── pySerThread.py     // 多线程串口通信

└── workstation.py     // 数据处理及反馈

## 开发

1.如需修改UI界面请更改serUI.py

2.串口通信配置调整需更改pySerThread.py

3.workstation.py对串口通信接收数据进行处理并提供更新和呼叫数据池的方式

4.pySerThread.py中隐藏了多线程串口通信实现细节，可以通过另外两个文件的调整直接实现用户界面

<br><br><br>
[NoEVaa](https://github.com/NoEvaa "悬停显示")
<br>
[NPark](https://github.com/NoEvaa "悬停显示")
