from requests import get
from re import findall
from json import load
from tkinter import messagebox


#获取ip
def getip(url):
    WebContent0=get(url).text
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'  
    ip_addresses = findall(ip_pattern,WebContent0)
    return ip_addresses[1]

#登录
def login():
    LoginInUrl = 'http://10.9.1.3'
    try:
        ip = getip(LoginInUrl)
    except:
        messagebox.showerror("运行结果", "网络异常，请检查网络连接")
        return

    try:
        with open("config.json",encoding='utf-8') as f:
            config=load(f)
    except IOError as err:
        messagebox.showerror("运行结果", "配置文件错误")
        return
    ISP={'校园网':'','中国移动':'@zgyd','中国电信':'@ctc','中国联通':'@cucc'}
    params = (
        ('c', 'Portal'),
        ('a', 'login'),
        ('login_method', '1'),
        ('user_account', config["学号"]+ISP[config["运营商"]]),
        ('user_password', config["密码"]),
        ('wlan_user_ip', ip)
        )
    try:  
        response = get('http://10.9.1.3:801/eportal/',  params=params)  
        text=response.text  
    except:  
        messagebox.showerror("运行结果", "请求错误，请检查网络连接")
        return
    str1='"ret_code":2'  
    str2='"ret_code":1'  
    if(str1 in text):  
        messagebox.showinfo("运行结果", "已登录,无需重复登录")
    elif(str2 in text):  
        messagebox.showerror("运行结果", "登录失败，请检查账密及运营商是否输入正确")
    else:  
        messagebox.showinfo("运行结果", "登陆成功")
    return

login()