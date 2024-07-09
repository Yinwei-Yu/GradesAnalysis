import pandas as pd

from GradeManager import gradeManager
from User import *

'''
2024/7/8
AccountManager类
    inputUsers()
    login()
    logout()
    changePassword()
    createUser()
    printUserInfo()
    changeUserName()
    saveUserInfo()
    
by陈邱华

2024/7/9
AccountManager类
    refreshUserInfo()
    getGrades()
by陈邱华
'''


class AccountManager:
    # 初始化，并从'./users.csv'读取文件信息
    def __init__(self):
        self.users = {}
        self.userName: str = ''
        self.password: str = ''
        self.flag: int = 0
        # 管理员为1，教师为2，学生为3
        self.ID: int = 0
        self.userNum = 0
        self.inputUsers('./users.csv')

    # 读取用户信息
    # 文件格式为.csv
    # path为文件路径信息
    def inputUsers(self, path):
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            flag = row['类型']
            if flag == 1:
                user = User_Administrator(row['用户名'], str(row['密码']), row['学号/工号'], flag)
            if flag == 2:
                user = User_Teacher(row['用户名'], str(row['密码']), row['学号/工号'], flag)
            if flag == 3:
                user = User_Student(row['用户名'], str(row['密码']), row['学号/工号'], flag)

            self.users.update({user.ID: user})
            # print(type(user))

        self.userNum = len(self.users)
        # print(self.userNum)
        # for ID in self.users:
        #     print(self.users[ID].userName, self.users[ID].password, ID, sep=" ")

        return

    # 账号登录
    # userName:str 从前端获得的用户名
    # password:str 从前端获得的密码信息
    def login(self, userName: str, password: str) -> bool:
        for ID in self.users:
            user = self.users[ID]
            if user.userName == userName and user.password == password:
                self.userName = user.userName
                self.password = user.password
                self.ID = user.ID
                self.flag = user.flag
                print("登录成功")
                return True
        print("登录失败")
        return False

    # 登出，将类属性重置
    def logout(self) -> bool:
        self.userName = ""
        self.password = 0
        self.flag = 0
        # 管理员为1，教师为2，学生为3
        self.ID = 0
        return True

    # 修改密码
    # originPassword:str 前端获取的原密码
    # newPassword:str 前端获取的新密码
    def changePassword(self, originPassword: str, newPassword: str) -> bool:

        if self.users[self.ID].setPassword(newPassword) is False or self.password != originPassword:
            return False
        else:
            self.password = newPassword
            self.saveUserInfo()
            return True

    # 创建新用户名
    '''
    userName: str:前端输入的待创建的用户名
    password: int：前端输入的密码
    ID: int：前端输入的学号或工号
    flag: int
    '''

    def createUser(self, userName: str, password: str, ID: int, flag: int) -> bool:
        # 判断用户名是否已经创建
        if self.users.get(ID) is None:
            if flag == 1:
                self.users.update({ID: User_Administrator(userName, password, ID, flag)})
            if flag == 2:
                self.users.update({ID: User_Teacher(userName, password, ID, flag)})
            print("成功创建用户名！")
            self.saveUserInfo()
            return True
        else:
            print("该用户名已被创建！")
            return False

    def printUserInfo(self):
        self.users[self.ID].showUserInfo()

    def printAllUsersInfo(self):
        for key in self.users:
            self.users[key].showUserInfo()

    def getCheckApplications(self):
        return gradeManager.checkApplication

    # 修改用户名
    # newUserName :str 前端输入的新用户名
    def changeUserName(self, newUserName: str) -> bool:
        if self.users[self.ID].setUserName(newUserName) is True:
            self.userName = newUserName
            self.saveUserInfo()
            return True
        else:
            return False

    # 保存用户信息，便于下次系统启动时获取信息
    def saveUserInfo(self):
        user_name_list = [self.users[key].userName for key in self.users]
        user_password_list = [self.users[key].password for key in self.users]
        user_ID_list = [self.users[key].ID for key in self.users]
        user_flag_list = [self.users[key].flag for key in self.users]
        data = {'用户名': user_name_list, '密码': user_password_list, '学号/工号': user_ID_list, '类型': user_flag_list}

        df = pd.DataFrame(data)

        df.to_csv('users.csv', index=False, mode='w')

    # 更新用户信息
    # 根据学生信息更新用户信息，并置初始密码为123456
    def refreshUserInfo(self):
        for student in gradeManager.student:
            if self.users.get(student.stuID) is None:
                self.users.update(({student.stuID: User(student.name, '123456', student.stuID, 3)}))
            else:
                self.users.update(
                    {student.stuID: User(self.users[student.stuID].userName, self.users[student.stuID].password,
                                         student.stuID, 3)})
        self.saveUserInfo()

    # 获取成绩
    # mode==1时返回学生分析
    # mode==2时返回全班分析
    # 待完成
    def getGrades(self, mode, stuID=0) -> list:
        if mode == 1:
            for temp in gradeManager.student:
                if temp.ID == stuID:
                    return temp
        if mode == 2:
            gradeManager.generateGradesAnalysis(1, 'Chinese')
            gradeManager.generateGradesAnalysis(1, 'Math')
            gradeManager.generateGradesAnalysis(1, 'English')
            gradeManager.generateGradesAnalysis(1, 'Physics')
            gradeManager.generateGradesAnalysis(1, 'Chemistry')
            gradeManager.generateGradesAnalysis(1, 'Biology')
            gradeManager.generateGradesAnalysis(2, 1)
            return gradeManager.student

    def dispAllGrades(self):
        gradeManager.dispAllGrades()


