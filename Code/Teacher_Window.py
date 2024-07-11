"""
2024/7/10
    Teacher_Window
    教师的界面
by 廖雨龙
"""
import tkinter as tk


# 实现返回上一步的操作
def last_step(current_window, previous_window):
    previous_window.deiconify()
    current_window.destroy()


# 实现查看成绩功能1 查看所有学生成绩 未实现
def disp_all_grades(grade_window):
    grade_window.withdraw()
    choice1 = tk.Toplevel(grade_window)
    choice1.title("查看所有学生成绩")
    choice1.geometry("800x500")
    l1 = tk.Label(choice1, text='学生成绩', font=("Arial", 20))
    l1.pack()
    choice1.focus_force()

    choice1.mainloop()


# 实现查看成绩功能2 显示总体成绩的分析 未实现
def disp_all_analysis(grade_window):
    grade_window.withdraw()
    choice2 = tk.Toplevel(grade_window)
    choice2.title("查看总体成绩分析报告")
    choice2.geometry("800x500")
    l2 = tk.Label(choice2, text='总体成绩报告',font=("Arial",20))
    l2.pack()
    choice2.focus_force()

    choice2.mainloop()
    pass


# 实现查看成绩功能3 查看单个学生的成绩 未实现
# 还要加一个确认和取消的按钮
# stuID: 存放学生的ID,用于查找这个学生,得到它的成绩
def disp_single_grade(grade_window):
    grade_window.withdraw()
    choice3 = tk.Toplevel(grade_window)
    choice3.title("查看单个学生成绩")
    choice3.geometry("800x500")
    stuID_label = tk.Label(choice3,text="学号:",font=('Arial',10))
    stuID_label.place(x=140,y=100)
    stuID_entry = tk.Entry(choice3,show=None,font=('Arial',14))
    stuID_entry.place(x=190,y=100)
    stuID = stuID_entry.get()



# 实现查看成绩功能4 查看单个学生的成绩分析报告 未实现
def disp_single_analysis(grade_window):

    pass


# 有一个新的界面,里面提供其他的成绩查询选项 未完成
# 成绩展示的内置其他选项
# 1. 查看所有学生成绩
# 2. 所有学生成绩分析
# 3. 查找个人成绩
# 4. 个人成绩分析
def disp_grades(tea_window):  # 这里存在一个问题,就是老师选择查看成绩后,原来的窗口无法隐藏 已解决
    grade_window = tk.Toplevel(tea_window)
    grade_window.title("查看成绩")
    tea_window.withdraw()

    disp_all_grades_button = tk.Button(grade_window, text='显示所有学生成绩',
                                       command=lambda: disp_all_grades(grade_window), width=30,
                                       height=3)
    disp_all_grades_button.pack(pady=10)
    disp_all_analysis_button = tk.Button(grade_window, text='总体成绩分析',
                                         command=lambda: disp_all_analysis(grade_window), width=30,
                                         height=3)
    disp_all_analysis_button.pack(pady=10)
    disp_single_grade_button = tk.Button(grade_window, text='查看个人成绩',
                                         command=lambda: disp_single_grade(grade_window), width=30,
                                         height=3)
    disp_single_grade_button.pack(pady=10)
    disp_single_analysis_button = tk.Button(grade_window, text='查看个人成绩分析',
                                            command=lambda: disp_single_analysis(grade_window),
                                            width=30, height=3)
    disp_single_analysis_button.pack(pady=10)
    last_step_button = tk.Button(grade_window, text='返回上一步', command=lambda: last_step(grade_window, tea_window),
                                 width=30, height=3)
    last_step_button.pack(pady=10)
    grade_window.mainloop()


# 申请成绩复核函数,发送请求给admin
def app_review():

    pass


# 修改自己密码的函数  (复用沈智恺的函数) # 未完成,缺少输入完之后的确认按钮
def change_my_password(tea_window, var):
    tea_window.withdraw()
    page4 = tk.Toplevel(tea_window)
    page4.title('修改密码')
    page4.geometry("600x400")
    tk.Label(page4, text='修改密码', font=("Arial", 20)).pack()
    tk.Label(page4, text='原密码', font=("Arial", 14)).place(x=100, y=75)
    tk.Label(page4, text='修改后密码', font=("Arial", 14)).place(x=100, y=150)
    tk.Label(page4, text='确认密码', font=("Arial", 14)).place(x=100, y=225)
    tk.Entry(page4, textvariable=var, show='*', width=50).place(x=180, y=80)
    tk.Entry(page4, textvariable=var, show='*', width=44).place(x=220, y=155)
    tk.Entry(page4, textvariable=var, show='*', width=47).place(x=200, y=230)
    page4.focus_force()
    page4.mainloop()


# 修改学生的密码的函数  未实现
#
def change_stu_password():
    pass


# 退出函数 返回到主界面
def log_out(tea_window, login_window, username_entry, password_entry):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    tea_window.destroy()
    login_window.deiconify()
    pass


# 显示教师界面
def show_teacher_window(login_window, username_entry, password_entry):
    tea_window = tk.Toplevel(login_window)
    tea_window.title("Teacher Window")
    var = tk.StringVar()
    var = None
    # 标题
    welcome_title = tk.Label(tea_window, text='你好!', font=('Arial', 14), width=20, height=2)
    welcome_title.pack(side='top')
    # 查看成绩->一个新的页面 包括各种成绩与分析
    query_button = tk.Button(tea_window, text="查询成绩", command=lambda: disp_grades(tea_window),
                             width=30, height=3)
    query_button.pack(pady=10)
    # 申请复核成绩按钮
    app_review_button = tk.Button(tea_window, text="申请复核成绩", command=app_review, width=30, height=3)
    app_review_button.pack(pady=10)
    # 修改自己的密码
    cha_my_button = tk.Button(tea_window, text="修改我的密码", command=lambda: change_my_password(tea_window, var),
                              width=30, height=3)
    cha_my_button.pack(pady=10)
    # 修改学生的密码
    cha_stu_button = tk.Button(tea_window, text="修改学生密码", command=change_stu_password, width=30, height=3)
    cha_stu_button.pack(pady=10)
    # 退出登录
    exit_button = tk.Button(tea_window, text="退出登录",
                            command=lambda: log_out(tea_window, login_window, username_entry
                                                    , password_entry), width=30, height=3)
    exit_button.pack(pady=10)
