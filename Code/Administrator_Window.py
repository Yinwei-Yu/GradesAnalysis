"""
2024/7/11
    管理员窗口
by 刘杨健
"""
from tkinter import filedialog, messagebox

from tinui.TinUI import *

from AccountManager import accountManager

"""
2024/7/12
    添加：
    加入查看申请表与查看账户信息功能
by  沈智恺
"""
"""
2024/7/15
    完成了Admin录入单科成绩的界面
    复用Teacher的查看成绩和修改密码功能给Admin
    完成查看账户信息的框架搭建
    处理申请表的框架搭建
    by 廖雨龙
"""
"""
2024/7/16
    完成管理员的修改成绩功能
    将修改成绩和处理申请合并
    by 廖雨龙
"""

import tkinter as tk

import ttkbootstrap as ttk
# 复用Teacher查看成绩的窗口
from Teacher_Window import disp_grades
# 复用Teacher修改密码的函数
from Teacher_Window import change_my_password


def last_step(current_window, previous_window):
    previous_window.deiconify()
    current_window.destroy()


# 获取Treeview中选中的选项,并将其值填入右侧的输入字段
def view_application(tree, entry_id, entry_course, label_original_grade):
    # 看是否有选中什么东西
    selected_item = tree.selection()
    # 如果有选中东西的话,就会填入它的学号和科目和初始成绩 # 待修改
    if selected_item:
        # item_values获取选中的第一行的所有列值(因为可以一次选中很多行)
        item_values = tree.item(selected_item[0], "values")
        # 自动填入学号
        entry_id.delete(0, tk.END)
        entry_id.insert(0, item_values[2])
        # 自动填入科目
        entry_course.delete(0, tk.END)
        entry_course.insert(0, item_values[3])


# 完成成绩申请处理 删除Treeview中选中的项
def finish_application(tree):
    selected_item = tree.selection()
    if selected_item:
        tree.delete(selected_item[0])


# 确认修改 确认并保存修改后的成绩
# 还存在小问题,就是如果是自己输入的话会认为你没有输入
def confirm_modification(entry_id, entry_new_grade):
    # 拿到输入的学号
    student_id = entry_id.get()
    # 拿到输入的新成绩
    new_grade = entry_new_grade.get()
    if student_id and new_grade:  # 这里调用实际的函数
        messagebox.showinfo("成功")
    else:
        messagebox.showinfo("失败")


def update_subject2(selected_subject1, selected_subject2, selected_subject3, subject2_menu, subject3_menu,
                    dynamic_subjects):
    # 更新科目二的选项
    selected_subject2.set("")
    subject2_menu["menu"].delete(0, "end")
    for subject in dynamic_subjects:
        subject2_menu["menu"].add_command(label=subject,
                                          command=lambda value=subject: set_subject2(value, selected_subject2,
                                                                                     selected_subject3, subject3_menu,
                                                                                     dynamic_subjects))
    update_subject3(selected_subject2, selected_subject3, subject3_menu, dynamic_subjects)


def set_subject2(value, selected_subject2, selected_subject3, subject3_menu, dynamic_subjects):
    selected_subject2.set(value)
    update_subject3(selected_subject2, selected_subject3, subject3_menu, dynamic_subjects)


def update_subject3(selected_subject2, selected_subject3, subject3_menu, dynamic_subjects):
    selected_subject2_value = selected_subject2.get()
    selected_subject3.set("")
    subject3_menu["menu"].delete(0, "end")
    for subject in dynamic_subjects:
        if subject != selected_subject2_value:
            subject3_menu["menu"].add_command(label=subject, command=lambda value=subject: selected_subject3.set(value))


