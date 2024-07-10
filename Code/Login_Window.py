"""
2024/7/9
    Login_Window
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

# 用户名和密码的提示标签
username_label = tk.Label(login_window, text='用户名:', font=('Arial', 10))
username_label.place(x=140, y=100)
password_label = tk.Label(login_window, text='密码:', font=('Arial', 10))
password_label.place(x=140, y=140)
# 用户名和密码的输入框
username_entry = tk.Entry(login_window, show=None, font=('Arial', 14))
username_entry.place(x=190, y=100)

password_entry = tk.Entry(login_window, show='*', font=('Arial', 14))
password_entry.place(x=190, y=140)

# 显示身份的标签（测试）
identity_var = tk.StringVar()
identity_disp = tk.Label(login_window, textvariable=identity_var)
identity_disp.place(x=190, y=260)


# 选项触发函数
def identity_selection():
    identity_var.set(identity_var.get())

# 身份选择Radiobutton
identity_label = tk.Label(login_window, text='身份:', font=('Arial', 10))
identity_label.place(x=140, y=180)
identity_var.set("未选择身份")
radiobt_student = tk.Radiobutton(login_window, text='学生', variable=identity_var, value='学生',
                                 command=identity_selection)
radiobt_teacher = tk.Radiobutton(login_window, text='老师', variable=identity_var, value='老师',
                                 command=identity_selection)
radiobt_administrator = tk.Radiobutton(login_window, text='管理员', variable=identity_var, value='管理员',
                                       command=identity_selection)
radiobt_student.place(x=190, y=180)
radiobt_teacher.place(x=190, y=205)
radiobt_administrator.place(x=190, y=230)

# 接受log_in函数传出的内容显示在标签上
login_var = tk.StringVar()
login_label = tk.Label(login_window, textvariable=login_var)
login_label.place(x=240, y=280)

# 按钮+函数，传出的内容显示在标签上，内容通过var传递

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
    elif identity_var.get()=="未选择身份":
        login_var.set('请选择身份')
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
bt_register=tk.Button(login_window,text='注册',font=('Arial',12),width=10,height=1,command=m_register)
bt_register.place(x=100,y=300)
bt_login = tk.Button(login_window, text='登录', font=('Arial', 12), width=10, height=1, command=log_in)
bt_login.place(x=250, y=300)
bt_logout = tk.Button(login_window, text='退出', font=('Arial', 12), width=10, height=1, command=log_out)
bt_logout.place(x=400, y=300)

login_window.mainloop()


