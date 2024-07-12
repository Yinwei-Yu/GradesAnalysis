"""
2024/7/11
    管理员窗口
by 刘杨健
"""

import tkinter as tk

# 导入成绩函数
def import_grades():
    pass


# 查看学生成绩函数
def admin_disp_grads():
    pass


# 查看成绩申请表函数
def admin_disp_apps():
    pass


# 查看所有用户
def admin_disp_users():
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
    welcome_title = tk.Label(admin_window, text='你好！' + username_entry.get(), font=('楷体', 10), width=10, height=2,bg='red')
    # welcome_title.place_configure(anchor='nw')
    welcome_title.place(x=0,y=0)

    # 导入学生成绩按钮
    bt_import_grades = tk.Button(admin_window, text='导入学生成绩', command=import_grades, font=('楷体', 18),width=20,height=1)
    bt_import_grades.place(x=180,y=40)

    # 查看学生成绩按钮
    bt_show_grades = tk.Button(admin_window, text='查看成绩', command=admin_disp_grads, font=('楷体', 18),width=20,height=1)
    bt_show_grades.place(x=180,y=90)

    # 查看成绩复核申请表
    bt_show_apps = tk.Button(admin_window, text='查看成绩复核申请表', command=admin_disp_apps, font=('楷体', 18),width=20,height=1)
    bt_show_apps.place(x=180,y=140)

    # 查看所有账户信息
    bt_show_users = tk.Button(admin_window, text='查看账户信息', command=admin_disp_users, font=('楷体', 18), width=20,
                              height=1)
    bt_show_users.place(x=180, y=190)

    # 修改密码（包括修改管理员的密码和重置用户的密码）
    bt_modify_password = tk.Button(admin_window, text='修改密码', command=admin_modify_password, font=('楷体', 18),width=20,height=1)
    bt_modify_password.place(x=180,y=240)

    # 修改学生成绩
    bt_modify_grades = tk.Button(admin_window, text='修改成绩', command=admin_modify_grades, font=('楷体', 18),width=20,height=1)
    bt_modify_grades.place(x=180,y=290)

    # 退出
    bt_logout = tk.Button(admin_window, text='退出登录',
                          command=lambda: admin_logout(admin_window, login_window, username_entry, password_entry),
                          font=('楷体', 18),width=20,height=1)
    bt_logout.place(x=180,y=340)