# 导入单个成绩的函数
def import_single(admin_window):
    def preSubmit(single_window, name, ID, chinese, Math, english, sub1, sub2, sub3, grade1, grade2, grade3):
        nonlocal warning_text
        warning_text.set('正在导入……')
        # 创建子线程
        thread = threading.Thread(target=submit,
                                  args=[single_window, name, ID, chinese, Math, english, sub1, sub2, sub3, grade1,
                                        grade2, grade3, ])
        thread.start()
        # single_window.mainloop()

    def submit(single_window, name, ID, chinese, Math, english, sub1, sub2, sub3, grade1, grade2, grade3):
        # 测试
        nonlocal flag, warning_text
        # warning_text.set('正在导入……')
        # print(name)
        # print(ID)
        # print(type(chinese))
        # print(Math)
        # print(english)
        # print(sub1)
        # print(sub2)
        # print(sub3)
        # print(type(grade1))
        # print(grade2)
        # print(grade3)
        if (sub1 in ['选科一', ''] or sub2 in ['选科一', ''] or sub3 in ['选科一', '']
                or name == '' or ID == '' or chinese == '' or Math == '' or english == ''):
            flag = 2
            warning_text.set(options[flag])
            print(warning_text)
            return
        try:
            ID = int(ID)
            chinese = int(chinese)
            Math = int(Math)
            english = int(english)
            grade1 = int(grade1)
            grade2 = int(grade2)
            grade3 = int(grade3)
        except Exception as e:
            print("格式错误{}".format(e))
            flag = 1
            warning_text.set(options[flag])
            print(warning_text)
        # 注明flag变量为非本地变量

        flag = accountManager.inputSingleGrades(name, ID, chinese, Math, english, sub1, sub2, sub3, grade1, grade2,
                                                grade3)
        warning_text.set(options[flag])
        print(options[flag])

    single_window = tk.Toplevel(admin_window)
    admin_window.withdraw()
    single_window.geometry("800x600+800+400")
    single_window.resizable(False, False)
    # 姓名 学号 语文 数学 外语 物理/历史 四选二 输入框的文字变量
    var_name = tk.StringVar()
    var_id = tk.StringVar()
    var_chinese = tk.StringVar()
    var_math = tk.StringVar()
    var_english = tk.StringVar()
    var_sub1 = tk.StringVar()
    var_sub2 = tk.StringVar()
    var_sub3 = tk.StringVar()
    # 这三个标记选择了哪个科目
    selected_subject1 = tk.StringVar()
    selected_subject2 = tk.StringVar()
    selected_subject3 = tk.StringVar()
    # 科目的选项
    all_subjects = ["物理", "化学", "生物", "地理", "历史", "政治"]
    dynamic_subjects = ["化学", "生物", "地理", "政治"]  # 去掉物理和历史后的选项
    # 这些固定不变的输入的标签提示语
    labels = ["姓名", "学号", "语文", "数学", "英语"]
    for i, label in enumerate(labels):
        ttk.Label(single_window, text=f"{label}:", font=('黑体', 14)).place(x=100, y=25 + 60 * i)
    # 创建下拉菜单
    subject1_menu = ttk.OptionMenu(single_window, selected_subject1, "选科一", "历史", "物理",
                                   command=lambda value: update_subject2(value, selected_subject2, selected_subject3,
                                                                         subject2_menu, subject3_menu,
                                                                         dynamic_subjects), bootstyle=bootstyle)
    subject1_menu.place(x=100, y=325)
    subject2_menu = ttk.OptionMenu(single_window, selected_subject2, "选科二",
                                   command=lambda *args: update_subject3(selected_subject2, selected_subject3,
                                                                         subject3_menu, dynamic_subjects),
                                   bootstyle=bootstyle)
    subject2_menu.place(x=100, y=385)
    subject3_menu = ttk.OptionMenu(single_window, selected_subject3, "选科三", bootstyle=bootstyle)
    subject3_menu.place(x=100, y=445)
    # 创建各个数据的文本输入框
    name_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_name)
    id_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_id)
    chinese_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_chinese)
    math_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_math)
    english_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_english)
    sub1_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_sub1)
    sub2_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_sub2)
    sub3_entry = ttk.Entry(single_window, show="", font=("黑体", 16), textvariable=var_sub3)
    # 放输入框
    entries = [name_entry, id_entry, chinese_entry, math_entry, english_entry, sub1_entry, sub2_entry, sub3_entry]
    for i, entry in enumerate(entries):
        entry.place(x=250, y=25 + 60 * i)
    # 下面再有两个按钮,一个是确认,一个是返回
    confirm_button = ttk.Button(single_window, text="确认",
                                command=lambda: preSubmit(single_window, var_name.get(), var_id.get(),
                                                          var_chinese.get(),
                                                          var_math.get(), var_english.get(), selected_subject1.get(),
                                                          selected_subject2.get(), selected_subject3.get(),
                                                          var_sub1.get(), var_sub2.get(), var_sub3.get()),
                                width=5,
                                bootstyle=bootstyle)
    confirm_button.place(x=400, y=530)
    cancel_button = ttk.Button(single_window, text="取消", command=lambda: last_step(single_window, admin_window),
                               width=5,
                               bootstyle='darkly')
    cancel_button.place(x=170, y=530)

    flag = 0
    options = ['', '请输入数字！', '请完善信息！', '学号与已导入数据重复！', '分数超出范围！', '导入数据时出现错误！',
               '导入成功！']

    warning_text = ttk.StringVar()
    warning_label = ttk.Label(single_window, textvariable=warning_text, font=('黑体', 10), style="danger")
    warning_label.place(x=100, y=500)
    single_window.mainloop()

    # 在导入单科成绩中点击确认键
    # 这里会传入 姓名:name 学号:ID 语文:chinese 数学:math 英语:english
    # 科目一名称:sub1 科目二名称:sub2 科目三名称:sub3 科目一成绩:grade1 科目二成绩:grade2 科目三成绩:grade3


