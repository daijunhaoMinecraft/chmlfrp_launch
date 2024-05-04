# -*- coding:utf-8 -*-
import time

import wx
from Taowa_wx import *
from Taowa_skin import *
import sys
import requests
import json
import os
from plyer import notification
import datetime
import platform
import psutil
import winreg
import subprocess
import threading
import re
message_time = 1
token = sys.argv[1]
id = sys.argv[2]
#获取当前路径
pathx = os.path.dirname(os.path.abspath(__file__))
#忽略证书警告
requests.packages.urllib3.disable_warnings()
#获取cpu型号
def getcpu():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DESCRIPTION\System\CentralProcessor\0')
    path = winreg.QueryValueEx(key, "ProcessorNameString")[0]
    return path
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}
#获取当前exe执行路径
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))

皮肤_加载(皮肤.Areo)

try:
    usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/tunnelinfo.php?id={id}",headers=headers,verify=False).text)
except Exception as e:
    notification.notify(title='出现错误', message=f'{e}', app_icon=f"{pathx}\\system_Error.ico", timeout=message_time)
    sys.exit()

class Frame(wx_Frame):
    def __init__(self):
        wx_Frame.__init__(self, None, title=f'隧道控制台-{usertunnel_info["tunnel_name"]}', size=(800, 600),name='frame',style=541072384)
        self.启动窗口 = wx_StaticText(self)
        self.Centre()
        self.标签1 = wx_StaticTextL(self.启动窗口,size=(736, 24),pos=(15, 20),label='当前隧道运行状态:',name='staticText',style=1)
        self.编辑框1 = wx_TextCtrl(self.启动窗口,size=(748, 418),pos=(20, 56),value='',name='text',style=1073745968)
        self.按钮1 = wx_Button(self.启动窗口,size=(80, 32),pos=(20, 496),label='停止隧道',name='button')
        self.按钮1.Bind(wx.EVT_BUTTON,self.按钮1_按钮被单击)
        self.按钮3 = wx_Button(self.启动窗口,size=(80, 32),pos=(113, 496),label='保存日志',name='button')
        self.按钮3.Bind(wx.EVT_BUTTON,self.按钮3_按钮被单击)
        self.按钮4 = wx_Button(self.启动窗口,size=(80, 32),pos=(211, 496),label='启动隧道',name='button')
        self.按钮4.Bind(wx.EVT_BUTTON,self.按钮4_按钮被单击)
        self.按钮5 = wx_Button(self.启动窗口,size=(80, 32),pos=(310, 496),label='重启隧道',name='button')
        self.按钮5.Bind(wx.EVT_BUTTON,self.按钮5_按钮被单击)
        notification.notify(title=f"隧道正在启动--{usertunnel_info['tunnel_name']}",message=f"隧道ip地址:{usertunnel_info['iparea']}", app_icon=f"{pathx}\\system_info.ico",timeout=message_time)
        self.编辑框1.AppendText(os.popen(f"@echo off&echo ChmlFrp日志信息 - {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}生成&echo 已自动屏蔽token内容&echo.&echo ===========设备信息==============&echo.&echo 系统/系统版本:{platform.platform()}&echo 操作系统位数:{platform.architecture()[0]}&echo 处理器信息:{getcpu()}&echo 机带RAM:{round(psutil.virtual_memory().total / (1024 ** 3))}GB&echo.&echo ===========隧道信息==============&echo.&echo 隧道ID:{usertunnel_info['tunnel_id']}&echo 隧道名称:{usertunnel_info['tunnel_name']}&echo 隧道类型:{usertunnel_info['tunnel_type']}&echo 内网IP:{usertunnel_info['tunnel_localip']}&echo 内网端口:{usertunnel_info['tunnel_nport']}&echo 外网端口/域名:{usertunnel_info['tunnel_dorp']}&echo 节点名称:{usertunnel_info['name']}&echo 连接地址:{usertunnel_info['iparea']}&echo.&echo ===========FRPC输出==============").read().encode("utf-8"))
        threading.Thread(target=self.start_frpc).start()
        self.按钮4.Disable()
        self.Bind(wx.EVT_CLOSE, self.on_close)
    def on_close(self,event):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(f"taskkill /PID {frpc_process_pid} /f", stdout=subprocess.PIPE, universal_newlines=True,startupinfo=startupinfo, encoding="gbk")
        self.Destroy()
    def frpc_stop(self):
        self.编辑框1.AppendText("frpc已终止!")
        self.按钮1.Disable()
        self.按钮4.Enable()
        self.按钮5.Disable()
        self.标签1.SetLabel("当前隧道运行状态(停止):")
    def start_frpc(self):
        global frpc_process_pid
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        process = subprocess.Popen(f"{pathx_pyinstaller}\\frpc.exe -u {token} -p {id}", stdout=subprocess.PIPE,universal_newlines=True,startupinfo=startupinfo, encoding="utf-8")
        self.按钮1.Enable()
        frpc_process_pid = process.pid
        # 逐行读取输出并过滤掉包含指定关键词的行
        for line in process.stdout:
            if token in line:
                self.标签1.SetLabel("当前隧道运行状态(运行中):")
                line = re.sub(rf'\[{token}-[\w]+\]', '\b', line)
                line = line.replace(f"{token}.", "")
                line = line.replace(f"{token}", "")
            if "映射启动成功" in line:
                self.标签1.SetLabel("当前隧道运行状态(映射启动成功):")
                notification.notify(title=f"隧道启动成功--{usertunnel_info['tunnel_name']}",message=f"隧道ip地址:{usertunnel_info['iparea']}",app_icon=f"{pathx}\\system_info.ico", timeout=message_time)
                self.编辑框1.AppendText(f"[信息]当前隧道启动成功,连接地址: {usertunnel_info['iparea']}\n")
                self.编辑框1.AppendText("")
            if "启动失败: proxy" in line:
                self.标签1.SetLabel("当前隧道运行状态(启动失败:proxy):")
                notification.notify(title=f"隧道启动失败--{usertunnel_info['tunnel_name']}",message=f"隧道启动失败,原因:proxy(端口被占用)\n请检查你的隧道是否是运行状态,frp日志:\n",app_icon=f"{pathx}\\system_Error.ico", timeout=message_time)
                self.编辑框1.AppendText("[错误]当前隧道出现错误:proxy(端口被占用)\n请检查你的隧道是否是运行状态")
            if "无法连接至服务器" in line:
                self.按钮1.Disable()
                self.按钮4.Enable()
                self.按钮5.Disable()
                self.标签1.SetLabel("当前隧道运行状态(启动失败:无法连接至服务器):")
                notification.notify(title=f"隧道启动失败--{usertunnel_info['tunnel_name']}",message=f"隧道启动失败,原因:无法连接至服务器\n请检查你的节点是否是在线状态,请检查你的网络\n实在不行就去换节点,frp报错:\n",app_icon=f"{pathx}\\system_Error.ico", timeout=message_time)
                self.编辑框1.AppendText("[错误]当前隧道出现错误:无法连接至服务器\n请检查你的节点是否是在线状态,请检查你的网络是否连接\n实在不行就去换节点,frp日志:\n")
            self.编辑框1.AppendText(line.replace("",""))  # 输出处理后的行
        process.wait()
        threading.Thread(target=self.frpc_stop).start()

    def 按钮1_按钮被单击(self,event):
        taskkill_os_ok_warm = wx.MessageDialog(None, caption="警告",message=f"确定要停止隧道?",style=wx.YES_NO | wx.ICON_WARNING)
        if taskkill_os_ok_warm.ShowModal() == wx.ID_YES:
            taskkill_os_ok = os.popen(f"taskkill /PID {frpc_process_pid} /f").read()
            notification.notify(title=f"隧道已停止--{usertunnel_info['tunnel_name']}",message=f"{taskkill_os_ok}", app_icon=f"{pathx}\\system_info.ico",timeout=message_time)
            taskkill_os_ok_info = wx.MessageDialog(None, caption="info",message=f"当前停止隧道命令执行状态:\n{taskkill_os_ok}",style=wx.OK | wx.ICON_INFORMATION)
            if taskkill_os_ok_info.ShowModal() == wx.ID_OK:
                pass


    def 按钮3_按钮被单击(self,event):
        wildcard = "Text files (*.log)|*.log|Text files (*.txt)|*.txt|All files (*.*)|*.*"
        dlg = wx.FileDialog(self, message="请选择一个文件夹用于保存日志",defaultFile=f"chmlfrp隧道启动日志-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log", wildcard=wildcard,style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
        if dlg.ShowModal() == wx.ID_OK:
            with open(dlg.GetPath(),mode="w",encoding="utf-8") as f:
                f.write(self.编辑框1.GetValue())
            save_log_ok = wx.MessageDialog(None, caption="info",message="保存日志成功",style=wx.OK | wx.ICON_INFORMATION)
            if save_log_ok.ShowModal() == wx.ID_OK:
                pass

    def 按钮4_按钮被单击(self,event):
        self.按钮5.Enable()
        self.编辑框1.SetLabel("")
        self.标签1.SetLabel("当前隧道运行状态:")
        notification.notify(title=f"隧道正在启动--{usertunnel_info['tunnel_name']}",message=f"隧道ip地址:{usertunnel_info['iparea']}", app_icon=f"{pathx}\\system_info.ico",timeout=message_time)
        self.编辑框1.AppendText(os.popen(f"@echo off&echo ChmlFrp日志信息 - {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}生成&echo 已自动屏蔽token内容&echo.&echo ===========设备信息==============&echo.&echo 系统/系统版本:{platform.platform()}&echo 操作系统位数:{platform.architecture()[0]}&echo 处理器信息:{getcpu()}&echo 机带RAM:{round(psutil.virtual_memory().total / (1024 ** 3))}GB&echo.&echo ===========隧道信息==============&echo.&echo 隧道ID:{usertunnel_info['tunnel_id']}&echo 隧道名称:{usertunnel_info['tunnel_name']}&echo 隧道类型:{usertunnel_info['tunnel_type']}&echo 内网IP:{usertunnel_info['tunnel_localip']}&echo 内网端口:{usertunnel_info['tunnel_nport']}&echo 外网端口/域名:{usertunnel_info['tunnel_dorp']}&echo 节点名称:{usertunnel_info['name']}&echo 连接地址:{usertunnel_info['iparea']}&echo.&echo ===========FRPC输出==============").read().encode("utf-8"))
        threading.Thread(target=self.start_frpc).start()
        self.按钮4.Disable()


    def 按钮5_按钮被单击(self,event):
        reset_frpc_info = wx.MessageDialog(None, caption="警告",message=f"确定要重启隧道?",style=wx.YES_NO | wx.ICON_WARNING)
        if reset_frpc_info.ShowModal() == wx.ID_YES:
            self.标签1.SetLabel("当前隧道运行状态:")
            self.按钮4.Disable()
            notification.notify(title=f"隧道正在启动--{usertunnel_info['tunnel_name']}",message=f"隧道ip地址:{usertunnel_info['iparea']}", app_icon=f"{pathx}\\system_info.ico",timeout=message_time)
            self.编辑框1.AppendText(os.popen(f"@echo off&echo ChmlFrp日志信息 - {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}生成&echo 已自动屏蔽token内容&echo.&echo ===========设备信息==============&echo.&echo 系统/系统版本:{platform.platform()}&echo 操作系统位数:{platform.architecture()[0]}&echo 处理器信息:{getcpu()}&echo 机带RAM:{round(psutil.virtual_memory().total / (1024 ** 3))}GB&echo.&echo ===========隧道信息==============&echo.&echo 隧道ID:{usertunnel_info['tunnel_id']}&echo 隧道名称:{usertunnel_info['tunnel_name']}&echo 隧道类型:{usertunnel_info['tunnel_type']}&echo 内网IP:{usertunnel_info['tunnel_localip']}&echo 内网端口:{usertunnel_info['tunnel_nport']}&echo 外网端口/域名:{usertunnel_info['tunnel_dorp']}&echo 节点名称:{usertunnel_info['name']}&echo 连接地址:{usertunnel_info['iparea']}&echo.&echo ===========FRPC输出==============").read().encode("utf-8"))
            threading.Thread(target=self.start_frpc).start()

class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()
