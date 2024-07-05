class AccountManager:
    # 从账号文件中读取
    def __init__(self):
        self.users = {}
        self.userName: str = ""
        self.password: int = 0
        self.flag: int = 0
        # 管理员为1，教师为2，学生为3
        self.ID: int = 0
        for user in self.users:
            print(type(user))

        # 从学生信息中读取

    def createUsers(self):
        pass

    # 账号登录
    # 待实现
    def login(self, userName: str, password: str) -> bool:
        for user in self.users:
            if user.name == userName and user.password == password:
                self.userName = user.name
                self.password = user.password
                print(type(user))
                return True
        return False

    def logout(self) -> bool:
        pass

    def changePassword(self, origiPassword: str, newPassword: str) -> bool:
        if origiPassword == self.password:
            self.password = newPassword
            return True
        else:
            return False

    def changeUserName(self, newUserName: str) -> bool:
        pass

    def getGrades(self, mode: int, *args: None) -> list:
        pass
