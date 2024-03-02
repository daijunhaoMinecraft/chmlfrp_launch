# -*- coding:utf-8 -*-
import base64
import json
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
import getpass
from io import BytesIO
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))
#获取当前path路径
pathx = os.path.dirname(os.path.realpath(sys.argv[0]))
#忽略证书警告
requests.packages.urllib3.disable_warnings()
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
        if os.path.exists(f"{pathx_pyinstaller}\\frpc.exe"):
            pass
        else:
            frpc_file_Error = wx.MessageDialog(None, caption="Error",message=f"未检测到frpc文件,请检查你是否有被删除,如果有,请下载frpc文件到此文件夹目录下",style=wx.OK | wx.ICON_ERROR)
            if frpc_file_Error.ShowModal() == wx.ID_OK:
                sys.exit()
        if os.path.exists(f"{pathx_pyinstaller}\\start_frpc.exe"):
            pass
        else:
            start_frpc_file_Error = wx.MessageDialog(None, caption="Error",message=f"未检测到start_frpc文件,请检查你是否有被删除,如果有,请重新下载文件",style=wx.OK | wx.ICON_ERROR)
            if start_frpc_file_Error.ShowModal() == wx.ID_OK:
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
        self.chmlfrp_user_img.SetBitmap(wx.Image(BytesIO(requests.get(f"{chmlfrp_user_info['userimg']}",headers=headers,verify=False).content)).ConvertToBitmap())
        #获取签到状态
        qd = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/qdxx.php?userid={chmlfrp_user_info['userid']}",verify=False,headers=headers).text)
        if qd['is_signed_in_today'] == True:
            qd_info = f"今天已经签到了\n累计签到次数:{qd['total_sign_ins']}次\n累计签到获得的积分:{qd['total_points']}分\n今天一共签到的人数:{qd['count_of_matching_records']}人\n你的上一次签到时间为:{qd['last_sign_in_time']}"
        if qd['is_signed_in_today'] == False:
            qd_info = f"今天还未签到\n累计签到次数:{qd['total_sign_ins']}次\n累计签到获得的积分:{qd['total_points']}分\n今天一共签到的人数:{qd['count_of_matching_records']}人\n你的上一次签到时间为:{qd['last_sign_in_time']}"
        self.chmlfrp_info = wx.TextCtrl(self,size=(366, 249),pos=(7, 151),value=f'当前用户id:{str(chmlfrp_user_info["userid"])}\n当前用户组:{str(chmlfrp_user_info["usergroup"])}\n到期时间:{chmlfrp_user_info["term"]}\n当前用户隧道数量:{chmlfrp_user_info["tunnelstate"]} / {chmlfrp_user_info["tunnel"]}\n当前用户宽带限制:国内:{chmlfrp_user_info["bandwidth"]}Mbps | 国外:{str(int(chmlfrp_user_info["bandwidth"]) * 4)}M\n当前用户实名状态:{chmlfrp_user_info["realname"]}\n当前用户积分数:{str(chmlfrp_user_info["integral"])}\n{qd_info}',name='text',style=1073741872)
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
class chmlfrp_start_delete_usertunnel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.标签1 = wx.StaticText(self,size=(170, 24),pos=(15, 13),label='当前隧道列表(单击隧道选择):',name='staticText',style=2321)
        self.start_usertunnel = wx.Button(self,size=(224, 85),pos=(591, 381),label='启动隧道',name='button')
        start_usertunnel_字体 = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.start_usertunnel.SetFont(start_usertunnel_字体)
        self.start_usertunnel.SetForegroundColour((0, 128, 255, 255))
        self.start_usertunnel.Bind(wx.EVT_BUTTON,self.start_usertunnel_按钮被单击)
        self.usertunnel_list = wx.ListCtrl(self,size=(1113, 312),pos=(15, 41),name='listCtrl',style=8227)
        self.usertunnel_list.AppendColumn('隧道序号', 0,183)
        self.usertunnel_list.AppendColumn('隧道名称', 0,117)
        self.usertunnel_list.AppendColumn('隧道id', 0,85)
        self.usertunnel_list.AppendColumn('启动地址', 0,155)
        self.usertunnel_list.AppendColumn('上一次隧道启动时间', 0,182)
        self.usertunnel_list.AppendColumn('隧道节点', 0,130)
        self.usertunnel_list.AppendColumn('隧道内网ip', 0,121)
        self.usertunnel_list.AppendColumn('隧道内网端口', 0,146)
        self.usertunnel_list.AppendColumn('隧道类型', 0,119)
        self.usertunnel_list.AppendColumn('隧道外网端口/域名', 0,127)
        self.usertunnel_list.AppendColumn('隧道状态', 0,94)
        self.usertunnel_list.AppendColumn('节点状态', 0,101)
        self.usertunnel_list.AppendColumn('数据加密是否开启', 0,113)
        self.usertunnel_list.AppendColumn('数据压缩是否开启', 0,117)
        self.usertunnel_list.AppendColumn('隧道ap内容', 0,138)
        self.usertunnel_list.AppendColumn('使用客户端', 0,145)
        self.usertunnel_list.Bind(wx.EVT_LIST_ITEM_SELECTED,self.usertunnel_list_选中表项)
        self.编辑框2 = wx.TextCtrl(self,size=(366, 323),pos=(206, 381),value='',name='text',style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_AUTO_URL)
        self.标签3 = wx.StaticText(self,size=(165, 112),pos=(15, 381),label='当前隧道frpc配置:\nfrpc配置请不要随意发给任何人',name='staticText',style=17)
        self.delete_usertunnel = wx.Button(self,size=(224, 85),pos=(591, 507),label='删除隧道',name='button')
        delete_usertunnel_字体 = wx.Font(9,70,90,700,False,'Microsoft YaHei UI',28)
        self.delete_usertunnel.SetFont(delete_usertunnel_字体)
        self.delete_usertunnel.SetForegroundColour((255, 0, 0, 255))
        self.delete_usertunnel.Bind(wx.EVT_BUTTON,self.delete_usertunnel_按钮被单击)
        self.flushed_usertunnel = wx.Button(self,size=(107, 36),pos=(1021, 368),label='刷新隧道',name='button')
        flushed_usertunnel_字体 = wx.Font(9,70,90,700,False,'Microsoft YaHei UI',28)
        self.flushed_usertunnel.SetFont(flushed_usertunnel_字体)
        self.flushed_usertunnel.Bind(wx.EVT_BUTTON,self.flushed_usertunnel_按钮被单击)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        self.start_usertunnel.Disable()
        self.delete_usertunnel.Disable()
        self.按钮4 = wx.Button(self, size=(224, 85), pos=(591, 630), label='添加自启动项目', name='button')
        按钮4_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.按钮4.SetFont(按钮4_字体)
        self.按钮4.SetForegroundColour((255, 128, 64, 255))
        self.按钮4.Bind(wx.EVT_BUTTON, self.按钮4_按钮被单击)
        self.按钮4.Disable()
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
        except KeyError:
            pass

    def 按钮4_按钮被单击(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        with open(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\chmlfrp-{usertunnel_info[self.usertunnel_list.GetFirstSelected()]["name"]}.bat',mode="w",encoding="ANSI") as f:
            f.write(f"start {pathx_pyinstaller}\\start_frpc.exe {sys.argv[1]} {str(self.usertunnel_list.GetFirstSelected())}")
        start_up_write_info = wx.MessageDialog(None, caption="info", message=f"自启动添加完成,若需要删除自启动请到启动项管理中删除",style=wx.OK | wx.ICON_INFORMATION)
        if start_up_write_info.ShowModal() == wx.ID_YES:
            pass

    def usertunnel_list_选中表项(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            frpc_config = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/frpconfig.php?usertoken={sys.argv[1]}&node={usertunnel_info[self.usertunnel_list.GetFirstSelected()]['node']}",verify=False,headers=headers).text)['message']
            self.编辑框2.SetLabel(frpc_config)
            self.delete_usertunnel.Enable()
            self.start_usertunnel.Enable()
            self.按钮4.Enable()
        except Exception:
            self.按钮4.Disable()
            self.start_usertunnel.Disable()
            self.delete_usertunnel.Disable()


    def start_usertunnel_按钮被单击(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        os.system(f"start {pathx_pyinstaller}\\start_frpc.exe {sys.argv[1]} {str(self.usertunnel_list.GetFirstSelected())}")
        user_usertunnel_OK = wx.MessageDialog(None, caption="info",message=f"已执行隧道启动命令,是否复制ip?",style=wx.YES_NO | wx.ICON_INFORMATION)
        if user_usertunnel_OK.ShowModal() == wx.ID_YES:
            pycopy.copy(usertunnel_info[self.usertunnel_list.GetFirstSelected()]['ip'])
            copy_ok = wx.MessageDialog(None, caption="info", message=f"ip复制完成",style=wx.OK | wx.ICON_INFORMATION)
            if copy_ok.ShowModal() == wx.ID_OK:
                pass


    def delete_usertunnel_按钮被单击(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        delete_warm = wx.MessageDialog(None, caption="警告", message="你确定要删除此隧道吗?",style=wx.YES_NO | wx.ICON_WARNING)
        if delete_warm.ShowModal() == wx.ID_YES:
            delete_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/deletetl.php?token={sys.argv[1]}&nodeid={usertunnel_info[self.usertunnel_list.GetFirstSelected()]['id']}&userid={str(chmlfrp_user_info['userid'])}",headers=headers,verify=False).text)
            self.usertunnel_list.ClearAll()
            self.start_usertunnel.Disable()
            self.delete_usertunnel.Disable()
            self.按钮4.Disable()
            self.编辑框2.SetLabel("")
            self.usertunnel_list.AppendColumn('隧道序号', 0, 183)
            self.usertunnel_list.AppendColumn('隧道名称', 0, 117)
            self.usertunnel_list.AppendColumn('隧道id', 0, 85)
            self.usertunnel_list.AppendColumn('启动地址', 0, 155)
            self.usertunnel_list.AppendColumn('上一次隧道启动时间', 0, 182)
            self.usertunnel_list.AppendColumn('隧道节点', 0, 130)
            self.usertunnel_list.AppendColumn('隧道内网ip', 0, 121)
            self.usertunnel_list.AppendColumn('隧道内网端口', 0, 146)
            self.usertunnel_list.AppendColumn('隧道类型', 0, 119)
            self.usertunnel_list.AppendColumn('隧道外网端口/域名', 0, 127)
            self.usertunnel_list.AppendColumn('隧道状态', 0, 94)
            self.usertunnel_list.AppendColumn('节点状态', 0, 101)
            self.usertunnel_list.AppendColumn('数据加密是否开启', 0, 113)
            self.usertunnel_list.AppendColumn('数据压缩是否开启', 0, 117)
            self.usertunnel_list.AppendColumn('隧道ap内容', 0, 138)
            self.usertunnel_list.AppendColumn('使用客户端', 0, 145)
            usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
            try:
                for i in range(len(usertunnel_info)):
                    if str(usertunnel_info[i]['nodestate']) == "offline":
                        self.usertunnel_list.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                    if str(usertunnel_info[i]['nodestate']) == "online":
                        self.usertunnel_list.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
            except KeyError:
                pass
            delete_info_message = wx.MessageDialog(None, caption="删除状态", message=f"{delete_info['error']}",style=wx.OK | wx.ICON_INFORMATION)
            if delete_info_message.ShowModal() == wx.ID_YES:
                pass


    def flushed_usertunnel_按钮被单击(self,event):
        self.usertunnel_list.ClearAll()
        self.start_usertunnel.Disable()
        self.delete_usertunnel.Disable()
        self.按钮4.Disable()
        self.编辑框2.SetLabel("")
        self.usertunnel_list.AppendColumn('隧道序号', 0, 183)
        self.usertunnel_list.AppendColumn('隧道名称', 0, 117)
        self.usertunnel_list.AppendColumn('隧道id', 0, 85)
        self.usertunnel_list.AppendColumn('启动地址', 0, 155)
        self.usertunnel_list.AppendColumn('上一次隧道启动时间', 0, 182)
        self.usertunnel_list.AppendColumn('隧道节点', 0, 130)
        self.usertunnel_list.AppendColumn('隧道内网ip', 0, 121)
        self.usertunnel_list.AppendColumn('隧道内网端口', 0, 146)
        self.usertunnel_list.AppendColumn('隧道类型', 0, 119)
        self.usertunnel_list.AppendColumn('隧道外网端口/域名', 0, 127)
        self.usertunnel_list.AppendColumn('隧道状态', 0, 94)
        self.usertunnel_list.AppendColumn('节点状态', 0, 101)
        self.usertunnel_list.AppendColumn('数据加密是否开启', 0, 113)
        self.usertunnel_list.AppendColumn('数据压缩是否开启', 0, 117)
        self.usertunnel_list.AppendColumn('隧道ap内容', 0, 138)
        self.usertunnel_list.AppendColumn('使用客户端', 0, 145)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
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
        self.标签1 = wx.StaticText(self, size=(222, 24), pos=(27, 20),label='当前节点列表(单击选择创建的隧道节点):', name='staticText', style=17)
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
        self.超级列表框1 = wx.ListCtrl(self, size=(1103, 261), pos=(27, 51), name='listCtrl', style=8227)
        self.超级列表框1.AppendColumn('节点序号', 0, 111)
        self.超级列表框1.AppendColumn('节点名称', 0, 128)
        self.超级列表框1.AppendColumn('节点所在地', 0, 127)
        self.超级列表框1.AppendColumn('节点信息', 0, 159)
        self.超级列表框1.AppendColumn('节点id', 0, 92)
        self.超级列表框1.AppendColumn('节点ip', 0, 149)
        self.超级列表框1.AppendColumn('节点token', 0, 146)
        self.超级列表框1.AppendColumn('节点apitoken', 0, 165)
        self.超级列表框1.AppendColumn('节点端口', 0, 118)
        self.超级列表框1.AppendColumn('节点端口限制', 0, 166)
        self.超级列表框1.AppendColumn('节点状态', 0, 107)
        self.超级列表框1.AppendColumn('创建节点索要的最低权限', 0, 164)
        self.超级列表框1.AppendColumn('建站支持', 0, 99)
        self.超级列表框1.AppendColumn('节点是否在中国', 0, 113)
        self.超级列表框1.AppendColumn('http端口', 0, 95)
        self.超级列表框1.AppendColumn('https端口', 0, 84)
        self.超级列表框1.AppendColumn('节点有防/无防', 0, 97)
        self.超级列表框1.AppendColumn('udp支持', 0, 68)
        self.超级列表框1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.超级列表框1_选中表项)
        #获取节点
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        for i in range(len(unode)):
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                self.超级列表框1.Append([f'{str(i + 1)}.[国内节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                self.超级列表框1.Append([f'{str(i + 1)}.[国内VIP节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                self.超级列表框1.Append([f'{str(i + 1)}.[海外节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                self.超级列表框1.Append([f'{str(i + 1)}.[海外vip节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
        self.usertunnel_ip.SetLabel("127.0.0.1")
    def 超级列表框1_选中表项(self,event):
        self.create_usertunnel.Enable()
        self.Domain_name_query.Enable()
        self.random_w_port.Enable()

    def random_w_port_按钮被单击(self,event):
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        unode_w_port = f"{unode[self.超级列表框1.GetFirstSelected()]['rport']}".split("-")
        self.usertunnel_w_port.SetLabel(str(random.randint(int(unode_w_port[0]), int(unode_w_port[1]))))

    def random_name_usertunnel_按钮被单击(self,event):
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 15)))
        self.usertunnel_name.SetLabel(random_str)

    def Domain_name_query_按钮被单击(self,event):
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        Domain_name_query_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/Domain_name_query.php?domain={self.usertunnel_w_port.GetValue()}&target_domain={unode[self.超级列表框1.GetFirstSelected()]['ip']}",headers=headers,verify=False).text)
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
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
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
                      "node": f"{unode[self.超级列表框1.GetFirstSelected()]['name']}",
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
        self.超级列表框1.ClearAll()
        self.create_usertunnel.Disable()
        self.Domain_name_query.Disable()
        self.random_w_port.Disable()
        self.超级列表框1.AppendColumn('节点序号', 0, 111)
        self.超级列表框1.AppendColumn('节点名称', 0, 128)
        self.超级列表框1.AppendColumn('节点所在地', 0, 127)
        self.超级列表框1.AppendColumn('节点信息', 0, 159)
        self.超级列表框1.AppendColumn('节点id', 0, 92)
        self.超级列表框1.AppendColumn('节点ip', 0, 149)
        self.超级列表框1.AppendColumn('节点token', 0, 146)
        self.超级列表框1.AppendColumn('节点apitoken', 0, 165)
        self.超级列表框1.AppendColumn('节点端口', 0, 118)
        self.超级列表框1.AppendColumn('节点端口限制', 0, 166)
        self.超级列表框1.AppendColumn('节点状态', 0, 107)
        self.超级列表框1.AppendColumn('创建节点索要的最低权限', 0, 164)
        self.超级列表框1.AppendColumn('建站支持', 0, 99)
        self.超级列表框1.AppendColumn('节点是否在中国', 0, 113)
        self.超级列表框1.AppendColumn('http端口', 0, 95)
        self.超级列表框1.AppendColumn('https端口', 0, 84)
        self.超级列表框1.AppendColumn('节点有防/无防', 0, 97)
        self.超级列表框1.AppendColumn('udp支持', 0, 68)
        try:
            unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
            for i in range(len(unode)):
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                    self.超级列表框1.Append([f'{str(i + 1)}.[国内节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                    self.超级列表框1.Append([f'{str(i + 1)}.[国内VIP节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                    self.超级列表框1.Append([f'{str(i + 1)}.[海外节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                    self.超级列表框1.Append([f'{str(i + 1)}.[海外vip节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
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
        self.标签1 = wx.StaticText(self,size=(248, 24),pos=(38, 16),label='请选择要修改的隧道(单击修改隧道):',name='staticText',style=17)
        self.标签2 = wx.StaticText(self,size=(780, 24),pos=(38, 269),label='请选择修改的节点:',name='staticText',style=17)
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
        self.超级列表框1 = wx.ListCtrl(self, size=(1090, 214), pos=(38, 46), name='listCtrl', style=8227)
        self.超级列表框1.AppendColumn('隧道序号', 0, 115)
        self.超级列表框1.AppendColumn('隧道名称', 0, 142)
        self.超级列表框1.AppendColumn('隧道id', 0, 65)
        self.超级列表框1.AppendColumn('启动地址', 0, 129)
        self.超级列表框1.AppendColumn('上一次隧道启动时间', 0, 169)
        self.超级列表框1.AppendColumn('隧道节点', 0, 102)
        self.超级列表框1.AppendColumn('隧道内网ip', 0, 106)
        self.超级列表框1.AppendColumn('隧道内网端口', 0, 126)
        self.超级列表框1.AppendColumn('隧道类型', 0, 113)
        self.超级列表框1.AppendColumn('隧道外网端口/域名', 0, 206)
        self.超级列表框1.AppendColumn('隧道状态', 0, 108)
        self.超级列表框1.AppendColumn('节点状态', 0, 112)
        self.超级列表框1.AppendColumn('数据加密是否开启', 0, 140)
        self.超级列表框1.AppendColumn('数据压缩是否开启', 0, 125)
        self.超级列表框1.AppendColumn('隧道ap内容', 0, 118)
        self.超级列表框1.AppendColumn('使用客户端', 0, 118)
        self.超级列表框1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.超级列表框1_选中表项)
        self.超级列表框2 = wx.ListCtrl(self, size=(1090, 214), pos=(38, 300), name='listCtrl', style=8227)
        self.超级列表框2.AppendColumn('节点序号', 0, 128)
        self.超级列表框2.AppendColumn('节点名称', 0, 148)
        self.超级列表框2.AppendColumn('节点所在地', 0, 191)
        self.超级列表框2.AppendColumn('节点信息', 0, 130)
        self.超级列表框2.AppendColumn('节点id', 0, 94)
        self.超级列表框2.AppendColumn('节点ip', 0, 132)
        self.超级列表框2.AppendColumn('节点token', 0, 126)
        self.超级列表框2.AppendColumn('节点apitoken', 0, 156)
        self.超级列表框2.AppendColumn('节点端口', 0, 106)
        self.超级列表框2.AppendColumn('节点端口限制', 0, 141)
        self.超级列表框2.AppendColumn('节点状态', 0, 127)
        self.超级列表框2.AppendColumn('创建节点索要的最低权限', 0, 185)
        self.超级列表框2.AppendColumn('建站支持', 0, 102)
        self.超级列表框2.AppendColumn('节点是否在中国', 0, 116)
        self.超级列表框2.AppendColumn('http端口', 0, 92)
        self.超级列表框2.AppendColumn('https端口', 0, 89)
        self.超级列表框2.AppendColumn('节点有防/无防', 0, 105)
        self.超级列表框2.AppendColumn('udp支持', 0, 71)
        self.超级列表框2.Disable()
        self.Domain_name_query.Hide()
        self.Domain_name_query.Disable()
        self.revise_usertunnel.Disable()
        self.多选框3.Disable()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.超级列表框1.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.超级列表框1.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
        except KeyError:
            pass
        #获取节点列表
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        for i in range(len(unode)):
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                self.超级列表框2.Append([f'{str(i + 1)}.[国内节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
            if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                self.超级列表框2.Append([f'{str(i + 1)}.[国内VIP节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                self.超级列表框2.Append([f'{str(i + 1)}.[海外节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
            if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                self.超级列表框2.Append([f'{str(i + 1)}.[海外vip节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])

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

    def 超级列表框1_选中表项(self, event):
        #获取用户选中的隧道信息
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}", headers=headers,verify=False).text)
        self.超级列表框2.Enable()
        self.多选框3.Enable()
        self.Domain_name_query.Enable()
        self.revise_usertunnel.Enable()
        self.标签2.SetLabel(f"请选择修改的节点(当前节点为{usertunnel_info[self.超级列表框1.GetFirstSelected()]['node']}):")
        self.usertunnel_name.SetLabel(f"{usertunnel_info[self.超级列表框1.GetFirstSelected()]['name']}")
        self.usertunnel_ip.SetLabel(f"{usertunnel_info[self.超级列表框1.GetFirstSelected()]['localip']}")
        self.usertunnel_n_port.SetLabel(f"{usertunnel_info[self.超级列表框1.GetFirstSelected()]['nport']}")
        self.usertunnel_w_port.SetLabel(f"{str(usertunnel_info[self.超级列表框1.GetFirstSelected()]['dorp'])}")
        if usertunnel_info[self.超级列表框1.GetFirstSelected()]['type'] == "tcp":
            self.chmlfrp_type.SetSelection(0)
        elif usertunnel_info[self.超级列表框1.GetFirstSelected()]['type'] == "udp":
            self.chmlfrp_type.SetSelection(1)
        elif usertunnel_info[self.超级列表框1.GetFirstSelected()]['type'] == "http":
            self.chmlfrp_type.SetSelection(2)
        elif usertunnel_info[self.超级列表框1.GetFirstSelected()]['type'] == "https":
            self.chmlfrp_type.SetSelection(3)
        if usertunnel_info[self.超级列表框1.GetFirstSelected()]['encryption'] == "false":
            self.encryption.SetValue(False)
        if usertunnel_info[self.超级列表框1.GetFirstSelected()]['encryption'] == "true":
            self.encryption.SetValue(True)
        if usertunnel_info[self.超级列表框1.GetFirstSelected()]['compression'] == "false":
            self.compression.SetValue(False)
        if usertunnel_info[self.超级列表框1.GetFirstSelected()]['compression'] == "true":
            self.compression.SetValue(True)
        self.编辑框5.SetLabel(f"{str(usertunnel_info[self.超级列表框1.GetFirstSelected()]['ap'])}")
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
            node = usertunnel_info[self.超级列表框1.GetFirstSelected()]['node']
        elif self.多选框3.GetValue() == False:
            node = unode[self.超级列表框2.GetFirstSelected()]['name']
        if self.超级列表框2.GetFirstSelected() == -1:
            node = usertunnel_info[self.超级列表框1.GetFirstSelected()]['node']
        #修改隧道请求内容
        data1 = {
                  "tunnelid": f"{str(usertunnel_info[self.超级列表框1.GetFirstSelected()]['id'])}",
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
        self.超级列表框1.ClearAll()
        self.多选框3.Disable()
        self.超级列表框2.Disable()
        self.revise_usertunnel.Disable()
        self.超级列表框1.AppendColumn('隧道序号', 0, 115)
        self.超级列表框1.AppendColumn('隧道名称', 0, 142)
        self.超级列表框1.AppendColumn('隧道id', 0, 65)
        self.超级列表框1.AppendColumn('启动地址', 0, 129)
        self.超级列表框1.AppendColumn('上一次隧道启动时间', 0, 169)
        self.超级列表框1.AppendColumn('隧道节点', 0, 102)
        self.超级列表框1.AppendColumn('隧道内网ip', 0, 106)
        self.超级列表框1.AppendColumn('隧道内网端口', 0, 126)
        self.超级列表框1.AppendColumn('隧道类型', 0, 113)
        self.超级列表框1.AppendColumn('隧道外网端口/域名', 0, 206)
        self.超级列表框1.AppendColumn('隧道状态', 0, 108)
        self.超级列表框1.AppendColumn('节点状态', 0, 112)
        self.超级列表框1.AppendColumn('数据加密是否开启', 0, 140)
        self.超级列表框1.AppendColumn('数据压缩是否开启', 0, 125)
        self.超级列表框1.AppendColumn('隧道ap内容', 0, 118)
        self.超级列表框1.AppendColumn('使用客户端', 0, 118)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.超级列表框1.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.超级列表框1.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
        except KeyError:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"{usertunnel_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        self.超级列表框2.ClearAll()
        self.标签2.SetLabel("请选择修改的节点")
        self.超级列表框2.AppendColumn('节点序号', 0, 128)
        self.超级列表框2.AppendColumn('节点名称', 0, 148)
        self.超级列表框2.AppendColumn('节点所在地', 0, 191)
        self.超级列表框2.AppendColumn('节点信息', 0, 130)
        self.超级列表框2.AppendColumn('节点id', 0, 94)
        self.超级列表框2.AppendColumn('节点ip', 0, 132)
        self.超级列表框2.AppendColumn('节点token', 0, 126)
        self.超级列表框2.AppendColumn('节点apitoken', 0, 156)
        self.超级列表框2.AppendColumn('节点端口', 0, 106)
        self.超级列表框2.AppendColumn('节点端口限制', 0, 141)
        self.超级列表框2.AppendColumn('节点状态', 0, 127)
        self.超级列表框2.AppendColumn('创建节点索要的最低权限', 0, 185)
        self.超级列表框2.AppendColumn('建站支持', 0, 102)
        self.超级列表框2.AppendColumn('节点是否在中国', 0, 116)
        self.超级列表框2.AppendColumn('http端口', 0, 92)
        self.超级列表框2.AppendColumn('https端口', 0, 89)
        self.超级列表框2.AppendColumn('节点有防/无防', 0, 105)
        self.超级列表框2.AppendColumn('udp支持', 0, 71)
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        try:
            for i in range(len(unode)):
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                    self.超级列表框2.Append([f'{str(i + 1)}.[国内节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                    self.超级列表框2.Append([f'{str(i + 1)}.[国内VIP节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                    self.超级列表框2.Append([f'{str(i + 1)}.[海外节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                    self.超级列表框2.Append([f'{str(i + 1)}.[海外vip节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
        except Exception:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"出现错误:{unode}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass

    def 多选框3_狀态被改变(self, event):
        if self.多选框3.GetValue() == True:
            self.超级列表框2.Disable()
        elif self.多选框3.GetValue() == False:
            self.超级列表框2.Enable()
    def 按钮2_按钮被单击(self,event):
        #刷新隧道
        self.超级列表框1.ClearAll()
        self.超级列表框2.Disable()
        self.多选框3.Disable()
        self.revise_usertunnel.Disable()
        self.超级列表框1.AppendColumn('隧道序号', 0, 115)
        self.超级列表框1.AppendColumn('隧道名称', 0, 142)
        self.超级列表框1.AppendColumn('隧道id', 0, 65)
        self.超级列表框1.AppendColumn('启动地址', 0, 129)
        self.超级列表框1.AppendColumn('上一次隧道启动时间', 0, 169)
        self.超级列表框1.AppendColumn('隧道节点', 0, 102)
        self.超级列表框1.AppendColumn('隧道内网ip', 0, 106)
        self.超级列表框1.AppendColumn('隧道内网端口', 0, 126)
        self.超级列表框1.AppendColumn('隧道类型', 0, 113)
        self.超级列表框1.AppendColumn('隧道外网端口/域名', 0, 206)
        self.超级列表框1.AppendColumn('隧道状态', 0, 108)
        self.超级列表框1.AppendColumn('节点状态', 0, 112)
        self.超级列表框1.AppendColumn('数据加密是否开启', 0, 140)
        self.超级列表框1.AppendColumn('数据压缩是否开启', 0, 125)
        self.超级列表框1.AppendColumn('隧道ap内容', 0, 118)
        self.超级列表框1.AppendColumn('使用客户端', 0, 118)
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={sys.argv[1]}",headers=headers,verify=False).text)
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.超级列表框1.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.超级列表框1.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
        except KeyError:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"{usertunnel_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成", style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass

    def 按钮3_按钮被单击(self,event):
        #刷新节点
        self.超级列表框2.ClearAll()
        self.超级列表框2.AppendColumn('节点序号', 0, 128)
        self.超级列表框2.AppendColumn('节点名称', 0, 148)
        self.超级列表框2.AppendColumn('节点所在地', 0, 191)
        self.超级列表框2.AppendColumn('节点信息', 0, 130)
        self.超级列表框2.AppendColumn('节点id', 0, 94)
        self.超级列表框2.AppendColumn('节点ip', 0, 132)
        self.超级列表框2.AppendColumn('节点token', 0, 126)
        self.超级列表框2.AppendColumn('节点apitoken', 0, 156)
        self.超级列表框2.AppendColumn('节点端口', 0, 106)
        self.超级列表框2.AppendColumn('节点端口限制', 0, 141)
        self.超级列表框2.AppendColumn('节点状态', 0, 127)
        self.超级列表框2.AppendColumn('创建节点索要的最低权限', 0, 185)
        self.超级列表框2.AppendColumn('建站支持', 0, 102)
        self.超级列表框2.AppendColumn('节点是否在中国', 0, 116)
        self.超级列表框2.AppendColumn('http端口', 0, 92)
        self.超级列表框2.AppendColumn('https端口', 0, 89)
        self.超级列表框2.AppendColumn('节点有防/无防', 0, 105)
        self.超级列表框2.AppendColumn('udp支持', 0, 71)
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        try:
            for i in range(len(unode)):
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "user":
                    self.超级列表框2.Append([f'{str(i + 1)}.[国内节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "yes" and unode[i]['nodegroup'] == "vip":
                    self.超级列表框2.Append([f'{str(i + 1)}.[国内VIP节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "user":
                    self.超级列表框2.Append([f'{str(i + 1)}.[海外节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
                if unode[i]['china'] == "no" and unode[i]['nodegroup'] == "vip":
                    self.超级列表框2.Append([f'{str(i + 1)}.[海外vip节点]', f'{str(unode[i]["name"])}', f'{str(unode[i]["area"])}', f'{str(unode[i]["notes"])}', f'{str(unode[i]["id"])}', f'{str(unode[i]["ip"])}', f'{str(unode[i]["nodetoken"])}', f'{str(unode[i]["apitoken"])}', f'{str(unode[i]["port"])}', f'{str(unode[i]["rport"])}', f'{str(unode[i]["state"])}', f'{str(unode[i]["nodegroup"])}', f'{str(unode[i]["web"])}', f'{str(unode[i]["china"])}', f'{str(unode[i]["http_port"])}', f'{str(unode[i]["https_port"])}', f'{str(unode[i]["fangyu"])}', f'{str(unode[i]["udp"])}'])
        except Exception as e:
            flushed_usertunnel_error = wx.MessageDialog(None, caption="info", message=f"出现错误:{e}",style=wx.OK | wx.ICON_ERROR)
            if flushed_usertunnel_error.ShowModal() == wx.ID_OK:
                pass
        flushed_usertunnel_ok = wx.MessageDialog(None, caption="info", message=f"刷新完成",style=wx.OK | wx.ICON_INFORMATION)
        if flushed_usertunnel_ok.ShowModal() == wx.ID_OK:
            pass

    def Domain_name_query_按钮被单击(self,event):
        unode = json.loads(requests.get("https://panel.chmlfrp.cn/api/unode.php", verify=False, headers=headers).text)
        Domain_name_query_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/Domain_name_query.php?domain={self.usertunnel_w_port.GetValue()}&target_domain={unode[self.列表框2.GetSelection()]['ip']}",headers=headers, verify=False).text)
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
        random_str = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 15)))
        self.usertunnel_name.SetLabel(random_str)

class start_up(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        global chmlfrp_f
        self.标签1 = wx.StaticText(self,size=(399, 24),pos=(35, 25),label='当前启动文件中有以下启动项(只包含隧道启动项):',name='staticText',style=17)
        self.超级列表框1 = wx.ListCtrl(self,size=(1072, 327),pos=(35, 54),name='listCtrl',style=8227)
        self.超级列表框1.AppendColumn('启动项名称', 0,231)
        self.超级列表框1.AppendColumn('此启动项路径', 0,871)
        self.超级列表框1.Bind(wx.EVT_LIST_ITEM_SELECTED, self.超级列表框1_选中表项)
        self.按钮1 = wx.Button(self,size=(170, 65),pos=(35, 407),label='删除启动项',name='button')
        按钮1_字体 = wx.Font(9,70,90,700,False,'Microsoft YaHei UI',28)
        self.按钮1.SetFont(按钮1_字体)
        self.按钮1.SetForegroundColour((255, 0, 0, 255))
        self.按钮1.Bind(wx.EVT_BUTTON,self.按钮1_按钮被单击)
        self.按钮2 = wx.Button(self,size=(170, 65),pos=(35, 498),label='打开启动项文件',name='button')
        按钮2_字体 = wx.Font(9,70,90,700,False,'Microsoft YaHei UI',28)
        self.按钮2.SetFont(按钮2_字体)
        self.按钮2.SetForegroundColour((0, 128, 255, 255))
        self.按钮2.Bind(wx.EVT_BUTTON,self.按钮2_按钮被单击)
        self.按钮1.Disable()
        self.按钮4 = wx.Button(self, size=(80, 32), pos=(1027, 398), label='刷新启动项', name='button')
        self.按钮4.Bind(wx.EVT_BUTTON, self.按钮4_按钮被单击)
        f = []
        p = []
        chmlfrp_p = []
        chmlfrp_f = []
        for root, dirs, files in os.walk(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'):
            for filespath in files:
                f.append(os.path.join(filespath))
                p.append(os.path.join(root, filespath))
            for i in range(len(f)):
                if f[i].lower().find("chmlfrp") == 0:
                    self.超级列表框1.Append([f'{f[i]}', f'{p[i]}'])
                    chmlfrp_p.append(f[i])
                    chmlfrp_f.append(p[i])
    def 超级列表框1_选中表项(self,event):
        self.按钮1.Enable()


    def 按钮1_按钮被单击(self,event):
        f = []
        p = []
        chmlfrp_p = []
        chmlfrp_f = []
        for root, dirs, files in os.walk(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'):
            for filespath in files:
                f.append(os.path.join(filespath))
                p.append(os.path.join(root, filespath))
            for i in range(len(f)):
                if f[i].lower().find("chmlfrp") == 0:
                    chmlfrp_p.append(f[i])
                    chmlfrp_f.append(p[i])
        start_up_warm = wx.MessageDialog(None, caption="警告",message=f"你确定要删除此启动项吗?",style=wx.YES_NO | wx.ICON_WARNING)
        if start_up_warm.ShowModal() == wx.ID_YES:
            del_start_up_user = os.popen(f'del /f /s /q "{chmlfrp_f[self.超级列表框1.GetFirstSelected()]}"').read()
            self.超级列表框1.ClearAll()
            self.按钮1.Disable()
            self.超级列表框1.AppendColumn('启动项名称', 0, 231)
            self.超级列表框1.AppendColumn('此启动项路径', 0, 871)
            f = []
            p = []
            chmlfrp_p = []
            chmlfrp_f = []
            for root, dirs, files in os.walk(
                    fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'):
                for filespath in files:
                    f.append(os.path.join(filespath))
                    p.append(os.path.join(root, filespath))
                for i in range(len(f)):
                    if f[i].lower().find("chmlfrp") == 0:
                        self.超级列表框1.Append([f'{f[i]}', f'{p[i]}'])
                        chmlfrp_p.append(f[i])
                        chmlfrp_f.append(p[i])
            start_up_info = wx.MessageDialog(None, caption="info", message=f"删除状态:{del_start_up_user}",style=wx.OK | wx.ICON_INFORMATION)
            if start_up_info.ShowModal() == wx.ID_OK:
                pass



    def 按钮2_按钮被单击(self,event):
        os.startfile(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')


    def 按钮4_按钮被单击(self,event):
        self.超级列表框1.ClearAll()
        self.按钮1.Disable()
        self.超级列表框1.AppendColumn('启动项名称', 0, 231)
        self.超级列表框1.AppendColumn('此启动项路径', 0, 871)
        f = []
        p = []
        chmlfrp_p = []
        chmlfrp_f = []
        for root, dirs, files in os.walk(
                fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup'):
            for filespath in files:
                f.append(os.path.join(filespath))
                p.append(os.path.join(root, filespath))
            for i in range(len(f)):
                if f[i].lower().find("chmlfrp") == 0:
                    self.超级列表框1.Append([f'{f[i]}', f'{p[i]}'])
                    chmlfrp_p.append(f[i])
                    chmlfrp_f.append(p[i])
        start_up_flushed = wx.MessageDialog(None, caption="info", message="刷新完成",style=wx.OK | wx.ICON_INFORMATION)
        if start_up_flushed.ShowModal() == wx.ID_OK:
            pass
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
        self.AddPage(chmlfrp_start_delete_usertunnel(self), "管理隧道")
        self.AddPage(start_up(self), "启动项管理")
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
        icon_base64 = "data:image/x-icon;base64,AAABAAEAgIAAAAEAIAAoCAEAFgAAACgAAACAAAAAAAEAAAEAIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOZWAATNXQws1WQNPNZqEGTpZglm7GQIg+tpEJnuaQmZ72kEne9oA5/xZwOh9GcDofRnA6HyZwOf7GkFm+trCJntagmT6GgFbt9qDWbfZAlK2GMWMt5VAAwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANVhGijgZBJe7WYJh+pmB6/vZgjd9GgI//ZnCf/6ZwX//GgC//xoAf/9aAL//GgB//xoAf/8aQD//GkA//1pAP/+aQD//mkA//1pAP/8aQD//GkA//1pAf/8aQL/+WgD//VmBf/3aQP/8WgG/+9nB+HuZwfB6WcKldxkE2jeYxc45FQABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADTZBUu1mUTcuZkDbPvZQvx8WYG//VoAv/6aQH//mgA//5pAf/9aAL//GkA//xpAf/8aAL//mgA//5pAP/+aQD//mkA//9pAP//aQD//mkA//5pAP/+aQD//2kA//5pAP/+aQD//mkA//xpAf/9aQD//mkA//1nAv/9aAL//WgB//tpAv/9aAL//GgB//ZpBP/tZwr75mcMx+NoC4HZYhlA31QABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4FQABOBlF0rnYRGX62YJ5fFrBf/5aQL/+mcB//lpAv/7agL//moB//5pAP/8agL//WkC//1pAP/+agD//moA//5oAP/9aQH//mkC//5pAv/9agD//WoA//1qAP/+aQD//mkA//5pAP/+aQD//WoA//5qAP/+agD//mkA//5oAf/+aQL//WkB//1pAf/9agH//GoA//1pAf/8aAD/92kA//tpAf/8ZwH/9WkD//RoA//tZgfz6WcNrdNlD1jRYw4OAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1GITLtpkDpHraQvt9mkD//ppA//+aQP//GgA//tpAP/9awH//WoB//9pAf//aQH//mkA//9pAP/+aQD//mkA//5pAP//aQD//mkA//5pAP/+aQD//mkA//5pAP//aQD//2kA//5pAP/+aQD//mkA//9pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//2kA//9pAP/+aQD//moA//5qAP/9agD//GsB//xqAP/8aQD//mgA//9oAP/+aAD/+2cC/+9nCPfmZg6p3F8SQgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADgYAgA1V4MUudnDMXwaAf//mgB//lqAv/8aQD//mgB//5oAf/+aQD//moA//5qAP/+agD//2kA//9pAP/+aQD//2kA//5pAP/+aQD//mgA//9oAP/+aAD//mkA//5oAP/+aAD//mgA//9pAP//aQD//mkA//5pAP/+aQD//2kA//5pAP/+aAD//mgA//5pAP/+aQD//mkA//5pAP//aAD//2gA//5oAP/+aQD//mkA//5pAP/+agD//moA//5pAP//aQD//mkA//5pAP/6awD//GwA//lqAf/wagT/7mYH3dtiD27KahYMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADeWgAC12UNYOlnC9n5ZgT/9mkC//ppAf/7agD/+mgC//1pAP/+agD//WkA//5pAP/+aQD//2kA//5pAP//aQD//2kA//5pAP//aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//2kA//9pAP//aQD//mkA//9pAP//aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//2kA//9pAP//aQD//mkA//5pAP/+aQD//mkA//9pAP/+aQD//mkA//5pAP//agH//2oA//xrAP/8agH//GgC//tpAf/4aQP/+mcF/+poCe3lYxB81VYZDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAz18SRudnC9X4aQL/+2oA//1pAP/+aQH//moB//5qAP/+aQD//2kA//5pAP/+aQD//mkA//5pAP//aQD//mkA//5pAP//aQD//mkA//9pAP/+aQD//2kA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP//aQD//2kA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//9pAP/+aQD//mkA//5pAP/+aQD//2kA//9pAP/+aQD//mkA//5pAP/+aAD//mkA//5pAP//aQD//mgA//9pAP/+aQD//mkA//5pAP/+aQD//moB//5pAf//aAD//WkA//1oAv/sZA3t1GYQbNVRAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2GEOGuZkCq/zaAX//WkA//pqAP/8agD//mkA//9pAP//aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//9pAP//aQD//mkA//9pAP/+aQD//2kA//5pAP/+aQD//mkA//9pAP/+aQD//mkA//5pAP/+aQD//mkA//9pAP//aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP//aQD//2kA//5pAP/+aQD//mkA//5pAP/+aAD//2kA//5oAP/+aQD//2kA//5pAP/+aQD//mkA//5pAP//aQD//2kA//5pAP/9aQL/92sA//1qAP/4ZwP/4mgM1dhoEDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN9fDlrzZgbv92gB//hpAP/6aQL//GkC//xqAP/+aQD//mkA//5pAP/+aQD//mgA//5pAP/+aQD//mkA//5pAP/+aQD//2kA//5pAP/+aQD//mkA//5pAP//aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//2kA//9pAP/+aQD//mkA//9pAP/+aQD//mkA//5pAP/+aQD//mkA//5pAP/+aQD//mkA//9pAP//aQD//mkA//5pAP/+aQD//mgA//5pAP/+aQD//mgA//9oAP//aQD//mkA//5pAP/+aQD//mkA//5pAP//aQD//mkA//1pAP/4aQH//GgD//hpBf/7awD/82kG/eJnDonWXw0IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANJjIgrjZA6j82oH//prAP/8aAL//mkC//5pAv/9aQH//GkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aAH//WkB//5pAf/+aQD//mkA//5pAP/9aQD//WkA//1pAP/9aQH//WgB//1pAf/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//WkA//1pAP/9aQD//GkB//1pAv/+aQL//WoA//xpAP/8aQH/+moB/+JkC83OahseAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADUXAoY7GIQxfpoBP/8agH//GoA//xqAP/+aQD//2kA//9pAP/+agD//moA//9qAP/+agD//2oA//9qAP//agD//moA//9qAP/+agD//moA//9qAP/+agD//2oA//9qAP/+agD//2oA//5qAP//agD//moA//9qAP/+agD//2oA//5qAP/+agD//moA//9qAP//agD//2kA//5pAP/+aQD//2kA//5pAP/+aQD//2kA//5oAP/+aAD//mgA//9pAP//aQD//2kA//5qAP/+agD//moA//5qAP/+agD//moA//9qAP/+agD//2oA//9qAP/+agD//2oA//5qAP//agD//2oA//9qAP/+aQD//moA//9pAP/+aQD//2gA//5oAP/+ZwH/+WoC/+9mBefUXg00AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAOtlD9ncaxVcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADdZBB44mQLswAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAC4VxMW5mUP/8FPABgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA52YPsd5gEHQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANdjCmLhYwrBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADjZAz/vlcIKAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADjagyZ3GAMgwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1GMKZOFkCsMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOBmCv++WgcqAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOJoC5nfYQ6HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADVZAhk4WILwQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4GQL/8FaCioAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4mUNmeBiCIcAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANhnB2TiYQzBAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADhZAr/wloPKgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADmZQ6Z32QIhQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA22UFg+JhC78AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAvFwWIuZmBv/EVAMmAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOhkDLvbYQ18AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADjZQaj5GUPnwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADPXhU66moJ+8xMAAYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA7GcO2dtjFGAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAOllCNveYQyFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANtgEnTsZwfXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANheERLnaQz/3l4SPgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADYTwAE7WQL8fJnA//lZBCXAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4mMPkfNrAP/wZgzvy2gdDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA2GEaLvJnCf/zaAP/2GYaXgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANVg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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4l8Qg+FlDsUAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA0lgUGO1iC//QZR8qAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAONnCrnkZRGRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADjZRCZ32QOlwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADQXhgu5GUM+QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4WYMzdxlE2IAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAORlC5nfYg2TAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAMlbCyzkZwrxAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADqZg/N1mMTYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAADZYRFi6WcL699jDAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA6mYJ/d1nFVIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA4GcPl+hkELMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAN9dETzsaAj/1GQUSAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA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AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5jD0DUZxVky3MoCgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM5fCRjMZBVmvWwjFAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAANtfDgDbZBVW1GQVRAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8AD/////////////////8AAAAP///////////////wAAAAAH//////////////AAAAAAAP////////////+AAAAAAAAf///////////+AAAAAAAAB///////////+AAAAAAAAAH//////////+AAAAAAAAAAf/////////+AAAAAAAAAAB//////////AAAAAAAAAAAH/////////AAAAAAAAAAAA/////////gAAAAAAAAAAAH////////wAAAAAAAAAAAA////////4AAAAAAAAAAAAH///////8f///////////4///////+H////////////H///////j////////////5/5/////x////////////+PAA////8/////////////xAAD///+P////////////8D58f///3/////////////jwBz//////////////////5/M//////////////////+fzP///gAAAAAAAAAAAAADzxz///wAAAAAAAAAAAAAAPn5///8AAAAAAAAAAAAAAAfg///+P//////////////AA////n///////////////D////5////////////////////+fx///////////////////n3////j/////////H////57////4/////////x////+f/v//+P////////8f////nP/f//j8////////H////5x/3//Y/P//////3x/////M/+//uPx//////98f////z/7j/nj+f/////+/H////8//+Pj4/j//////Px/////P/fwD8P8f/////n8f////57v///D/j/////z/P////8f////gf8P////x/z/////D////5H/gf///w/8/////w////8R/+A///A/+P////4H///+Of/4AHwA//n////+A////njz/wAAB//5/////AH///x48//4AP//cf////wA///4/HH//////3P////8AH//4fx5//////7j////+AAf/8P+eP/////85//////4B/4P/jw/////+cf/////+AAAP/8eH////+PP//////gAAP//Hwf///+Hj//////4B////4/A///8Hx//////+A/////H8A//wH8f//////g/////w/wAAAH+P//////4f////+H/wAAf/H//////+f/////w//////j/////////////+H/////x//////////////w/////w//////////////+H////4f//////////////wf///4P//////////////+B///4H///////////////4H//4H////////////////gH/gD////////////////+AAAD/////////////////4AAH////////////+f+P/P4Af/////////////D/D/x////////////////wfwf8f///////////////8H8H/D////////////////B/A/w/////////////////f/P/v////////////////3/7/7////////////////8/+/+/////////////////v/v/v////////////////7/7/5////////////////+/+/+f////////////////v/v/n////////////////7/7/5////////////////8/+/+/////////////////P/v/v////////////////z/7/7////////////////9/8/+////////////////+f/P/P////////////////n/n/z////////////////x/5/5////////////////8/8f+f///////////////+P/P/H////////////////j/j/z////////////////5/4/4////////////////8f+f+f////////////////P/H/n////////////////z/z/7////////////////9/8/+/////////////////f/f/P////////////////n/3/z////////////////5/9/9////////////////+f/f/f////////////////n/3/3////////////////5/9/9////////////////+f/f/f////////////////3/3/z////////////////9/9/8/////////////////f/P/v////////////////z/z/5////////////////8P+P+H////////////////j/j/h////////////////4/4/8f////////////////P/P/H//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////8=".split(';base64,')[1]
        icon_base64_encode = BytesIO(base64.b64decode(icon_base64))
        icon_ok = wx.Image(icon_base64_encode).ConvertToBitmap()
        icon = wx.Icon(icon_ok)
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
