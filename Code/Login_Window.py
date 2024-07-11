"""
2024/7/9
    Login_Window
by 刘杨健
"""

"""
2024/7/11
    Login_Window调整登录界面
by 刘杨健
"""
import tkinter as tk
from Student_Window import show_student_window
from Teacher_Window import show_teacher_window
# 主窗口设置

login_window = tk.Tk()
login_window.title('main window')
login_window.geometry('600x400')

# 显示标题，高考成绩管理系统
first_title = tk.Label(login_window, text='高考成绩管理系统', font=('Arial', 20), width=20, height=2)
first_title.pack(side='top')

# 用和密码的提示标签
userid_label = tk.Label(login_window, text='学号/工号:', font=('Arial', 10))
userid_label.place(x=135, y=100)
password_label = tk.Label(login_window, text='密码:', font=('Arial', 10))
password_label.place(x=135, y=140)
# 设置两个var获取输入的学号和密码
var_userid=tk.StringVar()
var_password=tk.StringVar()

# 学号和密码的输入框
userid_entry = tk.Entry(login_window, show=None, font=('Arial', 14),textvariable=var_userid)
userid_entry.place(x=205, y=100)

password_entry = tk.Entry(login_window, show='*', font=('Arial', 14),textvariable=var_password)
password_entry.place(x=205, y=140)

# 登录信号，初始为0，学生登录为1，教师登录为2，管理员登录为3
login_hit = 0

def log_in():
    global login_hit
    if username_entry.get().strip()=="" and password_entry.get().strip()=="":
        login_var.set('请输入用户名和密码')
    elif username_entry.get().strip()=="":
        login_var.set('请输入用户名')
    elif password_entry.get().strip()=="":
        login_var.set('请输入密码')
    else:
        login_var.set('成功登录')
        login_window.withdraw()
        if identity_var.get()=='管理员':
            login_hit=1
        elif identity_var.get()=='老师':
            login_hit=2
            show_teacher_window(login_window,username_entry,password_entry)
        else:                   # 学生
            login_hit=3
            show_student_window(login_window,username_entry,password_entry)
    print(login_hit)

# 退出函数
def log_out():
    login_window.destroy()

#登录函数
def m_register():
    print('跳转到注册界面')

# 添加command参数补充按钮功能
# 注册、登录、退出按钮
bt_login = tk.Button(login_window, text='登录', font=('Arial', 12), width=15, height=1, command=log_in)
bt_login.place(x=150, y=300)
bt_logout = tk.Button(login_window, text='退出', font=('Arial', 12), width=15, height=1, command=log_out)
bt_logout.place(x=300, y=300)


login_window.mainloop()


