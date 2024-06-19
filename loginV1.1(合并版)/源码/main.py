from requests import get
from re import findall
from json import load
from json import dump
from tkinter import messagebox
from tkinter import *


# 创建窗口  
window = Tk()  
window.title("login")  
window.geometry("210x120")  # 调整窗口大小  

try:
    with open("config.json",encoding='utf-8') as f:
        data=load(f)
        # 创建变量并设置默认值  
        student_id = StringVar(value=data.get("学号"))  
        password = StringVar(value=data.get("密码"))  
        carrier = StringVar(value=data.get("运营商"))
except:
    # 创建输入框  
    student_id = StringVar()  
    password = StringVar()  
    carrier = StringVar(value="校园网")

# 创建选项框  
carrier_options = ["校园网", "中国移动", "中国电信", "中国联通"]  
  
# 创建输入框标签和输入框  
Label(window, text="学号").grid(row=0, column=0)  
Entry(window, textvariable=student_id).grid(row=0, column=1)  
  
Label(window, text="密码").grid(row=1, column=0)  
Entry(window, textvariable=password).grid(row=1, column=1)  
  
Label(window, text="运营商").grid(row=2, column=0)  
OptionMenu(window, carrier, *carrier_options).grid(row=2, column=1)  

def saveinfo():  
    # 获取用户输入的信息  
    student_id_value = student_id.get()  
    password_value = password.get()  
    carrier_value = carrier.get()  
  
    # 检查所有字段是否都已填写  
    if not student_id_value or not password_value or not carrier_value:  
        messagebox.showinfo("提示", "所有字段都是必填项！")  
        return  
  
    # 将用户信息写入JSON文件  
    with open("config.json", "w+", encoding="utf-8") as file:
        dump({  
            "学号": student_id_value,  
            "密码": password_value,  
            "运营商": carrier_value  
        }, file)  
  

#获取ip
def getip(url):
    WebContent0=get(url).text
    ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'  
    ip_addresses = findall(ip_pattern,WebContent0)
    return ip_addresses[1]

#登录
def login():
    saveinfo()
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
    # try:  
    response = get('http://10.9.1.3:801/eportal/',  params=params)  
    print(response)
    text=response.text  
    print(text)
    # except:  
    #     messagebox.showerror("运行结果", "请求错误，请检查网络连接")
        # return
    str1='"ret_code":2'  
    str2='"ret_code":1'  
    if(str1 in text):  
        messagebox.showinfo("运行结果", "已登录,无需重复登录")
    elif(str2 in text):  
        messagebox.showerror("运行结果", "登录失败，请检查账号密码运营商是否正确")
    else:  
        messagebox.showinfo("运行结果", "登陆成功")
    return


confirm_button = Button(window, text="连接", command=login)  
confirm_button.grid(row=3, column=1)  

  
# 运行窗口循环，等待用户操作  
window.mainloop()
  






