import tkinter as tk
from tkinter import messagebox

import matplotlib.pyplot as plt
import ttkbootstrap as ttk
from ttkbootstrap.widgets import Combobox

from AccountManager import accountManager
from GradeManager import gradeManager

"""
2024/7/10
    Teacher_Window
    教师的界面
by 廖雨龙

2024/7/12
   修改密码中的确认按钮
   提交申请的确认函数
by 刘链凯
"""
"""
2024/7/12
    Teacher_Window
    优化了教师界面
by 刘杨健
"""
"""
2024/7/13
    Teacher_Window
    完成相关按钮的布局,优化界面
by 廖雨龙
"""
"""
2024/7/14
    Teacher_Window
    实现总成绩显示的前后端对接
    继续细分查看总体成绩分析功能
    使用TinUI来美化界面
by 廖雨龙
"""
"""
2024/7/15
    app_review()
    完善了提交了申请表的功能
by刘杨健
"""


# 根据学号获取成绩
def get_grades(stuID):
    if stuID == "":
        return False
    stuName, gradeList = accountManager.getGrades(1, int(stuID))
    subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治',
                '\n地理：']
    grades = {}
    if gradeList:
        for i in range(9):
            if gradeList[i] != -1:
                grades.update({subjects[i]: gradeList[i]})
            if not grades:
                raise ValueError(f"No valid grades found for userid {stuID}")
        return grades
    else:
        return False
    # 获取特定用户的分数


# 点击之后实现排序的函数,在显示总成绩界面,点击之后就会按照单科进行排序
# 传入点击的标题的名称
def click_sort(sub, tree):
    # 这个函数传两个参数 mod1=0 总分 1 语文 mod2=0 降序
    # 维护一个字典,使得每个科目的名称有对应的mod1
    subject_mapping = {
        '总分': 0,
        '语文': 1,
        '数学': 2,
        '外语': 3,
        '物理': 4,
        '化学': 5,
        '生物': 6,
        '历史': 7,
        '地理': 8,
        '政治': 9
    }
    mod1 = subject_mapping.get(sub, -1)
    if mod1 != -1:
        # 拿到新的排序方式得到的成绩
        data1 = accountManager.getAllGrades(mod1, 0)
        update_treeview(data1, tree)


# 加一个函数用于更新treeview
def update_treeview(data2, tree):
    # 清空Treeview
    for item2 in tree.get_children():
        tree.delete(item2)
    # 重新插入数据
    for item2 in data2:
        values2 = []
        for key2 in ['姓名', '学号', '语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理',
                     '总分']:
            if item2[key2] == -1:
                values2.append('/')
            else:
                values2.append(item2[key2])
        tree.insert('', tk.END, values=tuple(values2))


def generate_histogram(scores):
    # 使用matplotlib生成直方图
    plt.hist(scores, bins=10, color='blue', edgecolor='black')
    plt.title('Scores Histogram')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()


# 设置窗口居中
def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')


# 显示成绩分布直方图的函数
def disp_graph(choice2):
    choice2.withdraw()
    graph_window = tk.Toplevel()
    graph_window.title("直方图分析")
    graph_window.geometry("1600x900")  # 设置窗口大小
    center_window(graph_window, 400, 300)  # 将窗口居中
    graph_window.configure(bg="lightblue")  # 设置背景颜色

    label = ttk.Label(graph_window, text="选择学科进行直方图分析：", background="lightblue")
    label.pack(pady=10)

    subjects = ['Chinese', 'Math', 'English', 'Physics', 'Chemistry', 'Biology', 'History', 'Politics', 'Geography']
    subject_var = tk.StringVar(graph_window)
    subject_var.set(subjects[0])

    subject_menu = ttk.OptionMenu(graph_window, subject_var, *subjects)
    subject_menu.pack(pady=10)

    def analyze_subject():
        selected_subject = subject_var.get()
        gradeManager.generateGradesAnalysis(1, selected_subject)

    analyze_button = ttk.Button(graph_window, text="分析", command=analyze_subject)
    analyze_button.pack(pady=10)

    def on_close():
        graph_window.destroy()
        choice2.deiconify()

    graph_window.protocol("WM_DELETE_WINDOW", on_close)


