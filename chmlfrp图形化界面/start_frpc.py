import sys
import requests
import json
import os
from plyer import notification
import datetime
import platform
import psutil
import winreg
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
#启动: 此文件 <token> <隧道id>
try:
    usertunnel_info = json.loads(requests.get(f"https://panel.chmlfrp.cn/api/tunnelinfo.php?id={id}",headers=headers,verify=False).text)
except Exception as e:
    notification.notify(title='出现错误', message=f'{e}', app_icon=f"{pathx}\\system_Error.ico", timeout=10)
    sys.exit()
os.system(f"start cmd /c \"@echo off&echo ChmlFrp日志信息 - {datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')}生成&echo.&echo ===========设备信息==============&echo.&echo 系统/系统版本:{platform.platform()}&echo 操作系统位数:{platform.architecture()[0]}&echo 处理器信息:{getcpu()}&echo 机带RAM:{round(psutil.virtual_memory().total / (1024**3))}GB&echo.&echo ===========隧道信息==============&echo.&echo 隧道ID:{usertunnel_info['tunnel_id']}&echo 隧道名称:{usertunnel_info['tunnel_name']}&echo 隧道类型:{usertunnel_info['tunnel_type']}&echo 内网IP:{usertunnel_info['tunnel_localip']}&echo 内网端口:{usertunnel_info['tunnel_nport']}&echo 外网端口/域名:{usertunnel_info['tunnel_dorp']}&echo 节点名称:{usertunnel_info['name']}&echo 连接地址:{usertunnel_info['iparea']}&echo.&echo ===========FRPC输出==============&{pathx_pyinstaller}\\frpc.exe -u {token} -p {id}&echo frpc已终止,按任意键退出&pause\"")
notification.notify(title = f"隧道正在启动--{usertunnel_info['tunnel_name']}",message = f"隧道ip地址:{usertunnel_info['iparea']}",app_icon = f"{pathx}\\system_info.ico",timeout = 10)