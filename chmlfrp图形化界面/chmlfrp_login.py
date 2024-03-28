# -*- coding:utf-8 -*-
from Taowa_wx import *
from Taowa_skin import *
#皮肤加载
皮肤_加载(皮肤.Areo)

from wx.html2 import WebView
import pyperclip3 as pycopy
import random
import string
import getpass
import json
import os
import requests
import wx
import winreg
import wx.adv
import sys
from io import BytesIO
from PIL import Image


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


class chmlfrp_user(wx.Panel):
    def __init__(self, parent):
        global chmlfrp_user_info
        wx.Panel.__init__(self, parent=parent, id=wx.ID_ANY)
        self.标签1 = wx_StaticTextL(self,size=(80, 24),pos=(7, 25),label='用户名:',name='staticText',style=257)
        self.chmlfrp_user = wx_TextCtrl(self,size=(285, 22),pos=(91, 22),value='',name='text',style=16)
        self.user_email = wx_StaticTextL(self,size=(80, 24),pos=(7, 59),label='用户邮箱:',name='staticText',style=257)
        self.chmlfrp_email = wx_TextCtrl(self,size=(285, 22),pos=(91, 60),value='',name='text',style=16)
        self.chmlfrp_qq = wx_TextCtrl(self,size=(285, 22),pos=(91, 97),value='',name='text',style=16)
        self.标签3 = wx_StaticTextL(self,size=(80, 24),pos=(7, 96),label='用户QQ号:',name='staticText',style=257)
        self.chmlfrp_user_img = wx.StaticBitmap(self,size=(40, 40),pos=(1097, 28),name='staticBitmap',style=33554432)
        self.chmlfrp_info = wx_TextCtrl(self,size=(366, 249),pos=(7, 151),value='',name='text',style=wx.TE_READONLY | wx.TE_MULTILINE)
        self.标签4 = wx_StaticTextL(self,size=(191, 24),pos=(7, 414),label='userinfo返回json(小白请无视):',name='staticText',style=1)
        self.debug_json_user_info = wx_TextCtrl(self,size=(366, 201),pos=(7, 447),value='',name='text',style=1073745968)
        self.resusertoken = wx_Button(self,size=(80, 32),pos=(7, 664),label='重置token',name='button')
        self.resusertoken.SetForegroundColour((255, 0, 0, 255))
        self.resusertoken.Bind(wx.EVT_BUTTON,self.resusertoken_按钮被单击)
        self.标签5 = wx_StaticTextL(self,size=(106, 24),pos=(405, 22),label='当前登录用户token:',name='staticText',style=0)
        self.编辑框6 = wx_TextCtrl(self,size=(305, 22),pos=(521, 21),value='',name='text',style=wx.TE_PASSWORD | wx.TE_READONLY)
        self.copy_token = wx_Button(self,size=(80, 32),pos=(931, 17),label='复制token',name='button')
        self.copy_token.Bind(wx.EVT_BUTTON,self.copy_token_按钮被单击)
        self.display_token = wx_CheckBox(self,size=(84, 24),pos=(838, 20),name='check',label='显示token',style=16384)
        self.display_token.Bind(wx.EVT_CHECKBOX,self.display_token_狀态被改变)


        # 获取登录信息
        chmlfrp_user_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/userinfo.php?usertoken={user_token_acces}", headers=headers,verify=False).text)
        chmlfrp_user_info_dump = json.dumps(chmlfrp_user_info, indent=4, ensure_ascii=False)
        # 用户主界面
        try:
            if chmlfrp_user_info['username']:
                user_token_login_OK = wx.MessageDialog(None, caption="info",message=f"登录成功,登录账号:{chmlfrp_user_info['username']}",style=wx.OK | wx.ICON_INFORMATION)
                if user_token_login_OK.ShowModal() == wx.ID_OK:
                    pass
        except KeyError:
            user_token_login_Error = wx.MessageDialog(None, caption="Error", message=f"{chmlfrp_user_info['error']}",style=wx.OK | wx.ICON_ERROR)
            if user_token_login_Error.ShowModal() == wx.ID_OK:
                sys.exit()
        self.chmlfrp_user.SetLabel(f"{chmlfrp_user_info['username']}")
        self.chmlfrp_email.SetLabel(f"{chmlfrp_user_info['email']}")
        self.chmlfrp_qq.SetLabel(f"{chmlfrp_user_info['qq']}")
        #获取用户头像
        self.chmlfrp_user_img.SetBitmap(wx.Image(BytesIO(requests.get(f"{chmlfrp_user_info['userimg']}",headers=headers,verify=False).content)).ConvertToBitmap())
        #获取签到状态
        qd = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/qdxx.php?userid={chmlfrp_user_info['userid']}",verify=False,headers=headers).text)
        if qd['is_signed_in_today'] == True:
            qd_info = f"今天已经签到了\n累计签到次数:{qd['total_sign_ins']}次\n累计签到获得的积分:{qd['total_points']}分\n今天一共签到的人数:{qd['count_of_matching_records']}人\n你的上一次签到时间为:{qd['last_sign_in_time']}"
        if qd['is_signed_in_today'] == False:
            qd_info = f"今天还未签到\n累计签到次数:{qd['total_sign_ins']}次\n累计签到获得的积分:{qd['total_points']}分\n今天一共签到的人数:{qd['count_of_matching_records']}人\n你的上一次签到时间为:{qd['last_sign_in_time']}"
        self.chmlfrp_info.SetValue(f'当前用户id:{str(chmlfrp_user_info["userid"])}\n当前用户组:{str(chmlfrp_user_info["usergroup"])}\n到期时间:{chmlfrp_user_info["term"]}\n当前用户隧道数量:{chmlfrp_user_info["tunnelstate"]} / {chmlfrp_user_info["tunnel"]}\n当前用户宽带限制:国内:{chmlfrp_user_info["bandwidth"]}Mbps | 国外:{str(int(chmlfrp_user_info["bandwidth"]) * 4)}M\n当前用户实名状态:{chmlfrp_user_info["realname"]}\n当前用户积分数:{str(chmlfrp_user_info["integral"])}\n{qd_info}')
        self.编辑框6_show = wx.TextCtrl(self, size=(305, 22), pos=(521, 21), value='', name='text', style=wx.TE_READONLY)
        self.编辑框6.SetLabel(f"{user_token_acces}")
        self.编辑框6_show.SetLabel(f"{user_token_acces}")
        self.debug_json_user_info.SetValue(chmlfrp_user_info_dump)
        self.编辑框6_show.Hide()

    #重置用户token
    def resusertoken_按钮被单击(self, event):
        resusertoken_warm = wx.MessageDialog(None, caption="警告", message="你确定要重置token吗?",style=wx.YES_NO | wx.ICON_WARNING)
        if resusertoken_warm.ShowModal() == wx.ID_YES:
            resusertoken_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/resusertoken.php?usertoken={user_token_acces}",headers=headers,verify=False).text)
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
        pycopy.copy(f"{user_token_acces}")
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
        self.按钮4 = wx.Button(self, size=(224, 85), pos=(591, 630), label='添加自启动项目', name='button')
        按钮4_字体 = wx.Font(9, 70, 90, 700, False, 'Microsoft YaHei UI', 28)
        self.按钮4.SetFont(按钮4_字体)
        self.按钮4.SetForegroundColour((255, 128, 64, 255))
        self.按钮4.Bind(wx.EVT_BUTTON, self.按钮4_按钮被单击)
        self.按钮4.Disable()
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}", headers=headers,verify=False).text)
        self.start_usertunnel.Disable()
        self.delete_usertunnel.Disable()
        try:
            for i in range(len(usertunnel_info)):
                if str(usertunnel_info[i]['nodestate']) == "offline":
                    self.usertunnel_list.Append([f'{str(i + 1)}.[离线节点]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
                if str(usertunnel_info[i]['nodestate']) == "online":
                    self.usertunnel_list.Append([f'{str(i + 1)}.[正常隧道]', f'{usertunnel_info[i]["name"]}', f'{usertunnel_info[i]["id"]}', f'{usertunnel_info[i]["ip"]}', f'{usertunnel_info[i]["uptime"]}', f'{usertunnel_info[i]["node"]}', f'{usertunnel_info[i]["localip"]}', f'{usertunnel_info[i]["nport"]}', f'{usertunnel_info[i]["type"]}',f'{usertunnel_info[i]["dorp"]}', f'{usertunnel_info[i]["state"]}', f'{usertunnel_info[i]["nodestate"]}', f'{usertunnel_info[i]["encryption"]}', f'{usertunnel_info[i]["compression"]}', f'{usertunnel_info[i]["ap"]}', f'{usertunnel_info[i]["client_version"]}'])
        except KeyError:
            pass

    def 按钮4_按钮被单击(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
        with open(fr'C:\Users\{getpass.getuser()}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\chmlfrp-{usertunnel_info[self.usertunnel_list.GetFirstSelected()]["name"]}.bat',mode="w",encoding="ANSI") as f:
            f.write(f"start {pathx_pyinstaller}\\start_frpc.exe {user_token_acces} {str(self.usertunnel_list.GetFirstSelected())}")
        start_up_write_info = wx.MessageDialog(None, caption="info", message=f"自启动添加完成,若需要删除自启动请到启动项管理中删除",style=wx.OK | wx.ICON_INFORMATION)
        if start_up_write_info.ShowModal() == wx.ID_YES:
            pass

    def usertunnel_list_选中表项(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
        try:
            frpc_config = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/frpconfig.php?usertoken={user_token_acces}&node={usertunnel_info[self.usertunnel_list.GetFirstSelected()]['node']}",verify=False,headers=headers).text)['message']
            self.编辑框2.SetLabel(frpc_config)
            self.delete_usertunnel.Enable()
            self.start_usertunnel.Enable()
            self.按钮4.Enable()
        except Exception:
            self.按钮4.Disable()
            self.start_usertunnel.Disable()
            self.delete_usertunnel.Disable()


    def start_usertunnel_按钮被单击(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
        os.system(f"start {pathx_pyinstaller}\\start_frpc.exe {user_token_acces} {str(usertunnel_info[self.usertunnel_list.GetFirstSelected()]['id'])}")
        user_usertunnel_OK = wx.MessageDialog(None, caption="info",message=f"已执行隧道启动命令,是否复制ip?",style=wx.YES_NO | wx.ICON_INFORMATION)
        if user_usertunnel_OK.ShowModal() == wx.ID_YES:
            pycopy.copy(usertunnel_info[self.usertunnel_list.GetFirstSelected()]['ip'])
            copy_ok = wx.MessageDialog(None, caption="info", message=f"ip复制完成",style=wx.OK | wx.ICON_INFORMATION)
            if copy_ok.ShowModal() == wx.ID_OK:
                pass


    def delete_usertunnel_按钮被单击(self,event):
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
        delete_warm = wx.MessageDialog(None, caption="警告", message="你确定要删除此隧道吗?",style=wx.YES_NO | wx.ICON_WARNING)
        if delete_warm.ShowModal() == wx.ID_YES:
            delete_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/deletetl.php?token={user_token_acces}&nodeid={usertunnel_info[self.usertunnel_list.GetFirstSelected()]['id']}&userid={str(chmlfrp_user_info['userid'])}",headers=headers,verify=False).text)
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
            usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
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
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
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
                      "token": f"{user_token_acces}",
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
            "HTTP_TOKEN": f"{user_token_acces}"
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
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
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
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}", headers=headers,verify=False).text)
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
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}", headers=headers,verify=False).text)
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
                  "usertoken": F"{user_token_acces}",
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
            "HTTP_TOKEN": f"{user_token_acces}"
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
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
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
        usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={user_token_acces}",headers=headers,verify=False).text)
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
        icon_bytes = BytesIO()
        Image.open(BytesIO(requests.get("https://chmlfrp.cn/favicon.ico", headers=headers, verify=False).content)).resize((128, 128), Image.LANCZOS).save(icon_bytes, 'ico')
        icon_ok = wx.Image(icon_bytes).ConvertToBitmap()
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

#创建图形化界面
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='chmlfrp登录界面', size=(1200, 800),name='frame',style=541072384)
        self.启动窗口 = wx_StaticText(self)
        self.Centre()
        self.标签1 = wx_StaticTextL(self.启动窗口,size=(190, 20),pos=(485, 190),label='欢迎使用Chmlfrp',name='staticText',style=257)
        标签1_字体 = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.标签1.SetFont(标签1_字体)
        self.chmlfrp_user = wx_TextCtrl(self.启动窗口,size=(250, 22),pos=(464, 242),value='',name='text',style=0)
        self.标签2 = wx_StaticTextL(self.启动窗口,size=(35, 24),pos=(424, 244),label='账号:',name='staticText',style=257)
        self.chmlfrp_password = wx_TextCtrl(self.启动窗口,size=(250, 22),pos=(464, 298),value='',name='text',style=wx.TE_PASSWORD)
        self.标签3 = wx_StaticTextL(self.启动窗口,size=(35, 24),pos=(424, 298),label='密码:',name='staticText',style=257)
        self.按钮1 = wx_Button(self.启动窗口,size=(80, 32),pos=(532, 390),label='登录',name='button')
        self.按钮1.Bind(wx.EVT_BUTTON,self.按钮1_按钮被单击)
        self.user_password = wx_RadioButton(self.启动窗口,size=(139, 24),pos=(722, 298),name='radioButton',label='使用账号密码登录')
        self.chmlfrp_token = wx_TextCtrl(self.启动窗口,size=(250, 22),pos=(464, 348),value='',name='text',style=wx.TE_PASSWORD)
        self.标签4 = wx_StaticTextL(self.启动窗口,size=(36, 24),pos=(423, 350),label='token:',name='staticText',style=257)
        self.user_token = wx_RadioButton(self.启动窗口,size=(117, 24),pos=(722, 348),name='radioButton',label='使用token登录')
        self.超级链接框1 = wx_adv_HyperlinkCtrl(self.启动窗口,size=(148, 22),pos=(18, 15),name='hyperlink',label='免费注册一个chmlfrp账号',url='panel.chmlfrp.cn/register',style=1)
        self.标签5 = wx_StaticTextL(self.启动窗口,size=(148, 22),pos=(18, 44),label='token指的是用户密钥',name='staticText',style=1)
        self.display_password = wx_CheckBox(self.启动窗口,size=(167, 24),pos=(872, 298),name='check',label='显示密码',style=16384)
        self.display_password.Bind(wx.EVT_CHECKBOX,self.display_password_狀态被改变)
        self.display_token = wx_CheckBox(self.启动窗口,size=(167, 24),pos=(872, 348),name='check',label='显示token',style=16384)
        self.display_token.Bind(wx.EVT_CHECKBOX,self.display_token_狀态被改变)
        self.chmlfrp_password_show = wx.TextCtrl(self.启动窗口, size=(250, 22), pos=(464, 298), value='', name='text',style=0)
        self.chmlfrp_token_show = wx.TextCtrl(self.启动窗口, size=(250, 22), pos=(464, 348), value='', name='text',style=0)
        icon_bytes = BytesIO()
        Image.open(BytesIO(requests.get("https://chmlfrp.cn/favicon.ico",headers=headers,verify=False).content)).resize((128, 128), Image.LANCZOS).save(icon_bytes, 'ico')
        icon_ok = wx.Image(icon_bytes).ConvertToBitmap()
        icon = wx.Icon(icon_ok)
        self.SetIcon(icon)
        self.user_password.SetValue(True)
        self.display_token.SetValue(False)
        self.display_password.SetValue(False)
        self.chmlfrp_password_show.Hide()
        self.chmlfrp_token_show.Hide()
        self.chmlfrp_token.Disable()
        self.chmlfrp_token_show.Disable()
        if os.path.exists(f"{pathx_pyinstaller}\\start_frpc.exe"):
            pass
        else:
            start_frpc_file_Error = wx.MessageDialog(None, caption="Error",message=f"未检测到start_frpc文件,请检查你是否有被删除,如果有,请重新下载文件",style=wx.OK | wx.ICON_ERROR)
            if start_frpc_file_Error.ShowModal() == wx.ID_OK:
                sys.exit()
        if os.path.exists(f"{pathx_pyinstaller}\\frpc.exe"):
            pass
        else:
            frpc_file_Error = wx.MessageDialog(None, caption="Error",message=f"未检测到frpc文件,请检查你是否有被删除,如果有,请从chmlfrp官网上下载此文件",style=wx.OK | wx.ICON_ERROR)
            if frpc_file_Error.ShowModal() == wx.ID_OK:
                sys.exit()

        #读取账号密码(或token)如果没有,则跳过
        try:
            with open(f"{Personal()}\\chmlfrp_user_password.json",mode="r",encoding="utf-8") as f:
                chmlfrp_user_password = json.loads(f.read())
                self.chmlfrp_user.SetLabel(chmlfrp_user_password['user'])
                self.chmlfrp_password.SetLabel(chmlfrp_user_password['password'])
                f.close()
        except Exception:
            pass
        try:
            with open(f"{Personal()}\\chmlfrp_token.json",mode="r",encoding="utf-8") as f:
                chmlfrp_token_read = json.loads(f.read())
                self.chmlfrp_token.SetLabel(chmlfrp_token_read['token'])
                f.close()
        except Exception:
            pass


    def 按钮1_按钮被单击(self,event):
        global user_token_acces
        #当用户选择使用账号密码登录
        if self.user_password.GetValue() == True:
            if self.display_password.GetValue() == True:
                self.chmlfrp_password.SetLabel(self.chmlfrp_password_show.GetValue())
            user_password_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/login.php?username={self.chmlfrp_user.GetValue()}&password={self.chmlfrp_password.GetValue()}",headers=headers,verify=False).text)
            try:
                if user_password_info['message'] == "登录成功":
                    with open(f"{Personal()}\\chmlfrp_user_password.json",mode="w",encoding="utf-8") as f:
                        data = {
                            "user": f"{self.chmlfrp_user.GetValue()}",
                            "password": f"{self.chmlfrp_password.GetValue()}"
                        }
                        f.write(json.dumps(data, indent=4, ensure_ascii=False))
                        f.close()
                    user_token_acces = user_password_info['token']
                    self.Destroy()
                    main()
            except KeyError:
                user_password_login_Error = wx.MessageDialog(None, caption="Error", message=f"{user_password_info['error']}",style=wx.OK | wx.ICON_ERROR)
                if user_password_login_Error.ShowModal() == wx.ID_OK:
                    pass
        #当用户选择使用token登录
        elif self.user_token.GetValue() == True:
            if self.display_token.GetValue() == True:
                self.chmlfrp_token.SetLabel(self.chmlfrp_token_show.GetValue())
            user_token_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/userinfo.php?usertoken={self.chmlfrp_token.GetValue()}",headers=headers,verify=False).text)
            try:
                if user_token_info['username']:
                    with open(f"{Personal()}\\chmlfrp_token.json",mode="w",encoding="utf-8") as f:
                        data = {
                            "token": f"{self.chmlfrp_token.GetValue()}"
                        }
                        f.write(json.dumps(data, indent=4, ensure_ascii=False))
                        f.close()
                    user_token_acces = self.chmlfrp_token.GetValue()
                    self.Destroy()
                    main()
            except KeyError:
                user_token_login_Error = wx.MessageDialog(None, caption="Error",message=f"{user_token_info['error']}",style=wx.OK | wx.ICON_ERROR)
                if user_token_login_Error.ShowModal() == wx.ID_OK:
                    pass

    def display_password_狀态被改变(self,event):
        if self.display_password.GetValue() == True:
            self.display_password.SetValue(False)
            chmlfrp_display_password_warm = wx.MessageDialog(None, caption="警告", message="你确定要显示密码?\n请不要随意将账号密码发送给任何人!",style=wx.YES_NO | wx.ICON_WARNING)
            if chmlfrp_display_password_warm.ShowModal() == wx.ID_YES:
                self.display_password.SetValue(True)
                self.chmlfrp_password_show.SetLabel(self.chmlfrp_password.GetValue())
                self.chmlfrp_password.Hide()
                self.chmlfrp_password_show.Show()
                self.启动窗口.Layout()
            else:
                self.display_password.SetValue(False)
        elif self.display_password.GetValue() == False:
            self.chmlfrp_password.SetLabel(self.chmlfrp_password_show.GetValue())
            self.chmlfrp_password_show.Hide()
            self.chmlfrp_password.Show()
            self.启动窗口.Layout()


    def display_token_狀态被改变(self,event):
        if self.display_token.GetValue() == True:
            self.display_token.SetValue(False)
            chmlfrp_display_token_warm = wx.MessageDialog(None, caption="警告",message="你确定要显示token?\n请不要随意将token发送给任何人!",style=wx.YES_NO | wx.ICON_WARNING)
            if chmlfrp_display_token_warm.ShowModal() == wx.ID_YES:
                self.display_token.SetValue(True)
                self.chmlfrp_token_show.SetLabel(self.chmlfrp_token.GetValue())
                self.chmlfrp_token.Hide()
                self.chmlfrp_token_show.Show()
                self.启动窗口.Layout()
            else:
                self.display_token.SetValue(False)
        elif self.display_token.GetValue() == False:
            self.chmlfrp_token.SetLabel(self.chmlfrp_token_show.GetValue())
            self.chmlfrp_token_show.Hide()
            self.chmlfrp_token.Show()
            self.启动窗口.Layout()


    def user_password_状态被改变(self,event):
        if self.user_password.GetValue() == False:
            self.chmlfrp_user.Disable()
            self.chmlfrp_password.Disable()
            self.chmlfrp_password_show.Disable()
            self.chmlfrp_token.Enable()
            self.chmlfrp_token_show.Enable()
            self.chmlfrp_token.Enable()
        if self.user_password.GetValue() == True:
            self.chmlfrp_user.Enable()
            self.chmlfrp_password.Enable()
            self.chmlfrp_password_show.Enable()
            self.chmlfrp_token.Disable()
            self.chmlfrp_token_show.Disable()



    def user_token_状态被改变(self,event):
        if self.user_token.GetValue() == False:
            self.chmlfrp_token.Disable()
            self.chmlfrp_token_show.Disable()
            self.chmlfrp_user.Enable()
            self.chmlfrp_password.Enable()
            self.chmlfrp_token_show.Enable()
        if self.user_token.GetValue() == True:
            self.chmlfrp_token.Enable()
            self.chmlfrp_token_show.Enable()
            self.chmlfrp_user.Disable()
            self.chmlfrp_password.Disable()
            self.chmlfrp_password_show.Disable()

class myApp(wx.App):
    def  OnInit(self):
        self.frame = Frame()
        self.frame.Show(True)
        return True

if __name__ == '__main__':
    app = myApp()
    app.MainLoop()