# 显示主副科关系曲线的函数
def disp_relation(choice2):
    choice2.withdraw()
    rel_window = tk.Toplevel()
    rel_window.title("折线图分析")
    rel_window.geometry("400x300")  # 设置窗口大小
    center_window(rel_window, 400, 300)  # 将窗口居中
    rel_window.configure(bg="lightblue")  # 设置背景颜色

    label = ttk.Label(rel_window, text="选择分析方式：", background="lightgreen")
    label.pack(pady=10)

    analysis_methods = ['物化生', '史政地']
    method_var = tk.StringVar(rel_window)
    method_var.set(analysis_methods[0])

    method_menu = ttk.OptionMenu(rel_window, method_var, *analysis_methods)
    method_menu.pack(pady=10)

    def analyze_method():
        selected_method = method_var.get()
        if selected_method == '物化生':
            way = 1
        elif selected_method == '史政地':
            way = 2
        gradeManager.generateGradesAnalysis(2, way)

    analyze_button = ttk.Button(rel_window, text="分析", command=analyze_method)
    analyze_button.pack(pady=10)

    def on_close():
        rel_window.destroy()
        choice2.deiconify()

    rel_window.protocol("WM_DELETE_WINDOW", on_close)


# 提交申请的确认函数
def confirm_app(stuid, sub, current_window, pre_window):
    if not sub:  # 当科目为空时，说明用户没有选择或者学号输入有误，提示错误
        messagebox.showerror('错误', '请输入正确的学号并选择科目')
    else:
        accountManager.addCheckApplication(accountManager.users[int(stuid)].userName, int(stuid), sub)
        messagebox.showinfo('提示', '申请已提交')
        current_window.destroy()
        pre_window.deiconify()
        # 补充将申请存到数据库中的功能


def confirm_password(old, new1, new2, password_window, tea_window, user_id):
    if accountManager.changePassword(old, new1, new2, user_id):
        messagebox.showinfo('提示', '密码修改成功')
        password_window.destroy()
        tea_window.deiconify()
    return


# 实现返回上一步的操作/也可以当作取消按钮来用
# 参数: 现在的窗口 之前的窗口
def last_step(current_window, previous_window):
    previous_window.deiconify()
    current_window.destroy()


