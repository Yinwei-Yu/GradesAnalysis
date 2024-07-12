import tkinter as tk

from AccountManager import accountManager
from Administrator_Window import show_admin_window
from Student_Window import show_student_window
from Teacher_Window import show_teacher_window

"""
2024/7/9
    Login_Window
by 刘杨健
"""

"""
2024/7/11
    Login_Window调整登录界面
    补充登录检测机制
by 刘杨健
"""

# 主窗口设置

login_window = tk.Tk()
login_window.title('main window')
login_window.geometry('600x400')
login_window.resizable(False, False)

# 显示标题，高考成绩管理系统
first_title = tk.Label(login_window, text='高考成绩管理系统', font=('华文行楷', 30, 'bold'), width=20, height=2)
first_title.pack(side='top')

# 用和密码的提示标签
userid_label = tk.Label(login_window, text='学号/工号:', font=('楷体', 15))
userid_label.place(x=120, y=170)
password_label = tk.Label(login_window, text='密码:', font=('楷体', 15))
password_label.place(x=170, y=210)

# 设置两个var获取输入的学号和密码
var_userid = tk.StringVar()
var_password = tk.StringVar()

# 学号和密码的输入框
userid_entry = tk.Entry(login_window, font=('楷体', 14), textvariable=var_userid)
userid_entry.place(x=230, y=170)

password_entry = tk.Entry(login_window, show='*', font=('楷体', 14), textvariable=var_password)
password_entry.place(x=230, y=210)

# 学号/工号和密码
userid = ""
password = ""

# 登录提示标签
login_var = tk.StringVar()
login_label = tk.Label(login_window, textvariable=login_var, font=('楷体', 14))
login_label.place(x=250, y=250)
login_label.pack(fill='x', padx=50, pady=20)

# 身份信号，初始为0，学生登录为3，教师登录为2，管理员登录为1
identity = 0

# 标记用户是否存在
is_exist = False


# 查询函数，应访问数据库，返回查询结果,密码错误，identity=0，否则返回相应的identity值

def find_user(userid, password):
    is_exist, identity = accountManager.login(int(userid), password)
    return is_exist, identity


# 记录密码错误次数
fault_times = 0

"""
登录函数会检测学号和密码的输入是否为空，当二者均不为空时，获取到的学号和密码分别存放于userid 和 password中
此时需要访问数据库查询对应账户，根据查询的结果进行页面跳转
1、学号不存在，提示用户不存在
2、学号存在，密码错误，提示用户重新输入密码，五次之后禁止再输入

查询函数返回identity信号，用于界面跳转
"""


def log_in():
    global identity, fault_times, userid, password
    if userid_entry.get() == "" and password_entry.get() == "":
        login_var.set('请输入学号/工号和密码')
    elif userid_entry.get() == "" and not password_entry.get() == "":
        login_var.set('请输入学号/工号')
    elif password_entry.get() == "":
        login_var.set('请输入密码')
    else:
        userid = userid_entry.get()
        password = password_entry.get()
        # 调用查找函数
        res_is_exist, res_identity = find_user(userid, password)
        if not res_is_exist:  # 用户不存在
            login_var.set('用户不存在！')
        else:
            if res_identity == 0:
                fault_times += 1
                if fault_times >= 5:
                    login_var.set('密码错误次数达到五次，禁止输入')
                    password_entry.config(state='disabled')
                else:
                    login_var.set(f'密码错误，你还可以输入{5 - fault_times}次')
            elif res_identity == 3:
                login_window.withdraw()
                show_student_window(login_window, userid_entry, password_entry)
            elif res_identity == 2:
                login_window.withdraw()
                show_teacher_window(login_window, userid_entry, password_entry)
            else:  # identity==1
                login_window.withdraw()
                show_admin_window(login_window, userid_entry, password_entry)
        # login_var.set('成功登录')

    # 测试代码
    # print(userid_entry.get(),password_entry.get())


# 退出函数
def log_out():
    login_window.destroy()


# 添加command参数补充按钮功能
# 注册、登录、退出按钮
bt_login = tk.Button(login_window, text='登录', font=('楷体', 12), width=15, height=1, command=log_in)
bt_login.place(x=150, y=300)
bt_logout = tk.Button(login_window, text='退出', font=('楷体', 12), width=15, height=1, command=log_out)
bt_logout.place(x=300, y=300)

login_window.mainloop()
