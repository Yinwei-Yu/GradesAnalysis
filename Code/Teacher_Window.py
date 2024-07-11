"""
2024/7/10
    Teacher_Window
    教师的界面
by 廖雨龙
"""
import tkinter as tk


# 实现查看成绩功能1 查看所有学生成绩 未实现
def disp_all_grades():
    pass


# 实现查看成绩功能2 显示总体成绩的分析 未实现
def disp_all_analysis():
    pass


# 实现查看成绩功能3 查看单个学生的成绩 未实现
def disp_single_grade():
    pass


# 实现查看成绩功能4 查看单个学生的成绩分析报告 未实现
def disp_single_analysis():
    pass


# 有一个新的界面,里面提供其他的成绩查询选项 未完成
# 成绩展示的内置其他选项
# 1. 查看所有学生成绩
# 2. 所有学生成绩分析
# 3. 查找个人成绩
# 4. 个人成绩分析
def disp_grades(tea_window):         # 这里存在一个问题,就是老师选择查看成绩后,原来的窗口无法隐藏
    tea_window.withdraw()
    grade_window = tk.Toplevel()
    grade_window.title("查看成绩")
    disp_all_grades_button = tk.Button(grade_window, text='显示所有学生成绩', command=disp_all_grades, width=30,
                                       height=3)
    disp_all_grades_button.pack(pady=10)
    disp_all_analysis_button = tk.Button(grade_window, text='总体成绩分析', command=disp_all_analysis, width=30,
                                         height=3)
    disp_all_analysis_button.pack(pady=10)
    disp_single_grade_button = tk.Button(grade_window, text='查看个人成绩', command=disp_single_grade, width=30,
                                         height=3)
    disp_single_grade_button.pack(pady=10)
    disp_single_analysis_button = tk.Button(grade_window, text='查看个人成绩分析', command=disp_single_analysis,
                                            width=30, height=3)
    disp_single_analysis_button.pack(pady=10)
    tea_window.deiconify()


# 申请成绩复核函数,发送请求给admin
def app_review():
    pass


# 修改自己密码的函数  未实现
def change_my_password():
    pass


# 修改学生的密码的函数  未实现
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
    global tea_window
    tea_window = tk.Toplevel(login_window)
    tea_window.title("Teacher Window")
    # 标题
    welcome_title = tk.Label(tea_window, text='你好!', font=('Arial', 14), width=20, height=2)
    welcome_title.pack(side='top')
    # 查看成绩->一个新的页面 包括各种成绩与分析
    query_button = tk.Button(tea_window, text="查询成绩", command=lambda: disp_grades(tea_window), width=30, height=3)
    query_button.pack(pady=10)
    # 申请复核成绩按钮
    app_review_button = tk.Button(tea_window, text="申请复核成绩", command=app_review, width=30, height=3)
    app_review_button.pack(pady=10)
    # 修改自己的密码
    cha_my_button = tk.Button(tea_window, text="修改我的密码", command=change_my_password, width=30, height=3)
    cha_my_button.pack(pady=10)
    # 修改学生的密码
    cha_stu_button = tk.Button(tea_window, text="修改学生密码", command=change_stu_password, width=30, height=3)
    cha_stu_button.pack(pady=10)
    # 退出登录
    exit_button = tk.Button(tea_window, text="退出登录",
                            command=lambda: log_out(tea_window, login_window, username_entry
                                                    , password_entry), width=30, height=3)
    exit_button.pack(pady=10)
