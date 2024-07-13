"""
2024/7/11
    管理员窗口
by 刘杨健
"""
from tkinter import filedialog, messagebox

from tinui.TinUI import *

from AccountManager import accountManager, importedGrades

"""
2024/7/12
    添加：
    加入查看申请表与查看账户信息功能
by  沈智恺
"""

import tkinter as tk


def last_step(current_window, previous_window):
    previous_window.deiconify()
    current_window.destroy()


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
                # finish()
                # #top.after(1000,top.destroy())
                # top.mainloop()
                time.sleep(0.5)
                top.destroy()
                tktop.destroy()
                tktop1 = tk.Toplevel(admin_window)
                tktop1.resizable(False, False)
                tktop1.geometry('200x100+200+250')
                top1 = TinUI(tktop1)
                top1.pack(fill='both', expand=True)
                top1.add_paragraph((70, 20), '导入成功！')
                # top.add_title('')
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

            # label = tk.Label(top, text="正在导入成绩……", font=('楷体', 15))
            # label.pack()
            top.mainloop()
            print('hello')
            if importedGrades is False:
                messagebox.showinfo("导入成绩", f"导入失败！")
        except Exception as e:
            messagebox.showinfo("导入成绩", f"导入失败！{e}")


# 查看学生成绩函数
def admin_disp_grads():
    pass


# 查看成绩申请表函数
def admin_disp_apps(admin_window):
    admin_window.withdraw()
    page2 = tk.Toplevel(admin_window)
    page2.title('申请表信息')
    page2.geometry("600x400+100+150")
    l2 = tk.Label(page2, text='申请表信息', font=("楷体", 20))
    l2.pack()
    page2.focus_force()
    last_step_button = tk.Button(page2, text='返回上一步', command=lambda: last_step(page2, admin_window),
                                 width=30, height=3)
    last_step_button.pack()
    page2.mainloop()


# 查看所有用户
def admin_disp_users(admin_window):
    admin_window.withdraw()
    user_window = tk.Toplevel(admin_window)
    user_window.title('账号信息')
    user_window.geometry("600x400")
    l1 = tk.Label(user_window, text='账号信息', font=("楷体", 20))
    l1.pack()
    user_window.focus_force()
    last_step_button = tk.Button(user_window, text='返回上一步', command=lambda: last_step(user_window, admin_window),
                                 width=30, height=3)
    last_step_button.pack()
    user_window.mainloop()
    pass


# 修改密码
def admin_modify_password():
    pass


# 修改成绩
def admin_modify_grades():
    pass


# 退出登录函数，返回初始登录界面
def admin_logout(admin_window, login_window, username_entry, password_entry):
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)
    admin_window.destroy()
    login_window.deiconify()


def show_admin_window(login_window, username_entry, password_entry):
    admin_window = tk.Toplevel()
    admin_window.title('admin_window')
    admin_window.geometry('600x400')
    admin_window.resizable(False, False)
    # 标题
    welcome_title = tk.Label(admin_window, text='你好！' + username_entry.get(), font=('楷体', 10), width=10, height=2,
                             bg='red')
    # welcome_title.place_configure(anchor='nw')
    welcome_title.place(x=0, y=0)

    # 导入学生成绩按钮
    bt_import_grades = tk.Button(admin_window, text='导入学生成绩', command=lambda: import_grades(admin_window),
                                 font=('楷体', 18), width=20,
                                 height=1)
    bt_import_grades.place(x=180, y=40)

    # 查看学生成绩按钮
    bt_show_grades = tk.Button(admin_window, text='查看成绩', command=admin_disp_grads, font=('楷体', 18), width=20,
                               height=1)
    bt_show_grades.place(x=180, y=90)

    # 查看成绩复核申请表

    bt_show_apps = tk.Button(admin_window, text='查看成绩复核申请表', command=lambda: admin_disp_apps(admin_window),
                             font=('楷体', 18),
                             width=20, height=1)
    bt_show_apps.place(x=180, y=140)

    # 查看所有账户信息

    bt_show_users = tk.Button(admin_window, text='查看账户信息', command=lambda: admin_disp_users(admin_window),
                              font=('楷体', 18), width=20,
                              height=1)
    bt_show_users.place(x=180, y=190)

    # 修改密码（包括修改管理员的密码和重置用户的密码）
    bt_modify_password = tk.Button(admin_window, text='修改密码', command=admin_modify_password, font=('楷体', 18),
                                   width=20, height=1)
    bt_modify_password.place(x=180, y=240)

    # 修改学生成绩
    bt_modify_grades = tk.Button(admin_window, text='修改成绩', command=admin_modify_grades, font=('楷体', 18),
                                 width=20, height=1)
    bt_modify_grades.place(x=180, y=290)

    # 退出
    bt_logout = tk.Button(admin_window, text='退出登录',
                          command=lambda: admin_logout(admin_window, login_window, username_entry, password_entry),
                          font=('楷体', 18), width=20, height=1)

    bt_logout.place(x=180, y=340)
