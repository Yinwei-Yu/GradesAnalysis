"""
2024/7/9
    Student_Window
    成功登录后跳转到学生界面
by 刘杨健
"""

"""
2024/7/10
    Student_Window
    修改了学生界面的窗口显示,在Login_Window里面调用里面的
    show_student_window,这样可以实现退出的时候返回到上一个界面
    同时在退出的时候会清空之前的输入
by 廖雨龙
"""
import tkinter as tk
from tkinter import messagebox

# 修改了一下
# 如果登录窗口收到的信号为1，则关闭登录窗口，打开学生窗口
# if login_hit == 3:
#    stu_window.title('学生窗口')
#    stu_window.geometry('600x400')

# 成绩查询的函数 未完成
def query_scores():
    # 这里要添加查询成绩的操作
    messagebox.showinfo("查询成绩", "这里是查询成绩的结果")

# 修改用户名和密码的函数 未完成
def modify_credentials():
    # 这里添加修改用户名和密码的操作
    messagebox.showinfo("修改用户名密码", "修改完成")

# 实现用户的登出 回到主窗口 同时会清空原来输入的账号和密码
def log_out(stu_window, login_window,username_entry,password_entry):
    username_entry.delete(0,tk.END)
    password_entry.delete(0,tk.END)
    stu_window.destroy()
    login_window.deiconify()

    # 选项
    # 1、查询成绩
    # 2、修改用户名和密码
    # 3. 退出登录


# 显示学生窗口的函数
def show_student_window(login_window,username_entry,password_entry):
    stu_window = tk.Toplevel()
    stu_window.title("Student Window")
    # 标题
    welcome_title = tk.Label(stu_window, text='你好!', font=('Arial', 14), width=20, height=2)
    welcome_title.pack(side='top')
    # 成绩查询按钮 query_button = tk.Button(stu_window, text="查询成绩", command=query_scores, width=30, height=3)
    query_button = tk.Button(stu_window, text="查询成绩", command=query_scores, width=30, height=3)
    query_button.pack(pady=10)
    # 修改用户名和密码的按钮
    modify_button = tk.Button(stu_window, text="修改用户名密码", command=modify_credentials, width=30, height=3)
    modify_button.pack(pady=10)
    # 退出登陆按钮
    exit_button = tk.Button(stu_window, text="退出登录", command=lambda: log_out(stu_window, login_window,username_entry
                                                                                 ,password_entry), width=30,height=3)
    exit_button.pack(pady=10)
