# -*- coding:utf-8 -*-
import json
import time

import requests
import wx
from wx.html2 import WebView
import sys
import os
import pyperclip3 as pycopy
import winreg
import random
import string
import datetime
import platform
import psutil
#忽略证书警告
requests.packages.urllib3.disable_warnings()
#获取当前路径
pathx = os.path.dirname(os.path.abspath(__file__))
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}
#获取当前计算机文档路径

def Personal():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Personal")[0]
    return path
def getcpu():
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r'HARDWARE\DESCRIPTION\System\CentralProcessor\0')
    path = winreg.QueryValueEx(key, "ProcessorNameString")[0]
    return path
#获取登录信息
chmlfrp_user_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/userinfo.php?usertoken={sys.argv[1]}",headers=headers,verify=False).text)
#用户主界面



class chmlfrp_user(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        try:
            if chmlfrp_user_info['username']:
                user_token_login_OK = wx.MessageDialog(None, caption="info",message=f"登录成功,登录账号:{chmlfrp_user_info['username']}",style=wx.OK | wx.ICON_INFORMATION)
                if user_token_login_OK.ShowModal() == wx.ID_OK:
                    pass
        except KeyError:
            user_token_login_Error = wx.MessageDialog(None, caption="Error", message=f"{chmlfrp_user_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if user_token_login_Error.ShowModal() == wx.ID_OK:
                sys.exit()

        self.标签1 = wx.StaticText(self,size=(80, 24),pos=(7, 25),label='用户名:',name='staticText',style=2321)
        self.chmlfrp_user = wx.TextCtrl(self,size=(285, 22),pos=(91, 22),value='',name='text',style=16)
        self.chmlfrp_user.SetLabel(f"{chmlfrp_user_info['username']}")
        self.user_email = wx.StaticText(self,size=(80, 24),pos=(9, 60),label='用户邮箱:',name='staticText',style=2321)
        self.chmlfrp_email = wx.TextCtrl(self,size=(285, 22),pos=(91, 61),value='',name='text',style=16)
        self.chmlfrp_email.SetLabel(f"{chmlfrp_user_info['email']}")
        self.chmlfrp_qq = wx.TextCtrl(self,size=(285, 22),pos=(91, 98),value='',name='text',style=16)
        self.chmlfrp_qq.SetLabel(f"{chmlfrp_user_info['qq']}")
        self.标签3 = wx.StaticText(self,size=(80, 24),pos=(9, 97),label='用户QQ号:',name='staticText',style=2321)
        self.chmlfrp_user_img = wx.StaticBitmap(self,size=(40, 40),pos=(1097, 28),name='staticBitmap',style=33554432)
        #获取用户头像
        chmlfrp_user_img = requests.get(f"{chmlfrp_user_info['userimg']}",headers=headers,verify=False).content
        with open(f"{pathx}\\temp.png",mode="wb") as f:
            f.write(chmlfrp_user_img)
            f.close()
        chmlfrp_user_icon_图片 = wx.Image(f"{pathx}\\temp.png").ConvertToBitmap()
        self.chmlfrp_user_img.SetBitmap(wx.BitmapFromImage(chmlfrp_user_icon_图片))
        #获取签到状态
        qd = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/qdxx.php?userid={chmlfrp_user_info['userid']}",verify=False,headers=headers).text)
        if qd['is_signed_in_today'] == True:
            qd_info = f"今天已经签到了\n累计签到次数:{qd['total_sign_ins']}次\n累计签到获得的积分:{qd['total_points']}分\n今天一共签到的人数:{qd['count_of_matching_records']}人\n你的上一次签到时间为:{qd['last_sign_in_time']}"
        if qd['is_signed_in_today'] == False:
            qd_info = f"今天还未签到\n累计签到次数:{qd['total_sign_ins']}次\n累计签到获得的积分:{qd['total_points']}分\n今天一共签到的人数:{qd['count_of_matching_records']}人\n你的上一次签到时间为:{qd['last_sign_in_time']}"
        self.chmlfrp_info = wx.TextCtrl(self,size=(366, 249),pos=(7, 151),value=f'当前用户id:{str(chmlfrp_user_info["userid"])}\n当前用户组:{str(chmlfrp_user_info["usergroup"])}\n到期时间:{chmlfrp_user_info["term"]}\n当前用户创建隧道的数量:{chmlfrp_user_info["tunnel"]}\n当前用户宽带限制(国内):{chmlfrp_user_info["bandwidth"]}\n当前用户实名状态:{chmlfrp_user_info["realname"]}\n当前用户积分数:{str(chmlfrp_user_info["integral"])}\n{qd_info}',name='text',style=1073741872)
        self.标签4 = wx.StaticText(self,size=(191, 24),pos=(7, 414),label='userinfo返回json(小白请无视):',name='staticText',style=17)
        self.debug_json_user_info = wx.TextCtrl(self,size=(366, 201),pos=(7, 447),value=f'{chmlfrp_user_info}',name='text',style=wx.TE_READONLY | wx.TE_MULTILINE | wx.TE_AUTO_URL)
        self.resusertoken = wx.Button(self, size=(80, 32), pos=(7, 664), label='重置token', name='button')
        self.resusertoken.SetForegroundColour((255, 0, 0, 255))
        self.resusertoken.Bind(wx.EVT_BUTTON, self.resusertoken_按钮被单击)
        self.标签5 = wx.StaticText(self, size=(106, 24), pos=(405, 22), label='当前登录用户token:',name='staticText', style=0)
        self.编辑框6 = wx.TextCtrl(self, size=(305, 22), pos=(521, 21), value='', name='text', style=wx.TE_PASSWORD | wx.TE_READONLY)
        self.编辑框6_show = wx.TextCtrl(self, size=(305, 22), pos=(521, 21), value='', name='text', style=wx.TE_READONLY)
        self.编辑框6.SetLabel(f"{sys.argv[1]}")
        self.编辑框6_show.SetLabel(f"{sys.argv[1]}")
        self.编辑框6_show.Hide()
        self.copy_token = wx.Button(self, size=(80, 32), pos=(931, 17), label='复制token', name='button')
        self.copy_token.Bind(wx.EVT_BUTTON, self.copy_token_按钮被单击)
        self.display_token = wx.CheckBox(self, size=(84, 24), pos=(838, 20), name='check', label='显示token',style=16384)
        self.display_token.Bind(wx.EVT_CHECKBOX, self.display_token_狀态被改变)
        self.标签6 = wx.StaticText(self, size=(352, 24), pos=(819, 721), label='', name='staticText', style=0)

    #重置用户token
    def resusertoken_按钮被单击(self, event):
        resusertoken_warm = wx.MessageDialog(None, caption="警告", message="你确定要重置token吗?",style=wx.YES_NO | wx.ICON_WARNING)
        if resusertoken_warm.ShowModal() == wx.ID_YES:
            resusertoken_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/resusertoken.php?usertoken={sys.argv[1]}",headers=headers,verify=False).text)
            with open(f"{Personal()}\\chmlfrp_token.json", mode="w", encoding="utf-8") as f:
                data = {
                    "token": f"{resusertoken_info['newToken']}"
                }
                f.write(json.dumps(data, indent=4, ensure_ascii=False))
                f.close()
            resusertoken_ok = wx.MessageDialog(None, caption="info", message=f"用户token重置完成,自动登录token已刷新,请重新打开程序,点击OK则程序退出\n新的token:{resusertoken_info['newToken']}",style=wx.OK | wx.ICON_INFORMATION)
            if resusertoken_ok.ShowModal() == wx.ID_OK:
                sys.exit()

    def display_token_狀态被改变(self,event):
        if self.display_token.GetValue() == True:
            self.display_token.SetValue(False)
            chmlfrp_display_token_warm = wx.MessageDialog(None, caption="警告",message="你确定要显示token?\n请不要随意将token发送给任何人!",style=wx.YES_NO | wx.ICON_WARNING)
            if chmlfrp_display_token_warm.ShowModal() == wx.ID_YES:
                self.display_token.SetValue(True)
                self.编辑框6.Hide()
                self.编辑框6_show.Show()
            else:
                self.display_token.SetValue(False)
        elif self.display_token.GetValue() == False:
            self.编辑框6.Show()
            self.编辑框6_show.Hide()


    def copy_token_按钮被单击(self,event):
        pycopy.copy(f"{sys.argv[1]}")
        chmlfrp_token_copy_ok = wx.MessageDialog(None, caption="信息", message="token复制成功\n请不要随意发给任何人!",style=wx.OK | wx.ICON_INFORMATION)
        if chmlfrp_token_copy_ok.ShowModal() == wx.ID_OK:
            pass

#启动隧道
class chmlfrp_start_usertunnel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.usertunnel_list = wx.ListBox(self, size=(1113, 312), pos=(15, 41), name='listBox', choices=[],style=1073741856)
        self.usertunnel_list.Bind(wx.EVT_LISTBOX_DCLICK, self.usertunnel_list_表项被双击)
        self.标签1 = wx.StaticText(self, size=(141, 24), pos=(15, 13), label='当前隧道列表(双击选择):',name='staticText', style=2321)
        self.frpc_config = wx.TextCtrl(self, size=(396, 339), pos=(107, 381), value='', name='text',style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_AUTO_URL)
        self.标签3 = wx.StaticText(self, size=(80, 24), pos=(15, 381), label='当前隧道配置:',name='staticText', style=2321)
        self.start_usertunnel = wx.Button(self, size=(224, 85), pos=(527, 381), label='启动隧道',name='button')
        start_usertunnel_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.start_usertunnel.SetFont(start_usertunnel_字体)
        self.start_usertunnel.Bind(wx.EVT_BUTTON, self.start_usertunnel_按钮被单击)
        self.start_usertunnel.Disable()
        self.flushed_usertunnel = wx.Button(self, size=(80, 32), pos=(1048, 370), label='刷新隧道',name='button')
        self.flushed_usertunnel.Bind(wx.EVT_BUTTON, self.flushed_usertunnel_按钮被单击)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            #获取用户隧道
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
        except KeyError:
            pass
    def usertunnel_list_表项被双击(self, event):
        #获取隧道配置
        global usertunnel_info_config_frpc
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        self.start_usertunnel.Enable()
        usertunnel_info_config_frpc = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/frpconfig.php?usertoken={sys.argv[1]}&node={usertunnel_info[self.usertunnel_list.GetSelection()]['node']}").text)['message']
        self.frpc_config.SetLabel(usertunnel_info_config_frpc)

    def start_usertunnel_按钮被单击(self, event):
        #启动隧道
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        with open(f"{pathx}\\frpc.ini",mode="w",encoding="utf-8") as f:
            f.write(usertunnel_info_config_frpc)
            f.close()
        os.system(f"start cmd /c \"@echo off&echo ChmlFrp日志信息 - {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}生成&echo.&echo ===========设备信息==============&echo.&echo 系统/系统版本:{platform.platform()}&echo 操作系统位数:{platform.architecture()[0]}&echo 处理器信息:{getcpu()}&echo 机带RAM:{round(psutil.virtual_memory().total / (1024**3))}GB&echo.&echo ===========隧道信息==============&echo.&echo 隧道ID:{usertunnel_info[self.usertunnel_list.GetSelection()]['id']}&echo 隧道名称:{usertunnel_info[self.usertunnel_list.GetSelection()]['name']}&echo 隧道类型:{usertunnel_info[self.usertunnel_list.GetSelection()]['type']}&echo 内网IP:{usertunnel_info[self.usertunnel_list.GetSelection()]['localip']}&echo 内网端口:{usertunnel_info[self.usertunnel_list.GetSelection()]['nport']}&echo 外网端口/域名:{usertunnel_info[self.usertunnel_list.GetSelection()]['dorp']}&echo 节点:{usertunnel_info[self.usertunnel_list.GetSelection()]['node']}&echo 连接地址:{usertunnel_info[self.usertunnel_list.GetSelection()]['ip']}&echo.&echo ===========FRPC输出==============&{pathx}\\frpc.exe -u {sys.argv[1]} -p {usertunnel_info[self.usertunnel_list.GetSelection()]['id']}&echo frpc已终止,按任意键退出&pause\"")
        user_usertunnel_OK = wx.MessageDialog(None, caption="info",message=f"已执行隧道启动命令,是否复制ip?",style=wx.YES_NO | wx.ICON_INFORMATION)
        if user_usertunnel_OK.ShowModal() == wx.ID_YES:
            pycopy.copy(usertunnel_info[self.usertunnel_list.GetSelection()]['ip'])
            copy_ok = wx.MessageDialog(None, caption="info", message=f"ip复制完成",style=wx.OK | wx.ICON_INFORMATION)
            if copy_ok.ShowModal() == wx.ID_OK:
                pass

    def flushed_usertunnel_按钮被单击(self, event):
        #刷新隧道
        self.usertunnel_list.Clear()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
        except KeyError:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"{usertunnel_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成", style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass
#删除隧道
class chmlfrp_delete_usertunnel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.usertunnel_list = wx.ListBox(self, size=(1113, 312), pos=(15, 41), name='listBox', choices=[],style=1073741856)
        self.usertunnel_list.Bind(wx.EVT_LISTBOX_DCLICK, self.usertunnel_list_表项被双击)
        self.标签1 = wx.StaticText(self, size=(141, 24), pos=(15, 13), label='当前隧道列表(双击选择):',name='staticText', style=2321)
        self.frpc_config = wx.TextCtrl(self, size=(396, 339), pos=(107, 381), value='', name='text',style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_AUTO_URL)
        self.标签3 = wx.StaticText(self, size=(80, 24), pos=(15, 381), label='当前隧道配置:',name='staticText', style=2321)
        self.delete_usertunnel = wx.Button(self, size=(224, 85), pos=(527, 381), label='删除隧道',name='button')
        delete_usertunnel_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.delete_usertunnel.SetFont(delete_usertunnel_字体)
        self.delete_usertunnel.Bind(wx.EVT_BUTTON, self.delete_usertunnel_按钮被单击)
        self.delete_usertunnel.Disable()
        self.delete_usertunnel.SetForegroundColour((255, 0, 0, 255))
        self.flushed_usertunnel = wx.Button(self, size=(80, 32), pos=(1048, 370), label='刷新隧道',name='button')
        self.flushed_usertunnel.Bind(wx.EVT_BUTTON, self.flushed_usertunnel_按钮被单击)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            #获取当前用户隧道
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
        except KeyError:
            pass
    def usertunnel_list_表项被双击(self, event):
        #获取隧道配置
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        self.delete_usertunnel.Enable()
        usertunnel_info_config_frpc = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/frpconfig.php?usertoken={sys.argv[1]}&node={usertunnel_info[self.usertunnel_list.GetSelection()]['node']}").text)['message']
        self.frpc_config.SetLabel(usertunnel_info_config_frpc)

    def delete_usertunnel_按钮被单击(self, event):
        #删除隧道
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        delete_warm = wx.MessageDialog(None, caption="警告", message="你确定要删除此隧道吗?",style=wx.YES_NO | wx.ICON_WARNING)
        if delete_warm.ShowModal() == wx.ID_YES:
            delete_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/deletetl.php?token={sys.argv[1]}&nodeid={usertunnel_info[self.usertunnel_list.GetSelection()]['id']}&userid={str(chmlfrp_user_info['userid'])}",headers=headers,verify=False).text)
            self.usertunnel_list.Clear()
            #再次获取隧道,避免删除的隧道重复删除
            usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
            try:
                for i in range(len(usertunnel_info)):
                    if str(usertunnel_info[i]['nodestate']) == "offline":
                        self.usertunnel_list.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                    if str(usertunnel_info[i]['nodestate']) == "online":
                        self.usertunnel_list.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
            except KeyError:
                pass
            self.delete_usertunnel.Disable()
            self.frpc_config.SetLabel("")
            delete_info_message = wx.MessageDialog(None, caption="删除状态", message=f"{delete_info['error']}",style=wx.OK | wx.ICON_INFORMATION)
            if delete_info_message.ShowModal() == wx.ID_YES:
                pass

    def flushed_usertunnel_按钮被单击(self, event):
        #刷新隧道
        self.usertunnel_list.Clear()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
        except KeyError:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"{usertunnel_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成", style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass
#创建隧道
class chmlfrp_create_usertunnel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        global unode
        self.列表框1 = wx.ListBox(self, size=(1103, 261), pos=(27, 51), name='listBox', choices=[], style=1073741856)
        self.列表框1.Bind(wx.EVT_LISTBOX_DCLICK,self.列表框1_表项被双击)
        self.标签1 = wx.StaticText(self, size=(222, 24), pos=(27, 20),label='当前节点列表(双击选择创建的隧道节点):', name='staticText', style=17)
        self.标签2 = wx.StaticText(self, size=(80, 24), pos=(26, 339), label='隧道名称:', name='staticText',style=2321)
        self.usertunnel_name = wx.TextCtrl(self, size=(291, 22), pos=(119, 339), value='', name='text',style=0)
        self.标签3 = wx.StaticText(self, size=(80, 24), pos=(26, 382), label='隧道ip:', name='staticText',style=2321)
        self.标签4 = wx.StaticText(self, size=(80, 24), pos=(26, 426), label='隧道内网端口:',name='staticText', style=2321)
        self.usertunnel_n_port = wx.TextCtrl(self, size=(291, 22), pos=(119, 427), value='', name='text',style=0)
        self.usertunnel_ip = wx.TextCtrl(self, size=(291, 22), pos=(119, 381), value='', name='text', style=0)
        self.chmlfrp_type = wx.RadioBox(self,size=(250, 60),pos=(26, 466),label='隧道端口类型',choices=['tcp', 'udp', 'http', 'https'],majorDimension=0,name='radioBox',style=4)
        self.chmlfrp_type.Bind(wx.EVT_RADIOBOX,self.chmlfrp_type_选项被单击)
        self.标签5 = wx.StaticText(self,size=(120, 24),pos=(26, 545),label='请输入外网端口:',name='staticText',style=2304)
        self.usertunnel_w_port = wx.TextCtrl(self,size=(291, 22),pos=(155, 544),value='',name='text',style=0)
        self.encryption = wx.CheckBox(self, size=(80, 24), pos=(589, 336), name='check', label='数据加密',style=16384)
        self.标签8 = wx.StaticText(self, size=(80, 24), pos=(503, 339), label='高级设置:', name='staticText',style=2321)
        self.compression = wx.CheckBox(self, size=(80, 24), pos=(589, 364), name='check', label='数据压缩',style=16384)
        self.ap = wx.TextCtrl(self, size=(297, 22), pos=(674, 401), value='', name='text', style=0)
        self.ap.Bind(wx.EVT_TEXT, self.ap_内容被改变)
        self.标签9 = wx.StaticText(self, size=(80, 24), pos=(589, 401), label='额外参数:', name='staticText',style=2321)
        self.create_usertunnel = wx.Button(self, size=(174, 75), pos=(26, 632), label='创建隧道',name='button')
        create_usertunnel_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.create_usertunnel.SetFont(create_usertunnel_字体)
        self.create_usertunnel.Bind(wx.EVT_BUTTON, self.create_usertunnel_按钮被单击)
        self.create_usertunnel.Disable()
        self.按钮2 = wx.Button(self, size=(80, 32), pos=(1050, 325), label='刷新节点', name='button')
        self.按钮2.Bind(wx.EVT_BUTTON, self.按钮2_按钮被单击)
        self.Domain_name_query = wx.Button(self,size=(108, 32),pos=(456, 539),label='域名解析查询',name='button')
        self.Domain_name_query.Hide()
        self.Domain_name_query.Disable()
        self.Domain_name_query.Bind(wx.EVT_BUTTON,self.Domain_name_query_按钮被单击)
        self.标签10 = wx.StaticText(self, size=(418, 24), pos=(26, 587),label='tips:域名解析查询和创建隧道还有随机外网端口都需要选择节点才可以进行操作', name='staticText',style=2304)
        self.random_name_usertunnel = wx.Button(self, size=(86, 32), pos=(418, 334), label='随机隧道名称',name='button')
        self.random_name_usertunnel.Bind(wx.EVT_BUTTON, self.random_name_usertunnel_按钮被单击)
        self.random_w_port = wx.Button(self,size=(96, 32),pos=(350, 499),label='随机外网端口',name='button')
        self.random_w_port.Bind(wx.EVT_BUTTON,self.random_w_port_按钮被单击)
        self.random_w_port.Disable()
        #获取节点
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        for i in range(len(unode)):
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                self.列表框1.Append(str(i + 1) + ".[国内节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                self.列表框1.Append(str(i + 1) + ".[国内VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                self.列表框1.Append(str(i + 1) + ".[国外节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                self.列表框1.Append(str(i + 1) + ".[国外VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
        self.usertunnel_ip.SetLabel("127.0.0.1")
    def 列表框1_表项被双击(self,event):
        self.create_usertunnel.Enable()
        self.Domain_name_query.Enable()
        self.random_w_port.Enable()

    def random_w_port_按钮被单击(self,event):
        unode_w_port = f"{unode[self.列表框1.GetSelection()]['rport']}".split("-")
        self.usertunnel_w_port.SetLabel(str(random.randint(int(unode_w_port[0]), int(unode_w_port[1]))))

    def random_name_usertunnel_按钮被单击(self,event):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 30)))
        self.usertunnel_name.SetLabel(random_str)

    def Domain_name_query_按钮被单击(self,event):
        Domain_name_query_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/Domain_name_query.php?domain={self.usertunnel_w_port.GetValue()}&target_domain={unode[self.列表框1.GetSelection()]['ip']}",headers=headers,verify=False).text)
        if Domain_name_query_info['status'] == "success":
            if Domain_name_query_info['hasSrvToFrpOne'] == False:
                Domain_name_query_srv = "解析失败"
            elif Domain_name_query_info['hasSrvToFrpOne'] == True:
                Domain_name_query_srv = "解析成功"
            if Domain_name_query_info['hasCnameToFrpOne'] == False:
                Domain_name_query_cname = "解析失败"
            elif Domain_name_query_info['hasCnameToFrpOne'] == True:
                Domain_name_query_cname = "解析成功"
            Domain_name_query_ok = wx.MessageDialog(None, caption="info", message=f"解析成功!\n当前节点对此域名进行Srv解析状态:{Domain_name_query_srv}\n当前节点对此域名进行cname解析状态:{Domain_name_query_cname}",style=wx.OK | wx.ICON_INFORMATION)
            if Domain_name_query_ok.ShowModal() == wx.ID_OK:
                pass
        elif Domain_name_query_info['status'] == "error":
            Domain_name_query_Error = wx.MessageDialog(None, caption="info",message=f"解析失败!\n{Domain_name_query_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if Domain_name_query_Error.ShowModal() == wx.ID_OK:
                pass


    def chmlfrp_type_选项被单击(self,event):
        if self.chmlfrp_type.GetSelection() == 3:
            self.标签5.SetLabel("请输入你的https域名:")
            self.Domain_name_query.Show()

        elif self.chmlfrp_type.GetSelection() == 2:
            self.标签5.SetLabel("请输入你的http域名:")
            self.Domain_name_query.Show()

        elif self.chmlfrp_type.GetSelection() == 0 or self.chmlfrp_type.GetSelection() == 1:
            self.标签5.SetLabel("请输入外网端口:")
            self.Domain_name_query.Hide()

    def ap_内容被改变(self, event):
        self.encryption.SetValue(True)
        self.compression.SetValue(True)

    def create_usertunnel_按钮被单击(self, event):
        if self.encryption.GetValue() == True:
            encryption = "true"
        elif self.encryption.GetValue() == False:
            encryption = "false"
        if self.compression.GetValue() == True:
            compression = "true"
        elif self.compression.GetValue() == False:
            compression = "false"
        if self.chmlfrp_type.GetSelection() == 0:
            chmlfrp_type = "tcp"
        elif self.chmlfrp_type.GetSelection() == 1:
            chmlfrp_type = "udp"
        elif self.chmlfrp_type.GetSelection() == 2:
            chmlfrp_type = "http"
        elif self.chmlfrp_type.GetSelection() == 3:
            chmlfrp_type = "https"
        if self.chmlfrp_type.GetSelection() == 0 or self.chmlfrp_type.GetSelection() == 1:
            chmlfrp_domainNameLabel = ""
        elif self.chmlfrp_type.GetSelection() == 2 or self.chmlfrp_type.GetSelection() == 3:
            chmlfrp_domainNameLabel = "自定义"
        try:
            #创建隧道请求内容
            data = {
                      "token": f"{sys.argv[1]}",
                      "userid": int(chmlfrp_user_info["userid"]),
                      "localip": f"{self.usertunnel_ip.GetValue()}",
                      "name": f"{self.usertunnel_name.GetValue()}",
                      "node": f"{unode[self.列表框1.GetSelection()]['name']}",
                      "type": f"{chmlfrp_type}",
                      "nport": f"{self.usertunnel_n_port.GetValue()}",
                      "dorp": f"{self.usertunnel_w_port.GetValue()}",
                      "ap": f"{self.ap.GetValue()}",
                      "domainNameLabel": f"{chmlfrp_domainNameLabel}",
                      "choose": "",
                      "encryption": f"{encryption}",
                      "compression": f"{compression}"
                    }
        except ValueError as e:
            user_create_Error = wx.MessageDialog(None, caption="Error", message=f"创建失败,原因可能出现在外网端口上,错误信息:{e}",style=wx.OK | wx.ICON_ERROR)
            if user_create_Error.ShowModal() == wx.ID_OK:
                pass
        #创建隧道请求头
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            "Accept": "application/json, text/plain, */*",
            "HTTP_TOKEN": f"{sys.argv[1]}"
        }
        #创建隧道post请求
        create_info = json.loads(requests.post("https://panel.chmlfrp.cn/api/tunnel.php",json=data,headers=headers1,verify=False).text)
        #返回创建状态
        user_create_info_message = wx.MessageDialog(None, caption="info",message=f"{create_info['error']}",style=wx.OK | wx.ICON_INFORMATION)
        if user_create_info_message.ShowModal() == wx.ID_OK:
            pass

    def 按钮2_按钮被单击(self, event):
        self.列表框1.Clear()
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        try:
            for i in range(len(unode)):
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                    self.列表框1.Append(str(i + 1) + ".[国内节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                    self.列表框1.Append(str(i + 1) + ".[国内VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                    self.列表框1.Append(str(i + 1) + ".[国外节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                    self.列表框1.Append(str(i + 1) + ".[国外VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
        except Exception:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"出现错误:{unode}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成",style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass
#修改隧道
class chmlfrp_revise_usertunnel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.列表框1 = wx.ListBox(self, size=(1090, 214), pos=(43, 46), name='listBox', choices=[], style=1073741856)
        self.列表框1.Bind(wx.EVT_LISTBOX_DCLICK, self.列表框1_表项被双击)
        self.标签1 = wx.StaticText(self,size=(248, 24),pos=(38, 16),label='请选择要修改的隧道(双击修改隧道):',name='staticText',style=17)
        self.标签2 = wx.StaticText(self,size=(780, 24),pos=(38, 269),label='请选择修改的节点:',name='staticText',style=17)
        self.列表框2 = wx.ListBox(self, size=(1090, 214), pos=(43, 297), name='listBox', choices=[], style=1073741856)
        self.标签3 = wx.StaticText(self, size=(80, 24), pos=(43, 569), label='隧道内网ip:', name='staticText',style=2321)
        self.usertunnel_ip = wx.TextCtrl(self, size=(211, 22), pos=(125, 569), value='', name='text', style=0)
        self.标签4 = wx.StaticText(self, size=(80, 24), pos=(43, 609), label='隧道内网端口:',name='staticText', style=2321)
        self.usertunnel_n_port = wx.TextCtrl(self, size=(211, 22), pos=(125, 610), value='', name='text',style=0)
        self.标签5 = wx.StaticText(self, size=(80, 24), pos=(43, 653), label='隧道外网端口:',name='staticText', style=2321)
        self.usertunnel_w_port = wx.TextCtrl(self,size=(211, 22),pos=(142, 653),value='',name='text',style=0)
        self.标签6 = wx.StaticText(self, size=(80, 24), pos=(43, 532), label='隧道名称:', name='staticText',style=2321)
        self.usertunnel_name = wx.TextCtrl(self, size=(211, 22), pos=(125, 532), value='', name='text',style=0)
        self.chmlfrp_type = wx.RadioBox(self,size=(250, 60),pos=(382, 616),label='端口类型',choices=['tcp', 'udp', 'http', 'https'],majorDimension=0,name='radioBox',style=4)
        self.chmlfrp_type.Bind(wx.EVT_RADIOBOX,self.chmlfrp_type_选项被单击)
        self.标签7 = wx.StaticText(self, size=(80, 24), pos=(561, 532), label='高级设置:', name='staticText',style=2321)
        self.encryption = wx.CheckBox(self, size=(80, 24), pos=(654, 532), name='check', label='数据加密',style=16384)
        self.compression = wx.CheckBox(self, size=(80, 24), pos=(654, 566), name='check', label='数据压缩',style=16384)
        self.编辑框5 = wx.TextCtrl(self, size=(211, 22), pos=(734, 604), value='', name='text', style=0)
        self.标签8 = wx.StaticText(self, size=(80, 24), pos=(654, 604), label='额外参数:', name='staticText',style=2321)
        self.revise_usertunnel = wx.Button(self, size=(166, 77), pos=(993, 640), label='修改隧道',name='button')
        self.revise_usertunnel.Bind(wx.EVT_BUTTON,self.revise_usertunnel_按钮被单击)
        self.多选框3 = wx.CheckBox(self,size=(196, 24),pos=(843, 268),name='check',label='使用原来的隧道',style=16384)
        self.多选框3.Bind(wx.EVT_CHECKBOX,self.多选框3_狀态被改变)
        self.按钮2 = wx.Button(self,size=(80, 32),pos=(1048, 264),label='刷新隧道',name='button')
        self.按钮2.Bind(wx.EVT_BUTTON,self.按钮2_按钮被单击)
        self.按钮3 = wx.Button(self, size=(80, 32), pos=(1048, 523), label='刷新隧道', name='button')
        self.按钮3.Bind(wx.EVT_BUTTON, self.按钮3_按钮被单击)
        self.Domain_name_query = wx.Button(self, size=(91, 32), pos=(6, 682), label='域名解析查询',name='button')
        self.Domain_name_query.Bind(wx.EVT_BUTTON, self.Domain_name_query_按钮被单击)
        self.random_usertunnel = wx.Button(self, size=(104, 32), pos=(347, 528), label='随机隧道名称',name='button')
        self.random_usertunnel.Bind(wx.EVT_BUTTON, self.random_usertunnel_按钮被单击)
        self.标签9 = wx.StaticText(self, size=(346, 24), pos=(106, 689),label='tips:域名解析查询和修改隧道都需要选择你的隧道才可以进行操作',name='staticText', style=2304)
        self.列表框2.Disable()
        self.Domain_name_query.Hide()
        self.Domain_name_query.Disable()
        self.revise_usertunnel.Disable()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        try:
            #获取当前用户隧道
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.列表框1.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.列表框1.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
        except KeyError:
            pass
        #获取节点列表
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        for i in range(len(unode)):
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                self.列表框2.Append(str(i + 1) + ".[国内节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                self.列表框2.Append(str(i + 1) + ".[国内VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                self.列表框2.Append(str(i + 1) + ".[国外节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                self.列表框2.Append(str(i + 1) + ".[国外VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
        self.多选框3.Disable()

    def chmlfrp_type_选项被单击(self,event):
        if self.chmlfrp_type.GetSelection() == 3:
            self.标签5.SetLabel("你的https域名:")
            self.Domain_name_query.Show()

        elif self.chmlfrp_type.GetSelection() == 2:
            self.标签5.SetLabel("你的http域名:")
            self.Domain_name_query.Show()

        elif self.chmlfrp_type.GetSelection() == 0 or self.chmlfrp_type.GetSelection() == 1:
            self.标签5.SetLabel("隧道外网端口:")
            self.Domain_name_query.Hide()

    def 列表框1_表项被双击(self,event):
        #获取用户选中的隧道信息
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        self.列表框2.Enable()
        self.多选框3.Enable()
        self.Domain_name_query.Enable()
        self.revise_usertunnel.Enable()
        self.标签2.SetLabel(f"请选择修改的节点(当前节点为{usertunnel_info[self.列表框1.GetSelection()]['node']}):")
        self.usertunnel_name.SetLabel(f"{usertunnel_info[self.列表框1.GetSelection()]['name']}")
        self.usertunnel_ip.SetLabel(f"{usertunnel_info[self.列表框1.GetSelection()]['localip']}")
        self.usertunnel_n_port.SetLabel(f"{usertunnel_info[self.列表框1.GetSelection()]['nport']}")
        self.usertunnel_w_port.SetLabel(f"{str(usertunnel_info[self.列表框1.GetSelection()]['dorp'])}")
        if usertunnel_info[self.列表框1.GetSelection()]['type'] == "tcp":
            self.chmlfrp_type.SetSelection(0)
        elif usertunnel_info[self.列表框1.GetSelection()]['type'] == "udp":
            self.chmlfrp_type.SetSelection(1)
        elif usertunnel_info[self.列表框1.GetSelection()]['type'] == "http":
            self.chmlfrp_type.SetSelection(2)
        elif usertunnel_info[self.列表框1.GetSelection()]['type'] == "https":
            self.chmlfrp_type.SetSelection(3)
        if usertunnel_info[self.列表框1.GetSelection()]['encryption'] == "false":
            self.encryption.SetValue(False)
        if usertunnel_info[self.列表框1.GetSelection()]['encryption'] == "true":
            self.encryption.SetValue(True)
        if usertunnel_info[self.列表框1.GetSelection()]['compression'] == "false":
            self.compression.SetValue(False)
        if usertunnel_info[self.列表框1.GetSelection()]['compression'] == "true":
            self.compression.SetValue(True)
        self.编辑框5.SetLabel(f"{str(usertunnel_info[self.列表框1.GetSelection()]['ap'])}")
        if self.chmlfrp_type.GetSelection() == 3:
            self.标签5.SetLabel("你的https域名:")
            self.Domain_name_query.Show()

        elif self.chmlfrp_type.GetSelection() == 2:
            self.标签5.SetLabel("你的http域名:")
            self.Domain_name_query.Show()

        elif self.chmlfrp_type.GetSelection() == 0 or self.chmlfrp_type.GetSelection() == 1:
            self.标签5.SetLabel("隧道外网端口:")
            self.Domain_name_query.Hide()

    def revise_usertunnel_按钮被单击(self, event):
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        if self.encryption.GetValue() == True:
            encryption = "true"
        elif self.encryption.GetValue() == False:
            encryption = "false"
        if self.compression.GetValue() == True:
            compression = "true"
        elif self.compression.GetValue() == False:
            compression = "false"
        if self.chmlfrp_type.GetSelection() == 0:
            chmlfrp_chmlfrp_type = "tcp"
        elif self.chmlfrp_type.GetSelection() == 1:
            chmlfrp_chmlfrp_type = "udp"
        elif self.chmlfrp_type.GetSelection() == 2:
            chmlfrp_chmlfrp_type = "http"
        elif self.chmlfrp_type.GetSelection() == 3:
            chmlfrp_chmlfrp_type = "https"
        if self.多选框3.GetValue() == True:
            node = usertunnel_info[self.列表框1.GetSelection()]['node']
        elif self.多选框3.GetValue() == False:
            node = unode[self.列表框2.GetSelection()]['name']
        #修改隧道请求内容
        data1 = {
                  "tunnelid": f"{str(usertunnel_info[self.列表框1.GetSelection()]['id'])}",
                  "usertoken": F"{sys.argv[1]}",
                  "userid": int(chmlfrp_user_info["userid"]),
                  "localip": f"{self.usertunnel_ip.GetValue()}",
                  "name": f"{self.usertunnel_name.GetValue()}",
                  "node": f"{node}",
                  "type": f"{chmlfrp_chmlfrp_type}",
                  "nport": f"{self.usertunnel_n_port.GetValue()}",
                  "dorp": f"{self.usertunnel_w_port.GetValue()}",
                  "ap": f"{self.编辑框5.GetValue()}",
                  "encryption": f"{encryption}",
                  "compression": f"{compression}"
                }
        #修改隧道请求头
        headers1 = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
            "Accept": "application/json, text/plain, */*",
            "HTTP_TOKEN": f"{sys.argv[1]}"
        }
        #修改隧道请求post
        revise_usertunnel_info = json.loads(requests.post("https://panel.chmlfrp.cn/api/cztunnel.php",headers=headers1,json=data1,verify=False).text)
        #返回状态
        user_revise_info_message = wx.MessageDialog(None, caption="info", message=f"{revise_usertunnel_info['error']}",style=wx.OK | wx.ICON_INFORMATION)
        if user_revise_info_message.ShowModal() == wx.ID_OK:
            pass
        self.列表框1.Clear()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.列表框1.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:" + str(usertunnel_info[i]['localip']) + ",当前隧道内网端口:" + str(usertunnel_info[i]['nport']) + ",当前隧道外网端口:" + str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.列表框1.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:" + str(usertunnel_info[i]['localip']) + ",当前隧道内网端口:" + str(usertunnel_info[i]['nport']) + ",当前隧道外网端口:" + str(usertunnel_info[i]['dorp']))
        except KeyError:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"{usertunnel_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass

    def 多选框3_狀态被改变(self, event):
        if self.多选框3.GetValue() == True:
            self.列表框2.Disable()
        elif self.多选框3.GetValue() == False:
            self.列表框2.Enable()
    def 按钮2_按钮被单击(self,event):
        #刷新隧道
        self.列表框1.Clear()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.列表框1.Append(str(i + 1) + ".[离线节点]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.列表框1.Append(str(i + 1) + ".[正常隧道]隧道名称:" + str(usertunnel_info[i]['name']) + ",隧道节点:" + str(usertunnel_info[i]['node']) + ",隧道ID:" + str(usertunnel_info[i]['id']) + ",当前隧道节点状态:" + str(usertunnel_info[i]['nodestate']) + ",隧道IP:" + str(usertunnel_info[i]['ip']) + ",隧道类型:" + str(usertunnel_info[i]['type']) + ",当前隧道内网ip:"+str(usertunnel_info[i]['localip'])+",当前隧道内网端口:"+str(usertunnel_info[i]['nport'])+",当前隧道外网端口:"+str(usertunnel_info[i]['dorp']))
        except KeyError:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"{usertunnel_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成", style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass

    def 按钮3_按钮被单击(self,event):
        #刷新节点
        self.列表框2.Clear()
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        try:
            for i in range(len(unode)):
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                    self.列表框2.Append(str(i + 1) + ".[国内节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                    self.列表框2.Append(str(i + 1) + ".[国内VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                    self.列表框2.Append(str(i + 1) + ".[国外节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                    self.列表框2.Append(str(i + 1) + ".[国外VIP节点]节点名称:" + str(unode[i]['name']) + ",节点所在地:" + str(unode[i]['area']) + ",节点信息:" + str(unode[i]['notes']) + ",节点状态:" + str(unode[i]['state']) + ",udp支持:" + str(unode[i]['udp']) + ",建站支持:" + str(unode[i]['web']) + ",节点ip:" + str(unode[i]['ip']) + ",外网端口限制:" + str(unode[i]['rport']) + ",节点id:" + str(unode[i]['id']))
        except Exception:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"出现错误:{unode}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成",style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass

    def Domain_name_query_按钮被单击(self,event):
        Domain_name_query_info = json.loads(requests.get(
            f"https://panel.chmlfrp.cn/api/Domain_name_query.php?domain={self.usertunnel_w_port.GetValue()}&target_domain={unode[self.列表框2.GetSelection()]['ip']}",
            headers=headers, verify=False).text)
        if Domain_name_query_info['status'] == "success":
            if Domain_name_query_info['hasSrvToFrpOne'] == False:
                Domain_name_query_srv = "解析失败"
            elif Domain_name_query_info['hasSrvToFrpOne'] == True:
                Domain_name_query_srv = "解析成功"
            if Domain_name_query_info['hasCnameToFrpOne'] == False:
                Domain_name_query_cname = "解析失败"
            elif Domain_name_query_info['hasCnameToFrpOne'] == True:
                Domain_name_query_cname = "解析成功"
            Domain_name_query_ok = wx.MessageDialog(None, caption="info",message=f"解析成功!\n当前节点对此域名进行Srv解析状态:{Domain_name_query_srv}\n当前节点对此域名进行cname解析状态:{Domain_name_query_cname}",style=wx.OK | wx.ICON_INFORMATION)
            if Domain_name_query_ok.ShowModal() == wx.ID_OK:
                pass
        elif Domain_name_query_info['status'] == "error":
            Domain_name_query_Error = wx.MessageDialog(None, caption="info",message=f"解析失败!\n{Domain_name_query_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if Domain_name_query_Error.ShowModal() == wx.ID_OK:
                pass

    def random_usertunnel_按钮被单击(self,event):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 30)))
        self.usertunnel_name.SetLabel(random_str)


#关于
class chmlfrp_about(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.标签1 = wx.StaticText(self, size=(678, 120), pos=(236, 65),label='关于\n怊猫Chcat（项目运营）\n超级ChaoJi（Web端的开发）\ndaijunhao（视窗(windows)软件开发）\n感谢你使用chmlfrp',name='staticText', style=2304)
        标签1_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.标签1.SetFont(标签1_字体)

class chmlfrp_docs_web(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.browser = wx.html2.WebView.New(self)
        self.browser.LoadURL("https://docs.chcat.cn/docs")
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.browser, 1, wx.EXPAND, 10)
        self.SetSizer(sizer)
        self.SetSize((1200, 800))
        self.Center()




#选项卡创建
class MyNotebook(wx.Notebook):
    def __init__(self, parent):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT | wx.NB_FIXEDWIDTH | wx.NB_NOPAGETHEME)
        self.AddPage(chmlfrp_user(self), "用户主界面")
        self.AddPage(chmlfrp_start_usertunnel(self), "启动隧道")
        self.AddPage(chmlfrp_delete_usertunnel(self), "删除隧道")
        self.AddPage(chmlfrp_create_usertunnel(self), "创建隧道")
        self.AddPage(chmlfrp_revise_usertunnel(self), "修改隧道")
        #chmlfrp帮助文档在IE浏览器下加载不出来,帮助文档默认为IE浏览器,所以取消
        #self.AddPage(chmlfrp_docs_web(self), "帮助文档")
        self.AddPage(chmlfrp_about(self), "关于")


class SampleNotebook(wx.Frame):

    def __init__(self, *args, **kw):
        super(SampleNotebook, self).__init__(*args, **kw)
        self.InitUi()
    def InitUi(self):
        self.SetWindowStyle(style=541072384)
        # 设置标题
        self.hitokoto()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.hitokoto, self.timer)
        self.timer.Start(10000)  # 10 seconds
        # 设置窗口尺寸
        self.SetSize(1200, 800)
        panel = wx.Panel(self)
        notebook = MyNotebook(panel)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(notebook, 1, wx.ALL | wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()
        self.Centre()
        icon = wx.Icon(fr'{pathx}\chmlfrp.ico')
        self.SetIcon(icon)
    # 一言
    def hitokoto(self, event=None):
        try:
            response = json.loads(requests.get('https://v1.hitokoto.cn/', headers=headers, verify=False).text)
            hitokoto = response['hitokoto']
            hitokoto_from = response['from']
            self.SetTitle(f"chmlfrp客户端   {hitokoto}----{hitokoto_from}")
        except Exception:
            self.SetTitle("chmlfrp客户端")


def main():
    app = wx.App()
    sample = SampleNotebook(None)
    sample.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