# 导入成绩函数
def import_grades(admin_window):
    file_path = filedialog.askopenfilename()
    if file_path == '':
        pass
    else:

        # def work_a():
        #     for i in range(10):
        #         print(i, 'a', os.getpid())
        #         time.sleep(0.1)
        def check_condition():
            # print(thread.is_alive())
            if thread.is_alive() is False:
                time.sleep(0.5)
                top.destroy()
                tktop.destroy()
                tktop1 = tk.Toplevel(admin_window)
                tktop1.resizable(False, False)
                tktop1.geometry('200x100+200+250')
                top1 = TinUI(tktop1)
                top1.pack(fill='both', expand=True)
                importedGrades = accountManager.getImportedGrades()
                top1.add_paragraph((70, 20), '导入成功！' if importedGrades is True else '导入失败！')
                # top.add_title('')
                if importedGrades is True:
                    _, _, finish2, _ = top1.add_waitbar3((30, 50), width=150)
                    finish2()

                # top1.after(2000, top1.destroy())
                top1.mainloop()
                # tktop1.destroy()
            else:
                top.after(1000, check_condition)

        def disable_close_button():
            def on_closing():
                # 不执行任何操作，这样就禁用了关闭窗口的功能
                pass

            # 绑定 WM_DELETE_WINDOW 协议到 on_closing 方法
            tktop.protocol("WM_DELETE_WINDOW", on_closing)

        try:
            thread = threading.Thread(target=accountManager.refreshAll, args=(file_path,))
            thread.start()
            tktop = tk.Toplevel(admin_window)
            # tktop.overrideredirect(True)
            # top = tk.Toplevel(admin_window)
            tktop.resizable(False, False)
            tktop.geometry('200x100+200+250')
            disable_close_button()
            top = TinUI(tktop)
            top.pack(fill='both', expand=True)
            # top.add_title('')
            _, _, finish, _ = top.add_waitbar3((25, 50), width=150)

            top.add_paragraph((50, 10), '导入成绩中……')
            check_condition()
            top.mainloop()

        except Exception as e:
            messagebox.showinfo("导入成绩", f"导入失败！{e}")


