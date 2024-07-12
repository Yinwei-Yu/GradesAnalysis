"""
2024/7/10
    Teacher_Window
    教师的界面
by 廖雨龙

2024/7/12
   修改密码中的确认按钮
by 刘链凯
"""
import tkinter as tk


# 提交申请的确认函数
def confirm_app(tea_name, stu_name, stuID, sub):
    pass


# 修改密码中的确认按钮  未完成
# 参数 old:原来的密码 new1:第一次输入的新密码 new2:第二次输入的新的密码
def confirm_password(old, new1, new2,password_window):
    password_window.withdraw()
    # 创建一个新的窗口，标题，大小
    confirm_window = tk.Toplevel(password_window)
    confirm_window.title("密码修改确认")
    confirm_window.geometry("400x200")

    # 检查密码修改状态并设置标签
    if new1 == new2 and new1 != old:
        message = "密码修改成功！"
    else:
        message = "密码修改失败，请检查输入！"

    l1 = tk.Label(confirm_window, text=message, font=("Arial", 16))
    l1.pack(pady=20)

    # 返回上一步的按钮
    last_step_button = tk.Button(confirm_window, text='返回上一步', command=lambda: last_step(confirm_window, password_window),
                                 width=15, height=1)
    last_step_button.pack(pady=10)

    confirm_window.focus_force()
    confirm_window.mainloop()


# 成绩查询中的确认按钮
# 点击之后会出现一个新的界面,显示是否找到和查找结果
# 参数 stuID:学生的学号
def confirm_grade(stuID,grade_window):
    pass


# 实现返回上一步的操作/也可以当作取消按钮来用
# 参数: 现在的窗口 之前的窗口
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
    last_step_button = tk.Button(choice1, text='返回上一步', command=lambda: last_step(choice1, grade_window),
                                 width=30, height=3)
    last_step_button.pack(padx=0, pady=0)
    choice1.mainloop()


# 实现查看成绩功能2 显示总体成绩的分析 未实现
def disp_all_analysis(grade_window):
    # 隐藏grade_window窗口
    grade_window.withdraw()
    # 创建一个新的窗口 标题 大小 标签
    choice2 = tk.Toplevel(grade_window)
    choice2.title("查看总体成绩分析报告")
    choice2.geometry("800x500")
    l2 = tk.Label(choice2, text='总体成绩报告', font=("Arial", 20))
    l2.pack()
    choice2.focus_force()
    # 返回上一步的按钮
    last_step_button = tk.Button(choice2, text='返回上一步', command=lambda: last_step(choice2, grade_window),
                                 width=30, height=3)
    last_step_button.pack(padx=0, pady=0)

    choice2.mainloop()


# 实现查看成绩功能3 查看单个学生的成绩 未实现
# 还要加一个确认和取消的按钮
# stuID: 存放学生的ID,用于查找这个学生,得到它的成绩
def disp_single_grade(grade_window):
    # 隐藏grade_window窗口
    grade_window.withdraw()
    # 创建新的窗口 标题 大小 标签
    choice3 = tk.Toplevel(grade_window)
    choice3.title("查看单个学生成绩")
    choice3.geometry("800x500")
    stuID_label = tk.Label(choice3, text="学号:", font=('Arial', 10))
    stuID_label.place(x=140, y=100)
    # 输入框
    stuID_entry = tk.Entry(choice3, show=None, font=('Arial', 14))
    stuID_entry.place(x=190, y=100)
    # stuID里面放输入的内容
    stuID = stuID_entry.get()
    # 取消按钮
    cancel_button = tk.Button(choice3, text="取消", command=lambda: last_step(choice3, grade_window), width=30,
                              height=3)
    cancel_button.pack(pady=10)
    # 确认按钮
    confirm_button = tk.Button(choice3, text="确定", command=lambda: confirm_grade(stuID), width=30, height=3)
    confirm_button.pack(pady=10)


