import sys
import requests
import json
import os
from win10toast import ToastNotifier
toaster = ToastNotifier()
import datetime
import platform
import psutil
import winreg
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
#启动: 此文件 <token> <隧道序号-1>
get_token = sys.argv[1]
get_usertunnel_select = int(sys.argv[2])
usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/usertunnel.php?token={get_token}",headers=headers,verify=False).text)
try:
    with open(f"{pathx_pyinstaller}\\frpc.ini",mode="w",encoding="utf-8") as f:
        f.write(json.loads(requests.get(f"https://panel.chmlfrp.cn/api/frpconfig.php?usertoken={get_token}&node={usertunnel_info[get_usertunnel_select]['node']}",verify=False,headers=headers).text)['message'])
        f.close()
except Exception as e:
    toaster.show_toast("出现错误",f"{e}", duration=10)
    sys.exit()
os.system("cls")
os.system(f"start cmd /c \"@echo off&echo ChmlFrp日志信息 - {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}生成&echo.&echo ===========设备信息==============&echo.&echo 系统/系统版本:{platform.platform()}&echo 操作系统位数:{platform.architecture()[0]}&echo 处理器信息:{getcpu()}&echo 机带RAM:{round(psutil.virtual_memory().total / (1024**3))}GB&echo.&echo ===========隧道信息==============&echo.&echo 隧道ID:{usertunnel_info[get_usertunnel_select]['id']}&echo 隧道名称:{usertunnel_info[get_usertunnel_select]['name']}&echo 隧道类型:{usertunnel_info[get_usertunnel_select]['type']}&echo 内网IP:{usertunnel_info[get_usertunnel_select]['localip']}&echo 内网端口:{usertunnel_info[get_usertunnel_select]['nport']}&echo 外网端口/域名:{usertunnel_info[get_usertunnel_select]['dorp']}&echo 节点名称:{usertunnel_info[get_usertunnel_select]['node']}&echo 连接地址:{usertunnel_info[get_usertunnel_select]['ip']}&echo.&echo ===========FRPC输出==============&{pathx_pyinstaller}\\frpc.exe -u {sys.argv[1]} -p {usertunnel_info[get_usertunnel_select]['id']}&echo frpc已终止,按任意键退出&pause\"")
toaster.show_toast(f"隧道正在启动--{usertunnel_info[get_usertunnel_select]['name']}",f"隧道ip地址:{usertunnel_info[get_usertunnel_select]['ip']}",duration=10)
sys.exit()