# 实现查看成绩功能1 查看所有学生成绩 未实现
# 预期目标,可以打印出来各科成绩,做成一个可以往下拉的东西
# 还要在左上角做一个返回键
def disp_all_grades(grade_window):
    grade_window.withdraw()
    choice1 = ttk.Toplevel(grade_window)
    choice1.title("成绩表")
    choice1.attributes('-fullscreen', True)
    # 创建一个Frame来包含Treeview和滚动条
    frame = ttk.Frame(choice1)
    frame.pack(fill="both", expand=True)
    # 创建一个修改显示模式的函数,绑定在下拉框的切换上面
    # 添加选择下拉菜单  # 还没有绑定相关的事件
    category_var = tk.StringVar()
    category_dropdown = ttk.Combobox(choice1, textvariable=category_var, state="readonly")
    category_dropdown['values'] = ("物理类", "历史类")
    category_dropdown.pack(pady=10, side=tk.LEFT, anchor='nw')
    # 添加一个搜索框
    search_var = tk.StringVar()
    search_entry = ttk.Entry(choice1, textvariable=search_var)
    search_entry.pack(pady=10, side=tk.LEFT, anchor='nw')
    # 创建Treeview
    columns = (
        "姓名", "学号", "语文", "数学", "外语", "物理", "化学", "生物", "历史",
        "地理", "政治", "总分")
    tree = ttk.Treeview(frame, columns=columns, show='headings')

    # 定义每一列的标题和宽度
    for col in columns:
        tree.heading(col, text=col, command=lambda sub=col: click_sort(sub, tree))
        tree.column(col, width=100, anchor='center')

    # 总分降序
    data = accountManager.getAllGrades(0, 0)

    def insert_data(i_data):
        # 将得到的数据放到那个表里面去
        for item in i_data:
            # 将 -1 转换为斜杠
            values = []
            for key in ['姓名', '学号', '语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理', '总分']:
                if item[key] == -1:
                    values.append('/')
                else:
                    values.append(item[key])
            tree.insert('', tk.END, values=tuple(values))

    insert_data(data)  # 插入初始数据
    # 创建垂直和水平滚动条
    scrollbar_y = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar_x = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)

    # 配置Treeview的滚动条
    tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

    # 添加Treeview和滚动条到Frame中
    tree.grid(row=0, column=0, sticky="nsew")
    scrollbar_y.grid(row=0, column=1, sticky="ns")
    scrollbar_x.grid(row=1, column=0, sticky="ew")

    # 确保Treeview填充Frame
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # 再做一个确认并返回的按钮
    con_button = ttk.Button(choice1, text='确认', command=lambda: last_step(choice1, grade_window), width=10,
                            bootstyle=bootstyle)
    con_button.pack(pady=10)

    # 完成搜索框的搜索功能
    def search_tree():
        search_term = search_entry.get()
        for child in tree.get_children():
            s_values = tree.item(child, 'values')
            # 只在姓名和学号里面搜索
            if search_term.lower() in s_values[0].lower() or search_term.lower() in s_values[1].lower():
                tree.see(child)
                tree.selection_set(child)
            else:
                tree.selection_remove(child)

    search_var.trace("w", lambda name, index, mode: search_tree())

    # 添加一个选择类别的东西
    def filter_data(event):
        # 拿到选择的类别
        selected_category = category_var.get()
        if selected_category == "物理类":
            filtered_data = [item for item in data if item["物理"] != -1]
        elif selected_category == "历史类":
            filtered_data = [item for item in data if item["历史"] != -1]
        else:
            filtered_data = data
        # 清空TreeView中的数据并插入新的数据
        for child in tree.get_children():
            tree.delete(child)
        # 插入过滤后的数据
        insert_data(filtered_data)

    # 为下拉框绑定相关的函数
    category_dropdown.bind("<<ComboboxSelected>>", filter_data)
    choice1.mainloop()


# 实现查看成绩功能2 显示总体成绩的分析 未实现
# 总体成绩分析界面 还不知道里面十是否要细分出其他小的选项
def disp_all_analysis(grade_window):
    # 隐藏grade_window窗口
    grade_window.withdraw()
    # 创建一个新的窗口 标题 大小 标签
    choice2 = ttk.Toplevel(grade_window)
    choice2.title("成绩分析")
    choice2.geometry("800x1000+800+400")
    l2 = ttk.Label(choice2, text='成绩分析功能', font=("楷体", 25))
    l2.pack(pady=20)
    choice2.focus_force()
    # 显示成绩分布直方图
    disp_all_grades_button = ttk.Button(choice2, text='显示成绩分布直方图', command=lambda: disp_graph(choice2),
                                        width=20, bootstyle=bootstyle, padding=padding)
    disp_all_grades_button.pack(pady=pady)
    # 主副科成绩关系曲线
    disp_all_analysis_button = ttk.Button(choice2, text='查看主副科关系曲线', command=lambda: disp_relation(choice2),
                                          width=20, bootstyle=bootstyle, padding=padding)
    disp_all_analysis_button.pack(pady=pady)

    # 返回上一步
    last_step_button = ttk.Button(choice2, text='返回', command=lambda: last_step(choice2, grade_window), width=20,
                                  bootstyle=bootstyle, padding=padding)
    last_step_button.pack(pady=pady)
    choice2.mainloop()


