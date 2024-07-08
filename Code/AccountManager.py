import pandas as pd

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
        # for ID in self.users:
        #     print(self.users[ID].userName, self.users[ID].passWord, ID, sep=" ")

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

    def printUserInfo(self):
        print(self.userName, self.ID, self.password, self.flag)

    def changeUserName(self, newUserName: str) -> bool:
        pass

    def getGrades(self, mode: int, *args: None) -> list:
        pass


if __name__ == "__main__":
    # gradeManager = GradeManager([], 0, [])
    # gradeManager.inputCSV("./student.csv")
    # for x in gradeManager.student:
    #     print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)
    accountManager = AccountManager()
    accountManager.inputUsers("./users.csv")
    accountManager.login('user1', 111111)