# 查看成绩申请表函数 查看成绩复核申请表
# 只做了查看功能,还没有添加确认按钮
def admin_disp_apps(admin_window):
    # 创建查看成绩申请的窗口
    admin_window.withdraw()
    apps_window = ttk.Toplevel(admin_window)
    apps_window.title("处理成绩申请")
    apps_window.attributes('-fullscreen', True)
    # 创建左边的框架(查看申请)
    left_frame = ttk.Frame(apps_window, padding=10)
    left_frame.pack(side="left", fill="both", expand=True)

    # 创建Treeview
    columns = ("教师姓名", "学生姓名", "学生学号", "申请科目")
    tree = ttk.Treeview(left_frame, columns=columns, show='headings')
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    tree.pack(fill="both", expand=True, side="left")
    # 得到数据
    data = [('教师1', '学生1', 111, '语文'), ('教师2', '学生2', 222, '数学'), ('教师3', '学生3', 333, '物理')]
    # 将得到的数据放到那个表里面去
    for item in data:
        tree.insert('', tk.END, values=item)
    # 创建垂直滚动条
    scrollbar_y = ttk.Scrollbar(left_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_y.set)
    scrollbar_y.pack(side="right", fill="y")
    # 创建"查看"和"完成"按钮
    view_button = ttk.Button(left_frame, text="查看",
                             command=lambda: view_application(tree, entry_id, entry_course, label_original_grade))
    view_button.pack(pady=5)
    finish_button = ttk.Button(left_frame, text="完成", command=lambda: finish_application(tree))
    finish_button.pack(pady=5)
    # 创建右边的框架(成绩修改)
    right_frame = ttk.Frame(apps_window, padding=10)
    right_frame.pack(side="right", fill="both", expand=True)
    # 创建修改成绩的输入框和标签
    # 学号以及学号的输入框
    ttk.Label(right_frame, text="学号:").grid(row=0, column=0, pady=5, sticky="e")
    entry_id = ttk.Entry(right_frame)
    entry_id.grid(row=0, column=1, pady=5)
    # 显示姓名
    ttk.Label(right_frame, text="姓名:").grid(row=1, column=0, pady=5, sticky="e")
    label_name = ttk.Label(right_frame, text="这里显示学生的姓名")
    label_name.grid(row=1, column=1, pady=5)
    # 科目以及科目的输入框
    ttk.Label(right_frame, text="科目:").grid(row=2, column=0, pady=5, sticky="e")
    entry_course = ttk.Entry(right_frame)
    entry_course.grid(row=2, column=1, pady=5)
    # 显示原来的成绩
    ttk.Label(right_frame, text="原成绩:").grid(row=3, column=0, pady=5, sticky="e")
    label_original_grade = ttk.Label(right_frame, text="这里显示原来的成绩")
    label_original_grade.grid(row=3, column=1, pady=5)
    # 修改后成绩以及修改后成绩的输入框
    ttk.Label(right_frame, text="修改成绩:").grid(row=4, column=0, pady=5, sticky="e")
    entry_new_grade = ttk.Entry(right_frame)
    entry_new_grade.grid(row=4, column=1, pady=5)
    # 修改完成后的确认按钮
    confirm_button = ttk.Button(right_frame, text="确认",
                                command=lambda: confirm_modification(entry_id, entry_new_grade))
    confirm_button.grid(row=5, column=1, pady=10, sticky="e")
    # 之后再在这里加个退出的按钮返回
    quit_button = ttk.Button(right_frame,text="退出",
                             command=lambda:last_step(apps_window,admin_window))
    quit_button.grid(row=5,column=4,pady=10,sticky="e")
    apps_window.mainloop()


# 查看所有用户
# 做一张表查看所有的用户
def admin_disp_users(admin_window):
    admin_window.withdraw()
    users_window = ttk.Toplevel(admin_window)
    users_window.title("处理成绩申请")
    users_window.attributes('-fullscreen', True)
    # 创建一个Frame来包含Treeview和滚动条
    frame = ttk.Frame(users_window)
    frame.pack(fill="both", expand=True)
    # 创建Treeview
    columns = ("栏目一", "栏目二", "栏目三", "栏目四")
    tree = ttk.Treeview(frame, columns=columns, show='headings')
    # 定义每一列的标题和宽度
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    # 得到数据 一个包含所有用户的字典列表
    data = accountManager.getAllUsers()
    # 将得到的数据放到那个表里面去
    for item in data:
        if item['类型'] == 1:
            identity = "教师"
        elif item['类型'] == 2:
            identity = "学生"
        else:
            identity = "管理员"
        tree.insert('', tk.END, values=(item['姓名'], item['密码'], item['学号或工号'], identity))
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
    con_button = ttk.Button(users_window, text='确认', command=lambda: last_step(users_window, admin_window), width=10,
                            bootstyle=bootstyle)
    con_button.pack(pady=10)
    users_window.mainloop()