# 实现查看成绩功能3 查看单个学生的成绩 未实现
# 还要加一个确认和取消的按钮
# stuID: 存放学生的ID,用于查找这个学生,得到它的成绩
def disp_single_grade(grade_window):
    # 成绩查询中的确认按钮
    # 点击之后会出现一个新的界面,显示是否找到和查找结果
    # 参数 stuID:学生的学号
    def confirm_grade(stuID, grade_window):
        nonlocal grades_var, warning_var
        stuName, gradeList = accountManager.getGrades(1, int(stuID))
        if stuName is False:
            warning_var.set("学号不存在！")
            return
        subjects = [' \n\n语文：', '\n数学：', '\n英语：', ' \n物理：', '\n化学：', '\n生物：', ' \n历史：', '\n政治：',
                    '\n地理：']
        temp = stuName
        for i in range(9):
            if i == 3:
                temp += '\n'
            temp += (subjects[i] + str(gradeList[i])) if gradeList[i] != -1 else ''
        print(temp)
        grades_var.set(temp)
        warning_var.set('')
        seperator.pack(side="right", padx=30, pady=100, fill='y')

    grades_var = ttk.StringVar()
    stuID_var = ttk.StringVar()
    warning_var = ttk.StringVar()
    # 隐藏grade_window窗口
    grade_window.withdraw()
    # 创建新的窗口 标题 大小 标签
    choice3 = ttk.Toplevel(grade_window)
    choice3.title("查看单个学生成绩")
    choice3.geometry("800x600+800+400")
    choice3.resizable(False, False)
    stuID_label = ttk.Label(choice3, text="请输入学号:", font=('黑体', 16))
    stuID_label.place(x=100, y=100)
    # 输入框
    stuID_entry = ttk.Entry(choice3, show="", font=('楷体', 16), textvariable=stuID_var)
    stuID_entry.place(x=100, y=220)
    # stuID里面放输入的内容
    # stuID = stuID_entry.get()
    # 取消按钮
    cancel_button = ttk.Button(choice3, text="取消", command=lambda: last_step(choice3, grade_window), width=5,
                               bootstyle='darkly')
    cancel_button.place(x=100, y=400)
    # 确认按钮
    confirm_button = ttk.Button(choice3, text="确定", command=lambda: confirm_grade(stuID_var.get(), choice3),
                                width=5,
                                bootstyle=bootstyle)
    confirm_button.place(x=360, y=400)
    warning_label = ttk.Label(choice3, textvariable=warning_var, font=('黑体', 12), style='danger')
    warning_label.place(x=100, y=280)
    # myStr.set(('     '))
    grades_label = ttk.Label(choice3, textvariable=grades_var, font=('黑体', 16))
    grades_label.pack(padx=20, pady=100, side='right')
    seperator = ttk.Separator(choice3, orient=tk.VERTICAL)

    choice3.mainloop()


# 有一个新的界面,里面提供其他的成绩查询选项 未完成
# 成绩展示的内置其他选项
# 1. 查看所有学生成绩
# 2. 所有学生成绩分析
# 添加功能,在下面加搜索框和历史类物理类的切换
def disp_grades(tea_window, name):  # 这里存在一个问题,就是老师选择查看成绩后,原来的窗口无法隐藏 已解决
    grade_window = ttk.Toplevel(tea_window)
    grade_window.title("查看成绩")
    grade_window.geometry('800x1000+800+400')
    grade_window.resizable(False, False)
    tea_window.withdraw()

    blank_title = ttk.Label(grade_window, text='', font=('黑体', 15))
    blank_title.pack(pady=20)
    disp_all_grades_button = ttk.Button(grade_window, text='显示所有学生成绩',
                                        command=lambda: disp_all_grades(grade_window), width=20, bootstyle=bootstyle,
                                        padding=padding)
    disp_all_grades_button.pack(pady=pady)
    disp_all_analysis_button = ttk.Button(grade_window, text='总体成绩分析',
                                          command=lambda: disp_all_analysis(grade_window), width=20,
                                          bootstyle=bootstyle, padding=padding)
    disp_all_analysis_button.pack(pady=pady)
    disp_single_grade_button = ttk.Button(grade_window, text='查看个人成绩',
                                          command=lambda: disp_single_grade(grade_window), width=20,
                                          bootstyle=bootstyle, padding=padding)
    disp_single_grade_button.pack(pady=pady)
    # disp_single_analysis_button = tk.Button(grade_window, text='查看个人成绩分析',
    #                                         command=lambda: disp_single_analysis(grade_window),
    #                                         font=('楷体', 18), width=20, height=1)
    # disp_single_analysis_button.place(x=180, y=220)
    last_step_button = ttk.Button(grade_window, text='返回', command=lambda: last_step(grade_window, tea_window),
                                  width=20, bootstyle=bootstyle, padding=padding)
    last_step_button.pack(pady=pady)
    grade_window.mainloop()


