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
"""
2024/7/15
   query_scores
   by 刘链凯
2024/7/17
    修改了query_scores
by陈邱华
"""

"""
2024/7/17
    修改了query_scores
    generate_grade_report()
    实现了成绩分析图
by刘杨健
"""

import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
import numpy as np
import ttkbootstrap as ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from AccountManager import accountManager
# 复用Teacher_Window中修改密码的方法
from Teacher_Window import change_my_password
from Teacher_Window import get_grades
# 复用Teacher_Window中的确认键
# 复用Teacher_Window中返回上一步的方法
from Teacher_Window import last_step


def generate_grade_report(userid, grade_window):
    # 这里写生成和显示成绩报告的代码
    grade_window.withdraw()
    # 创建一个成绩分析显示窗口
    analysis_window = ttk.Toplevel(grade_window)
    analysis_window.geometry('+800+200')
    analysis_window.title('Analysis')
    # analysis_window.resizable(False, False)

    # 创建数据
    stu_grades, _ = get_grades(userid)
    categories = []
    scores1 = []  # 我的成绩
    scores2 = [80, 85, 75, 90, 80, 92]  # 平均成绩
    for subject, score in stu_grades.items():
        categories.append(subject)
        scores1.append(score)
    # categories = ['语文', '数学', '英语', '物理', '化学', '生物']
    # scores1 = [85, 90, 70, 88, 75, 95]

    # 用来正常显示中文标签
    plt.rc('font', family='SimHei', size=13)

    # 绘制第一个六边形
    plt.figure(figsize=(6, 6))
    plt.subplot(111, polar=True)

    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    plt.plot(angles, scores1 + [scores1[0]], 'o-', linewidth=2, label='你的成绩')
    plt.fill(angles, scores1 + [scores1[0]], alpha=0.25)

    # 在第一个六边形的顶点处显示分数值
    for angle, score in zip(angles, scores1 + [scores1[0]]):
        plt.text(angle, score + 5, str(score), ha='center', va='center')

    # 绘制第二个六边形
    plt.plot(angles, scores2 + [scores2[0]], 'o-', linewidth=2, label='平均成绩')
    plt.fill(angles, scores2 + [scores2[0]], alpha=0.25)

    # 在第二个六边形的顶点处显示分数值
    for angle, score in zip(angles, scores2 + [scores2[0]]):
        plt.text(angle, score + 5, str(score), ha='center', va='center')

    plt.xticks(angles[:-1], categories)
    plt.yticks([])  # 隐藏极坐标的刻度
    plt.ylim(0, 150)

    plt.legend()
    # 在GUI窗口中展示图形
    canvas = FigureCanvasTkAgg(plt.gcf(), master=analysis_window)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    # 关闭按钮
    confirm_button = ttk.Button(analysis_window, text="确认", width=10,
                                command=lambda: last_step(analysis_window, grade_window), bootstyle=bootstyle)
    confirm_button.pack()


# 成绩查询的函数 未完成
# 参数 userid: 学生的学号
def query_scores(userid, stu_window):
    # 这里要添加查询成绩的操作 通过查询到的成绩,打印到这个新的界面上
    # 创建一个成绩显示窗口
    stu_window.withdraw()
    grade_window = ttk.Toplevel(stu_window)
    grade_window.geometry('600x600+800+400')
    grade_window.title("Grades")
    grade_window.resizable(False, False)

    # 下面打印学生的成绩
    # messagebox.showinfo("这里显示出学生的成绩")

    try:
        user_grades, total_grades = get_grades(userid)
    except ValueError as e:
        messagebox.showerror("获取成绩出现错误！", str(e))
        grade_window.destroy()
        stu_window.deiconify()
        return
    # 在窗口中显示成绩
    info_label = ttk.Label(grade_window,
                           text=f"姓名：{accountManager.users[int(userid)].userName}\n总分：{str(total_grades[0])}",
                           font=('黑体', 15))
    info_label.place(x=20, y=10)
    total_grades_label = ttk.Label(grade_window, text=f"学号：{userid}\n大类排名：{str(total_grades[1])}",
                                   font=('黑体', 15))
    total_grades_label.pack(anchor=tk.NE, pady=10, padx=20)
    grade_text = ''
    for subject, score in user_grades.items():
        grade_text += f"{subject}: {score}\n"
    label = ttk.Label(grade_window, text=grade_text, font=('黑体', 15))
    label.pack(pady=50)
    # 创建一个生成成绩分析报告的按钮
    report_button = ttk.Button(grade_window, text="查看成绩分析图", width=15,
                               command=lambda: generate_grade_report(userid, grade_window), bootstyle=bootstyle)
    report_button.pack(pady=0)  # 放置在确认按钮的正上方
    # 这里加一个确认键,返回上一步
    confirm_button = ttk.Button(grade_window, text="确认", width=15,
                                command=lambda: last_step(grade_window, stu_window), bootstyle=bootstyle)
    confirm_button.pack(pady=0)


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
    stu_window = ttk.Toplevel()
    stu_window.title('admin_window')
    stu_window.geometry('800x1000+800+400')

    stu_window.resizable(False, False)
    # 标题
    welcome_title = ttk.Label(stu_window, text='你好!' + name, font=('楷体', 15))
    welcome_title.place(x=0, y=0)

    blank_title = ttk.Label(stu_window, text='', font=('黑体', 10))
    blank_title.pack(pady=20)
    # 成绩查询按钮 query_button = tk.Button(stu_window, text="查询成绩", command=query_scores, width=30, height=3)
    query_button = ttk.Button(stu_window, text="查询成绩", command=lambda: query_scores(userid_entry.get(), stu_window),
                              width=20, bootstyle=bootstyle, padding=padding)
    query_button.pack(pady=pady)
    # 修改密码的按钮
    modify_button = ttk.Button(stu_window, text="修改密码",
                               command=lambda: change_my_password(stu_window, password_entry.get(), userid_entry),
                               width=20,
                               bootstyle=bootstyle,
                               padding=padding)
    modify_button.pack(pady=pady)
    # 退出登陆按钮
    exit_button = ttk.Button(stu_window, text="退出登录",
                             command=lambda: log_out(stu_window, login_window, userid_entry
                                                     , password_entry), width=20, bootstyle=bootstyle, padding=padding)
    exit_button.pack(pady=pady)


padding = 15
pady = 20
bootstyle = 'info-outline'
