"""
2024/7/9
    Login_Window
by 刘杨健
"""
import tkinter as tk

# 主窗口设置
Login_window = tk.Tk()
Login_window.title('main window')
Login_window.geometry('600x400')
# 显示标题，高考成绩管理系统
first_title = tk.Label(Login_window, text='高考成绩管理系统', font=('Arial', 20), width=20, height=2)
first_title.pack(side='top')

# 用户名和密码的提示标签
username_label = tk.Label(Login_window, text='用户名:', font=('Arial', 10))
username_label.place(x=140, y=100)
password_label = tk.Label(Login_window, text='密码:', font=('Arial', 10))
password_label.place(x=140, y=140)
# 用户名和密码的输入框
username_entry = tk.Entry(Login_window, show=None, font=('Arial', 14))
username_entry.place(x=190, y=100)

password_entry = tk.Entry(Login_window, show='*', font=('Arial', 14))
password_entry.place(x=190, y=140)

# 显示身份的标签（测试）
identity_var = tk.StringVar()
identity_disp = tk.Label(Login_window, textvariable=identity_var)
identity_disp.place(x=190, y=260)


# 选项触发函数
def identity_selection():
    identity_var.set(identity_var.get())


# 身份选择Radiobutton
identity_label = tk.Label(Login_window, text='身份:', font=('Arial', 10))
identity_label.place(x=140, y=180)
identity_var.set("未选择身份")
radiobt_student = tk.Radiobutton(Login_window, text='学生', variable=identity_var, value='学生',
                                 command=identity_selection)
radiobt_teacher = tk.Radiobutton(Login_window, text='老师', variable=identity_var, value='老师',
                                 command=identity_selection)
radiobt_administrator = tk.Radiobutton(Login_window, text='管理员', variable=identity_var, value='管理员',
                                       command=identity_selection)
radiobt_student.place(x=190, y=180)
radiobt_teacher.place(x=190, y=205)
radiobt_administrator.place(x=190, y=230)

# 接受log_in函数传出的内容显示在标签上
login_var = tk.StringVar()
login_label = tk.Label(Login_window, textvariable=login_var)
login_label.place(x=240, y=280)

# 按钮+函数，传出的内容显示在标签上，内容通过var传递

login_hit = False  # 登录函数

def log_in():
    global login_hit
    # login_hit == False and
    # if not username_entry.get().strip() == "" and not password_entry.get().strip() == "":
    #     # login_hit=True
    #     login_var.set('成功登录')
    # else:
    #     # login_hit=False
    #     login_var.set('请输入用户名和密码')
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
        login_hit=True

# 退出函数
def log_out():
    Login_window.destroy()

# 添加command参数补充按钮功能
bt_login = tk.Button(Login_window, text='登录', font=('Arial', 12), width=10, height=1, command=log_in)
bt_login.place(x=100, y=300)

bt_logout = tk.Button(Login_window, text='退出', font=('Arial', 12), width=10, height=1, command=log_out)
bt_logout.place(x=400, y=300)

Login_window.mainloop()