# 申请成绩复核函数,发送请求给admin
# 填 账户老师用户名 学生姓名 学生学号 申请科目 四个信息
def app_review(tea_window):
    # 新建一个窗口
    tea_window.withdraw()
    app_window = tk.Toplevel(tea_window)
    app_window.title("成绩复核申请")
    app_window.geometry("800x600+800+400")
    app_window.resizable(False, False)
    # 提示标签
    stuID_label = ttk.Label(app_window, text="学生学号:", font=('黑体', 14))
    stuID_label.place(x=100, y=100)
    sub_label = ttk.Label(app_window, text="申请科目:", font=('黑体', 14))
    sub_label.place(x=100, y=220)

    def on_text_change(*args):
        # 获取文本框中的内容
        content = stuID_var.get()

    stuID_var = ttk.StringVar()
    # 绑定文本变化事件
    stuID_var.trace_add("write", on_text_change)
    # 学号文本框
    stuID_entry = ttk.Entry(app_window, show="", font=('黑体', 16), textvariable=stuID_var)
    stuID_entry.place(x=270, y=100)
    # 申请科目下拉框
    sub_combobox = Combobox(app_window, values=[], state="readonly")
    sub_combobox.place(x=270, y=220)

    # 绑定下拉框事件
    def update_combobox(event):
        student_id = stuID_entry.get()
        options = []
        try:
            stu_grades = get_grades(student_id)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            app_window.destroy()
            tea_window.deiconify()
            return
        if stu_grades:
            for subject, score in stu_grades.items():
                options.append(subject)
        else:
            sub_combobox.set("")
        sub_combobox['values'] = options
        if options:
            sub_combobox.set("")  # 设置默认为空

    stuID_entry.bind("<KeyRelease>", update_combobox)

    # 获取选中的科目
    def on_select(event):
        selected_sub = sub_combobox.get()

    sub_combobox.bind("<<ComboboxSelected>>", on_select)
    # 点击确认按钮，要给出提示
    # 全都输入完毕之后,点击确认或者取消
    confirm_button = ttk.Button(app_window, text="确认",
                                command=lambda: confirm_app(stuID_entry.get(), sub_combobox.get(), app_window,
                                                            tea_window), width=5, bootstyle=bootstyle)
    confirm_button.place(x=490, y=450)
    cancel_button = ttk.Button(app_window, text="取消", command=lambda: last_step(app_window, tea_window), width=5,
                               bootstyle='darkly')
    cancel_button.place(x=160, y=450)
    app_window.mainloop()


# 修改自己密码的函数  (复用沈智恺的函数) # 未完成,缺少输入完之后的确认按钮
"""
1、没有输入
    提示‘请输入密码’
2、没有新的密码
    提示‘请输入新的密码’
3、只有新的密码没有原来的密码
    提示‘请输入原来的密码’
4、有新的密码和原来的密码
    提示‘请确认新的密码’
"""