if __name__ == "__main__":
    # gradeManager = GradeManager([], 0, [])
    # gradeManager.inputCSV("./student.csv")
    # for x in gradeManager.student:
    #     print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)
    accountManager = AccountManager()
    while True:
        print('管理员账号：user1，密码：111111')
        print("请输入选项：1、登录，2、注册（仅限管理员和教师），3、退出系统：")
        op = eval(input())
        if op == 1:
            print('请输入账号：')
            account = input()
            print('请输入密码：')
            password = input()
            if accountManager.login(account, password) is False:
                continue

        if op == 2:
            print('请输入新账号：')
            account = input()
            print('请输入新账号密码：')
            password = eval(input())
            print('请输入工号：')
            ID = eval(input())
            print('请输入类型：1、管理员，2、教师')
            flag = eval(input())
            accountManager.createUser(account, password, ID, flag)
            print('注册成功，请登录！')
            continue

        if op == 3:
            break

        if accountManager.flag == 1:
            print('登录成功')
            while True:
                print(
                    '请输入选项：\n1、查看成绩\n2、修改账号名称\n3、修改密码\n4、导入学生账号\n5、查看成绩修改申请单\n'
                    '6、输出当前账号信息\n7、输出所有账号信息\n8、查看所有学生成绩\n9、登出账号\n')

                op = eval(input())
                if op <= 0 or op > 9:
                    continue
                if op == 1:
                    accountManager.getGrades(2)
                if op == 2:
                    print('当前账号名称为：{}'.format(accountManager.userName))
                    print('请输入新账号名称：')
                    newName = input()
                    accountManager.changeUserName(newName)
                    print('按enter继续……')
                    input()
                if op == 3:
                    print('请输入旧密码：')
                    password = input()
                    print('请输入新密码：')
                    newPassword = input()
                    if accountManager.changePassword(password, newPassword) is True:
                        print('修改成功，按enter继续……')
                        input()
                    else:
                        print('修改失败，按enter继续……')
                        input()

                if op == 4:
                    accountManager.refreshUserInfo()
                    print('导入成功')
                    print('按enter继续……')
                    input()

                if op == 5:
                    print(gradeManager.checkApplication)
                    print('按enter继续……')
                    input()

                if op == 6:
                    accountManager.printUserInfo()
                    print('按enter继续……')
                    input()

                if op == 7:
                    accountManager.printAllUsersInfo()
                    print('按enter继续……')
                    input()

                if op == 8:
                    accountManager.dispAllGrades()
                    print('按enter继续……')
                    input()

                if op == 9:
                    accountManager.logout()
                    accountManager.saveUserInfo()
                    break

# accountManager.inputUsers("./users.csv")
# accountManager.login('user1', 111111)
# accountManager.printUserInfo()
# accountManager.refreshUserInfo()
# accountManager.printUserInfo()
# accountManager.saveUserInfo()
