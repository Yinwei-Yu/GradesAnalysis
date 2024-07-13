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
"""
2024/7/13
    Student_Window
    根据Teacher_Window的做法,修改Student_Window
    by 廖雨龙
"""
import tkinter as tk
from tkinter import messagebox
# 复用Teacher_Window中修改密码的方法
from Teacher_Window import change_my_password
# 复用Teacher_Window中的确认键
from Teacher_Window import confirm_password
# 复用Teacher_Window中返回上一步的方法
from Teacher_Window import last_step


# 修改了一下
# 如果登录窗口收到的信号为1，则关闭登录窗口，打开学生窗口
# if login_hit == 3:
#    stu_window.title('学生窗口')
#    stu_window.geometry('600x400')


# 成绩查询的函数 未完成
# 参数 userid: 学生的学号
def query_scores(userid, stu_window):
    # 这里要添加查询成绩的操作 通过查询到的成绩,打印到这个新的界面上
    # 创建一个成绩显示窗口
    stu_window.withdraw()
    grade_window = tk.Toplevel(stu_window)
    grade_window.geometry('600x400')
    grade_window.title("Grades")
    grade_window.resizable(False, False)
    # 下面打印学生的成绩
    messagebox.showinfo("这里显示出学生的成绩")

    # 这里加一个确认键,返回上一步
    confirm_button = tk.Button(grade_window, text="确认", width=10, height=1,
                               command=lambda: last_step(grade_window, stu_window))
    confirm_button.place(x=180, y=40)


# 实现用户的登出 回到主窗口 同时会清空原来输入的账号和密码
def log_out(stu_window, login_window, username_entry, password_entry):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    stu_window.destroy()
    login_window.deiconify()

    # 选项
    # 1、查询成绩
    # 2、修改用户名和密码
    # 3. 退出登录


# 显示学生窗口的函数
def show_student_window(login_window, userid_entry, password_entry, name):
    stu_window = tk.Toplevel()
    stu_window.title("Student Window")
    stu_window.geometry('600x400')
    stu_window.resizable(False, False)
    # 标题
    welcome_title = tk.Label(stu_window, text='你好!' + name, font=('楷体', 10), width=10, height=2)
    welcome_title.place(x=0, y=0)
    # 成绩查询按钮 query_button = tk.Button(stu_window, text="查询成绩", command=query_scores, width=30, height=3)
    query_button = tk.Button(stu_window, text="查询成绩", command=lambda: query_scores(userid_entry.get(), stu_window),
                             width=20,
                             height=2, font=('楷体', 18))
    query_button.place(x=180, y=40)
    # 修改密码的按钮
    modify_button = tk.Button(stu_window, text="修改密码", command=lambda: change_my_password(stu_window), width=20,
                              height=2,
                              font=('楷体', 18))
    modify_button.place(x=180, y=120)
    # 退出登陆按钮
    exit_button = tk.Button(stu_window, text="退出登录",
                            command=lambda: log_out(stu_window, login_window, userid_entry
                                                    , password_entry), width=20, height=2, font=('楷体', 18))
    exit_button.place(x=180, y=200)
