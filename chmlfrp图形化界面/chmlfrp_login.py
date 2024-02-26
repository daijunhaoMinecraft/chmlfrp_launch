# -*- coding:utf-8 -*-
import json
import os
import requests
import wx
import winreg
import wx.adv
import sys
#关闭证书警告
requests.packages.urllib3.disable_warnings()
#获取当前路径
pathx = os.path.dirname(os.path.abspath(__file__))
pathx_pyinstaller = os.path.dirname(os.path.realpath(sys.argv[0]))
#请求头
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
}
#获取文档路径
def Personal():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
    path = winreg.QueryValueEx(key, "Personal")[0]
    return path

#创建图形化界面
class Frame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title='chmlfrp', size=(1200, 800),name='frame',style=541072384)
        self.启动窗口 = wx.Panel(self)
        self.Centre()
        self.标签1 = wx.StaticText(self.启动窗口,size=(190, 20),pos=(485, 190),label='欢迎使用Chmlfrp',name='staticText',style=2321)
        标签1_字体 = wx.Font(9,74,90,700,False,'Microsoft YaHei UI',28)
        self.标签1.SetFont(标签1_字体)
        self.chmlfrp_user = wx.TextCtrl(self.启动窗口,size=(250, 22),pos=(464, 242),value='',name='text',style=0)
        self.标签2 = wx.StaticText(self.启动窗口,size=(35, 24),pos=(424, 244),label='账号:',name='staticText',style=2321)
        self.chmlfrp_password = wx.TextCtrl(self.启动窗口,size=(250, 22),pos=(464, 298),value='',name='text',style=wx.TE_PASSWORD)
        self.chmlfrp_password_show = wx.TextCtrl(self.启动窗口, size=(250, 22), pos=(464, 298), value='', name='text',style=0)
        self.标签3 = wx.StaticText(self.启动窗口,size=(35, 24),pos=(424, 298),label='密码:',name='staticText',style=2321)
        self.按钮1 = wx.Button(self.启动窗口,size=(80, 32),pos=(532, 390),label='登录',name='button')
        self.按钮1.Bind(wx.EVT_BUTTON,self.按钮1_按钮被单击)
        self.user_password = wx.RadioButton(self.启动窗口,size=(139, 24),pos=(722, 298),name='radioButton',label='使用账号密码登录')
        self.user_password.SetValue(True)
        self.user_password.Bind(wx.EVT_RADIOBUTTON,self.user_password_状态被改变)
        self.标签4 = wx.StaticText(self.启动窗口,size=(36, 24),pos=(423, 350),label='token:',name='staticText',style=2321)
        self.user_token = wx.RadioButton(self.启动窗口,size=(117, 24),pos=(722, 348),name='radioButton',label='使用token登录')
        self.user_token.Bind(wx.EVT_RADIOBUTTON,self.user_token_状态被改变)
        self.chmlfrp_token = wx.TextCtrl(self.启动窗口,size=(250, 22),pos=(464, 348),value='',name='text',style=wx.TE_PASSWORD)
        self.chmlfrp_token_show = wx.TextCtrl(self.启动窗口, size=(250, 22), pos=(464, 348), value='', name='text',style=0)
        self.超级链接框1 = wx.adv.HyperlinkCtrl(self.启动窗口, size=(148, 22), pos=(18, 15), name='hyperlink',label='免费注册一个chmlfrp账号', url='panel.chmlfrp.cn/register',style=1)
        self.标签5 = wx.StaticText(self.启动窗口, size=(148, 22), pos=(18, 44), label='token指的是用户密钥',name='staticText', style=17)
        self.display_password = wx.CheckBox(self.启动窗口, size=(167, 24), pos=(872, 298), name='check',label='显示密码', style=16384)
        self.display_password.SetValue(False)
        self.display_password.Bind(wx.EVT_CHECKBOX, self.display_password_狀态被改变)
        self.display_token = wx.CheckBox(self.启动窗口, size=(167, 24), pos=(872, 348), name='check', label='显示token',style=16384)
        self.display_token.SetValue(False)
        self.display_token.Bind(wx.EVT_CHECKBOX, self.display_token_狀态被改变)
        self.chmlfrp_password_show.Hide()
        self.chmlfrp_token_show.Hide()
        self.chmlfrp_token.Disable()
        self.chmlfrp_token_show.Disable()
        if os.path.exists(f"{pathx_pyinstaller}\\frpc.exe"):
            pass
        else:
            frpc_file_Error = wx.MessageDialog(None, caption="Error",message=f"未检测到frpc文件,请检查你是否有被删除,如果有,请下载frpc文件到此文件夹目录下",style=wx.OK | wx.ICON_ERROR)
            if frpc_file_Error.ShowModal() == wx.ID_OK:
                sys.exit()
        if os.path.exists(f"{pathx_pyinstaller}\\chmlfrp_user.exe"):
            pass
        else:
            frpc_file_Error = wx.MessageDialog(None, caption="Error",message=f"未检测到chmlfrp_user文件,请检查你是否有被删除,如果有,请重新下载",style=wx.OK | wx.ICON_ERROR)
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
                    os.system(f"start {pathx_pyinstaller}\\chmlfrp_user.exe {user_password_info['token']}")
                    self.Destroy()
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
                    os.system(f"start {pathx_pyinstaller}\\chmlfrp_user.exe {self.chmlfrp_token.GetValue()}")
                    self.Destroy()
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