def change_my_password(tea_window, password, user_id):
    var_old = tk.StringVar()
    var_new1 = tk.StringVar()
    var_new2 = tk.StringVar()
    tea_window.withdraw()
    page4 = tk.Toplevel(tea_window)
    page4.title('修改密码')
    page4.geometry("800x600+800+400")
    # 修改密码标题
    change_password_title = tk.Label(page4, text='修改密码', font=('楷体', 30, 'bold'), width=20, height=2)
    change_password_title.pack(side='top')
    # 原密码提示标签和文本框
    ttk.Label(page4, text='原密码:', font=('黑体', 15)).place(x=158, y=145)
    ttk.Label(page4, text='新的密码:', font=('黑体', 15)).place(x=120, y=240)
    ttk.Label(page4, text='确认密码:', font=('黑体', 15)).place(x=120, y=335)
    ori_pas_entry = ttk.Entry(page4, textvariable=var_old, show='*', width=30)  # , width=50
    ori_pas_entry.place(x=290, y=150)
    new_pas_entry = ttk.Entry(page4, textvariable=var_new1, show='*', width=30)  # , width=44
    new_pas_entry.place(x=290, y=245)
    con_pas_entry = ttk.Entry(page4, textvariable=var_new2, show='*', width=30)  # , width=47
    con_pas_entry.place(x=290, y=340)
    page4.focus_force()

    # original = ori_pas_entry.get()
    # new = new_pas_entry.get()
    # confirm = con_pas_entry.get()
    # 标志密码是否修改成功
    password_flag = False
    user_id = user_id.get()
    confirm_button = ttk.Button(page4, text="确认",
                                command=lambda: confirm_password(ori_pas_entry.get(), new_pas_entry.get(),
                                                                 con_pas_entry.get(), page4, tea_window, int(user_id)),
                                width=5,
                                bootstyle=bootstyle)
    confirm_button.place(x=490, y=450)
    if password_flag:
        print(new_pas_entry.get())
    cancel_button = ttk.Button(page4, text="取消", command=lambda: last_step(page4, tea_window),
                               width=5, bootstyle='darkly')
    cancel_button.place(x=160, y=450)
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
# 使用TinUI
def show_teacher_window(login_window, userid_entry, password_entry, name):
    tea_window = ttk.Toplevel(login_window)
    tea_window.title("Teacher Window")
    tea_window.geometry('800x1000+800+400')
    tea_window.resizable(False, False)
    # 欢迎标题
    welcome_title = ttk.Label(tea_window, text='你好!' + name, font=('楷体', 10))
    welcome_title.place(x=0, y=0)

    blank_title = ttk.Label(tea_window, text='', font=('黑体', 10))
    blank_title.pack(pady=20)
    # 查看成绩->一个新的页面 包括各种成绩与分析
    query_button = ttk.Button(tea_window, text="查询成绩", command=lambda: disp_grades(tea_window, name),
                              width=20, bootstyle=bootstyle, padding=padding)
    query_button.pack(pady=pady)
    # 申请复核成绩按钮
    app_review_button = ttk.Button(tea_window, text="申请复核成绩", command=lambda: app_review(tea_window),
                                   width=20, bootstyle=bootstyle, padding=padding)
    app_review_button.pack(pady=pady)
    # 修改自己的密码
    user_id = userid_entry.get()
    cha_my_button = ttk.Button(tea_window, text="修改我的密码",
                               command=lambda: change_my_password(tea_window, password_entry.get(), int(user_id)),
                               width=20, bootstyle=bootstyle, padding=padding)
    cha_my_button.pack(pady=pady)
    # 修改学生的密码
    # cha_stu_button = tk.Button(tea_window, text="修改学生密码", command=change_stu_password, width=30, height=3)
    # cha_stu_button.pack(pady=10)
    # 退出登录
    exit_button = ttk.Button(tea_window, text="退出登录",
                             command=lambda: log_out(tea_window, login_window, userid_entry
                                                     , password_entry), width=20, bootstyle=bootstyle, padding=padding)
    exit_button.pack(pady=pady)


padding = 15
pady = 20
bootstyle = 'info-outline'
