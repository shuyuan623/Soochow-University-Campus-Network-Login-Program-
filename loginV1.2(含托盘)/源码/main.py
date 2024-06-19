from threading import Thread
from tkinter import Label,Entry,StringVar,OptionMenu,messagebox,Tk,Button
from pystray import MenuItem,Menu,Icon
from PIL import Image
from requests import get
from re import findall
from json import load,dump
from psutil import Process,process_iter
from sys import exit


class GUI:
    def __init__(self):
        # 创建窗口  
        self.root = Tk()  
        self.root.title("login")  
        self.root.geometry("210x120")  # 调整窗口大小  

        # 当用户点击窗口右上角的关闭按钮时，Tkinter 将自动发送 WM_DELETE_self.root 关闭事件。通过对其进行处理并调用 self.hide_self.root() 方法，可以改为将窗口隐藏到系统托盘中。
        # 该方法用于将程序窗口隐藏到系统托盘中而非直接退出应用程序
        self.root.protocol('WM_DELETE_WINDOW', self.hide_window)
        # 添加菜单和图标
        self.create_systray_icon()
        # 绘制界面
        self.interface()


    def saveinfo(self):  
        # 获取用户输入的信息  
        self.student_it_value = self.student_it.get()  
        self.password_value = self.password.get()  
        self.carrier_value = self.carrier.get()  
    
        # 检查所有字段是否都已填写  
        if not self.student_it_value or not self.password_value or not self.carrier_value:  
            messagebox.showinfo("提示", "所有字段都是必填项！")  
            return  0
    
        # 将用户信息写入JSON文件  
        with open("config.json", "w+", encoding="utf-8") as file:
            dump({  
                "学号": self.student_it_value,  
                "密码": self.password_value,  
                "运营商": self.carrier_value  
            }, file)  


    #获取ip
    def getip(self,url):
        WebContent = get(url).text
        ip_pattern = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'  
        ip_addresses = findall(ip_pattern,WebContent)
        return ip_addresses[1]

    #登录
    def login(self):
        if(self.saveinfo()==0):
            return
        LoginInUrl = 'http://10.9.1.3'
        try:
            ip = self.getip(LoginInUrl)
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
        str1='"ret_code":1'  
        str2='"ret_code":2'  

        if(str1 in text):  
            messagebox.showinfo("运行结果", "登录失败，请检查账号密码运营商是否正确")
        elif(str2 in text):  
            messagebox.showerror("运行结果", "已登录,无需重复登录")
        else: 
            messagebox.showinfo("运行结果", "登录成功")
        return


    def interface(self):
        try:
            with open("config.json",encoding='utf-8') as f:
                data=load(f)
                # 创建变量并设置默认值  
                self.student_it = StringVar(value=data.get("学号"))  
                self.password = StringVar(value=data.get("密码"))  
                self.carrier = StringVar(value=data.get("运营商"))
        except:
            # 创建输入框  
            self.student_it = StringVar()  
            self.password = StringVar()  
            self.carrier = StringVar(value="校园网")

        # 创建选项框  
        self.carrier_options = ["校园网", "中国移动", "中国电信", "中国联通"]  
        
        # 创建输入框标签和输入框  
        Label(self.root, text="学号").grid(row=0, column=0)  
        Entry(self.root, textvariable=self.student_it).grid(row=0, column=1)  
        
        Label(self.root, text="密码").grid(row=1, column=0)  
        Entry(self.root, textvariable=self.password).grid(row=1, column=1)  
        
        Label(self.root, text="运营商").grid(row=2, column=0)  
        OptionMenu(self.root, self.carrier, *self.carrier_options).grid(row=2, column=1)  

        
        confirm_button = Button(self.root, text="登录", command=self.login)  
        confirm_button.grid(row=3, column=1)  

        pass

    def create_systray_icon(self):
        """
        使用 Pystray 创建系统托盘图标
        """
        menu = (
            MenuItem('显示', self.show_window, default=True),
            Menu.SEPARATOR,  # 在系统托盘菜单中添加分隔线
            MenuItem('登录', self.login),
            Menu.SEPARATOR,  # 在系统托盘菜单中添加分隔线
            MenuItem('退出', self.quit_window))
        image = Image.open("ico/aniya.ico")
        self.icon = Icon("icon", image, "login", menu)
        Thread(target=self.icon.run, daemon=True).start()

    # 关闭窗口时隐藏窗口，并将 Pystray 图标放到系统托盘中。
    def hide_window(self):
        self.root.withdraw()

    # 从系统托盘中恢复 Pystray 图标，并显示隐藏的窗口。
    def show_window(self):
        self.icon.visible = True
        self.root.deiconify()

    def quit_window(self):
        """
        退出程序
        """
        self.icon.stop()  # 停止 Pystray 的事件循环
        self.root.quit()  # 终止 Tkinter 的事件循环
        self.root.destroy()  # 销毁应用程序的主窗口和所有活动

#判断当前进程是否已存在
def is_already_running():
    # 获取当前进程
    current_process = Process()
    # 获取所有与当前进程名称相同的进程
    for process in process_iter(['pid', 'name']):
        if process.info['name'] == current_process.name() and process.pid != current_process.pid:
            return True
    return False
 


if __name__ == '__main__':
    if is_already_running():
        exit()
    else:
        a = GUI()
        a.root.mainloop()