# 实现查看成绩功能4 查看单个学生的成绩分析报告 未实现
def disp_single_analysis(grade_window):
    # 隐藏grade_window窗口
    grade_window.withdraw()
    # 创建新的窗口 标题 大小 标签
    choice4 = tk.Toplevel(grade_window)
    choice4.title("查看单个学生成绩报告")
    choice4.geometry("800x500")
    stuID_label = tk.Label(choice4, text="学号:", font=('Arial', 10))
    stuID_label.place(x=140, y=100)
    # 输入框
    stuID_entry = tk.Entry(choice4, show=None, font=('Arial', 14))
    stuID_entry.place(x=190, y=100)
    # stuID里面放输入的内容
    stuID = stuID_entry.get()
    # 取消按钮
    cancel_button = tk.Button(choice4, text="取消", command=lambda: last_step(choice4, grade_window), width=30,
                              height=3)
    cancel_button.pack(pady=10)
    # 确认按钮
    confirm_button = tk.Button(choice4, text="确定", command=lambda: confirm_grade(stuID), width=30, height=3)
    confirm_button.pack(pady=10)


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
# 填 账户老师用户名 学生姓名 学生学号 申请科目 四个信息
def app_review(tea_window):
    # 新建一个窗口
    tea_window.withdraw()
    app_window = tk.Toplevel(tea_window)
    app_window.title("成绩复核申请")
    app_window.geometry("800x500")
    # 提示标签
    tea_name_label = tk.Label(app_window, text="老师姓名:", font=('Arial', 10))
    tea_name_label.place(x=140, y=100)
    stu_name_label = tk.Label(app_window, text="学生姓名:", font=('Arial', 10))
    stu_name_label.place(x=140, y=140)
    stuID_label = tk.Label(app_window, text="学生学号:", font=('Arial', 10))
    stuID_label.place(x=140, y=180)
    sub_label = tk.Label(app_window, text="申请科目:", font=('Arial', 10))
    sub_label.place(x=140, y=220)
    # 文本输入
    tea_name_entry = tk.Entry(app_window, show=None, font=('Arial', 14))
    tea_name_entry.place(x=190, y=100)
    stu_name_entry = tk.Entry(app_window, show=None, font=('Arial', 14))
    stu_name_entry.place(x=190, y=140)
    stuID_entry = tk.Entry(app_window, show=None, font=('Arial', 14))
    stuID_entry.place(x=190, y=180)
    sub_entry = tk.Entry(app_window, show=None, font=('Arial', 14))
    sub_entry.place(x=190, y=220)
    # 将输入得到的东西放到变量里面去
    tea_name = tea_name_entry.get()
    stu_name = stu_name_entry.get()
    stuID = stuID_entry.get()
    sub = sub_entry.get()
    # 全都输入完毕之后,点击确认或者取消
    confirm_button = tk.Button(app_window, text="确认", command=lambda: confirm_app(tea_name, stu_name, stuID, sub),
                               width=30, height=3)
    confirm_button.pack()
    cancel_button = tk.Button(app_window, text="取消", command=lambda: last_step(app_window, tea_window), width=30,
                              height=3)
    cancel_button.pack()
    app_window.mainloop()


# 修改自己密码的函数  (复用沈智恺的函数) # 未完成,缺少输入完之后的确认按钮
def change_my_password(tea_window, var):
    tea_window.withdraw()
    page4 = tk.Toplevel(tea_window)
    page4.title('修改密码')
    page4.geometry("600x400")
    # 修改密码标题
    tk.Label(page4, text='修改密码', font=("华文行楷", 20)).pack()
    # 原密码提示标签和文本框
    tk.Label(page4, text='原密码', font=("Arial", 14)).place(x=100, y=75)
    tk.Label(page4, text='修改后密码', font=("Arial", 14)).place(x=100, y=150)
    tk.Label(page4, text='确认密码', font=("Arial", 14)).place(x=100, y=225)
    ori_pas_entry = tk.Entry(page4, textvariable=var, show='*', width=50)
    ori_pas_entry.place(x=180, y=80)
    new_pas_entry = tk.Entry(page4, textvariable=var, show='*', width=44)
    new_pas_entry.place(x=220, y=155)
    con_pas_entry = tk.Entry(page4, textvariable=var, show='*', width=47)
    con_pas_entry.place(x=200, y=230)
    page4.focus_force()
    original = ori_pas_entry.get()
    new = new_pas_entry.get()
    confirm = con_pas_entry.get()
    confirm_button = tk.Button(page4, text="确认", command=lambda: confirm_password(original, new, confirm),
                               width=30, height=3)
    confirm_button.pack()
    cancel_button = tk.Button(page4, text="取消", command=lambda: last_step(page4, tea_window), width=30, height=3)
    cancel_button.pack()
    page4.mainloop()


# 老师可能不需要这个功能
# 修改学生的密码的函数  未实现
#
# def change_stu_password():
#   pass


# 退出函数 返回到主界面
# 先清空输入的内容,再删除tea_window窗口,解除对login_window的隐藏
def log_out(tea_window, login_window, username_entry, password_entry):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    tea_window.destroy()
    login_window.deiconify()


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
    app_review_button = tk.Button(tea_window, text="申请复核成绩", command=lambda: app_review(tea_window), width=30,
                                  height=3)
    app_review_button.pack(pady=10)
    # 修改自己的密码
    cha_my_button = tk.Button(tea_window, text="修改我的密码", command=lambda: change_my_password(tea_window, var),
                              width=30, height=3)
    cha_my_button.pack(pady=10)
    # 修改学生的密码
    # cha_stu_button = tk.Button(tea_window, text="修改学生密码", command=change_stu_password, width=30, height=3)
    # cha_stu_button.pack(pady=10)
    # 退出登录
    exit_button = tk.Button(tea_window, text="退出登录",
                            command=lambda: log_out(tea_window, login_window, username_entry
                                                    , password_entry), width=30, height=3)
    exit_button.pack(pady=10)