# 退出登录函数，返回初始登录界面
def admin_logout(admin_window, login_window, username_entry, password_entry):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    admin_window.destroy()
    login_window.deiconify()


def show_admin_window(login_window, userid_entry, password_entry, res_name):
    admin_window = ttk.Toplevel()
    admin_window.title('admin_window')
    admin_window.geometry('800x1000+800+400')

    admin_window.resizable(False, False)
    # 标题
    welcome_title = ttk.Label(admin_window, text='你好！' + res_name, font=('黑体', 15))
    # welcome_title.place_configure(anchor='nw')
    welcome_title.place(x=0, y=0)
    padding = 15
    pady = 20
    bootstyle = 'info-outline'
    blank_title = ttk.Label(admin_window, text='', font=('黑体', 10))
    blank_title.pack(pady=20)
    # 单个添加学生成绩按钮
    bt_import_single = ttk.Button(admin_window, text='导入单个学生成绩', command=lambda: import_single(admin_window),
                                  width=20, bootstyle=bootstyle, padding=padding)
    bt_import_single.pack(pady=pady)
    # 导入学生成绩按钮
    bt_import_grades = ttk.Button(admin_window, text='导入学生成绩', command=lambda: import_grades(admin_window),
                                  width=20, bootstyle=bootstyle, padding=padding)
    bt_import_grades.pack(pady=pady)
    # bt_import_grades.place(x=180, y=100)

    # 查看学生成绩按钮 # 复用教师的查看成绩窗口
    bt_show_grades = ttk.Button(admin_window, text='查看成绩', command=lambda: disp_grades(admin_window, res_name),
                                width=20,
                                bootstyle=bootstyle, padding=padding)
    bt_show_grades.pack(pady=pady)
    # bt_show_grades.place(x=180, y=200)

    # 查看成绩复核申请表

    bt_show_apps = ttk.Button(admin_window, text='查看成绩复核申请表', command=lambda: admin_disp_apps(admin_window),
                              width=20, bootstyle=bootstyle, padding=padding)
    bt_show_apps.pack(pady=pady)
    # bt_show_apps.place(x=180, y=300)

    # 查看所有账户信息

    bt_show_users = ttk.Button(admin_window, text='查看账户信息', command=lambda: admin_disp_users(admin_window),
                               width=20, bootstyle=bootstyle, padding=padding)
    bt_show_users.pack(pady=pady)
    # bt_show_users.place(x=180, y=400)

    # 修改密码（包括修改管理员的密码和重置用户的密码） # 复用教师的修改密码
    bt_modify_password = ttk.Button(admin_window, text='修改密码',
                                    command=lambda: change_my_password(admin_window, password_entry.get()),
                                    width=20,
                                    bootstyle=bootstyle, padding=padding)
    bt_modify_password.pack(pady=pady)
    # bt_modify_password.place(x=180, y=500)

    # 将这个功能放到处理申请表里面去
    # # 修改学生成绩
    # bt_modify_grades = ttk.Button(admin_window, text='修改成绩', command=admin_modify_grades, width=20,
    #                               bootstyle=bootstyle, padding=padding)
    # bt_modify_grades.pack(pady=pady)
    # # bt_modify_grades.place(x=180, y=600)

    # 退出
    bt_logout = ttk.Button(admin_window, text='退出登录',
                           command=lambda: admin_logout(admin_window, login_window, userid_entry, password_entry),
                           width=20, bootstyle=bootstyle, padding=padding)
    bt_logout.pack(pady=pady)

    # .place(x=180, y=700)


# 使用teacher里面的配置
padding = 15
pady = 20
bootstyle = 'info-outline'
