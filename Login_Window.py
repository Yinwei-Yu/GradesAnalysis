import tkinter as tk

window=tk.Tk()
window.title('main window')
window.geometry('600x400')
l=tk.Label(window,text='高考成绩管理系统',font=('Arial',20),width=20,height=2)
l.pack(side='top')

#用户名和密码的提示标签
username_label=tk.Label(window,text='用户名:',font=('Arial',10))
username_label.place(x=140,y=100)
password_label=tk.Label(window,text='密码:',font=('Arial',10))
password_label.place(x=140,y=140)
#用户名和密码的输入框
username_entry=tk.Entry(window,show=None,font=('Arial',14))
username_entry.place(x=190,y=100)

password_entry=tk.Entry(window,show='*',font=('Arial',14))
password_entry.place(x=190,y=140)

#显示身份的标签（测试）
identity_var=tk.StringVar()
identity_disp=tk.Label(window,textvariable=identity_var)
identity_disp.place(x=190,y=260)

#选项触发函数
def identity_selection():
    identity_var.set(identity_var.get())

#身份选择Radiobutton
identity_label=tk.Label(window,text='身份:',font=('Arial',10))
identity_label.place(x=140,y=180)
radiobt_student=tk.Radiobutton(window,text='学生',variable=identity_var,value='学生',command=identity_selection)
radiobt_teacher=tk.Radiobutton(window,text='老师',variable=identity_var,value='老师',command=identity_selection)
radiobt_administrator=tk.Radiobutton(window,text='管理员',variable=identity_var,value='管理员',command=identity_selection)
radiobt_student.place(x=190,y=180)
radiobt_teacher.place(x=190,y=205)
radiobt_administrator.place(x=190,y=230)

#接受log_in函数传出的内容显示在标签上
login_var=tk.StringVar()
login_label=tk.Label(window,textvariable=login_var)
login_label.place(x=240,y=280)

#按钮+函数，传出的内容显示在标签上，内容通过var传递

login_hit=False     #登录函数
def log_in():
    global login_hit
    #login_hit == False and
    if  not username_entry.get().strip()=="" and not password_entry.get().strip()=="":
        #login_hit=True
        login_var.set('成功登录')
    else:
        #login_hit=False
        login_var.set('请输入用户名和密码')


#添加command参数补充按钮功能
bt_login=tk.Button(window,text='登录',font=('Arial',12),width=10,height=1,command=log_in)
bt_login.place(x=100,y=300)

bt_logout=tk.Button(window,text='退出',font=('Arial',12),width=10,height=1)
bt_logout.place(x=400,y=300)

window.mainloop()
