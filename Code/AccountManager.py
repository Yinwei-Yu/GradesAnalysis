import pandas as pd

from GradeManager import gradeManager
from User import *


class AccountManager:
    # 从账号文件中读取
    def __init__(self):
        self.users = {}
        self.userName: str = ""
        self.password: int = 0
        self.flag: int = 0
        # 管理员为1，教师为2，学生为3
        self.ID: int = 0
        self.userNum = 0

        # 从学生信息中读取

    def inputUsers(self, path):
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            flag = row['类型']
            if flag == 1:
                user = User_Administrator(row['用户名'], row['密码'], row['学号/工号'], flag)
            if flag == 2:
                user = User_Teacher(row['用户名'], row['密码'], row['学号/工号'], flag)
            if flag == 3:
                user = User_Student(row['用户名'], row['密码'], row['学号/工号'], flag)

            self.users.update({user.ID: user})
            # print(type(user))

        self.userNum = len(self.users)
        print(self.userNum)
        for ID in self.users:
            print(self.users[ID].userName, self.users[ID].password, ID, sep=" ")

        return

    # 账号登录
    # 待实现
    def login(self, userName: str, password: int) -> bool:
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

    def logout(self) -> bool:
        self.userName = ""
        self.password = 0
        self.flag = 0
        # 管理员为1，教师为2，学生为3
        self.ID = 0
        return True

    def changePassword(self, origiPassword: int, newPassword: int) -> bool:
        if origiPassword == self.password:
            self.users[self.ID].password = newPassword
            return True
        else:
            return False

    # 创建新用户名

    def createUser(self, userName: str, password: int, ID: int, flag: int) -> bool:
        # 判断用户名是否已经创建
        if self.users.get(ID) is None:
            if flag == 1:
                self.users.update({ID: User_Administrator(userName, password, ID, flag)})
            if flag == 2:
                self.users.update({ID: User_Teacher(userName, password, ID, flag)})
            return True
        else:
            return False

    def printUserInfo(self):
        print(self.userName, self.ID, self.password, self.flag)

    def changeUserName(self, newUserName: str) -> bool:
        pass

    def saveUserInfo(self):
        user_name_list = [self.users[key].userName for key in self.users]
        user_password_list = [self.users[key].password for key in self.users]
        user_ID_list = [self.users[key].ID for key in self.users]
        user_flag_list = [self.users[key].flag for key in self.users]
        data = {'用户名': user_name_list, '密码': user_password_list, '学号/工号': user_ID_list, '类型': user_flag_list}

        df = pd.DataFrame(data)

        df.to_csv('users.csv', index=False, mode='w')


# 获取成绩
# mode==1时返回学生类型
# mode==2时返回全班分析
# 待完成
def getGrades(self, mode, stuID=0) -> list:
    if mode == 1:
        for temp in gradeManager.student:
            if temp.ID == stuID:
                return temp
    if mode == 2:
        return gradeManager.student


if __name__ == "__main__":
    # gradeManager = GradeManager([], 0, [])
    # gradeManager.inputCSV("./student.csv")
    # for x in gradeManager.student:
    #     print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)
    accountManager = AccountManager()
    accountManager.inputUsers("./users.csv")
    accountManager.login('user1', 111111)
    accountManager.printUserInfo()
    accountManager.saveUserInfo()
