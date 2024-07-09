"""
2024/7/9
    Student_Window
    成功登录后跳转到学生界面
by 刘杨健
"""

import tkinter as tk
from Login_Window import login_hit,username_entry

# 如果登录窗口收到的信号为1，则关闭登录窗口，打开学生窗口
if login_hit==3:
    stu_window = tk.Tk()
    stu_window.title('学生窗口')
    stu_window.geometry('600x400')

    # 标题
    welcome_title=tk.Label(stu_window ,text='你好!', font=('Arial', 14), width=20, height=2)
    welcome_title.pack(side='top')

    #选项
    #1、查询成绩
    #2、修改用户名和密码

    stu_window.mainloop()

