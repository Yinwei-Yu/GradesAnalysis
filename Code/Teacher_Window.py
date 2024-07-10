"""
2024/7/10
    Teacher_Window
    教师的界面
by 廖雨龙
"""
import tkinter as tk
from tkinter import messagebox

# 有一个新的界面,里面提供其他的成绩查询选项 未完成
def disp_grades():
    pass

# 申请成绩复核函数,发送请求给admin
def app_review():
    pass
# 修改自己密码的函数  未实现
def change_my_password():
    pass

# 修改学生的密码的函数  未实现
def change_stu_password():
    pass

# 退出函数 返回到上一个界面
def log_out(tea_window,login_window,username_entry,password_entry):
    username_entry.delete(0,tk.END)
    password_entry.delete(0,tk.END)
    tea_window.destroy()
    login_window.deiconify()
    pass

# 显示教师界面
def show_teacher_window(login_window,username_entry,password_entry):
    tea_window = tk.Toplevel()
    tea_window.title("Teacher Window")
    # 标题
    welcome_title = tk.Label(tea_window, text='你好!', font=('Arial', 14), width=20, height=2)
    welcome_title.pack(side='top')
    # 查看成绩->一个新的页面 包括各种成绩与分析
    query_button = tk.Button(tea_window, text="查询成绩", command=disp_grades, width=30, height=3)
    query_button.pack(pady=10)
    # 申请复核成绩按钮
    modify_button = tk.Button(tea_window, text="修改用户名密码", command=app_review, width=30, height=3)
    modify_button.pack(pady=10)
    # 修改自己的密码
    cha_my_button = tk.Button(tea_window,text="修改我的密码",command=change_my_password,width=30,height=3)
    cha_my_button.pack(pady=10)
    # 修改学生的密码
    cha_stu_button = tk.Button(tea_window,text="修改学生密码",command=change_stu_password,width=30,height=3)
    cha_stu_button.pack(pady=10)
    # 退出登录
    exit_button = tk.Button(tea_window, text="退出登录", command=lambda: log_out(tea_window, login_window,username_entry
                                                                                 ,password_entry), width=30,height=3)
    exit_button.pack(pady=10)