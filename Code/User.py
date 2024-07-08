'''
2024/7/5
    class User
    setUserName()
    setPassWord()
by 刘杨健
2023/7/8
    class User
    修改
by陈邱华
'''


# User基类
# userName:string 用户姓名
# passWord:string 密码
# ID:int 编号，每个用户应该具有唯一编号
class User:
    def __init__(self, userName, password, ID, flag):
        self.userName = userName
        self.password = password
        self.ID = ID
        self.flag = flag

    # 判断用户名和密码是否合法的函数
    def __isLegal(self, myStr):
        flag = True  # 合法标志
        if myStr == ' ':
            flag = False
        else:
            for i in myStr:
                if i == ' ':
                    flag = False
                    break
        return flag

    # 设置用户名
    def setUserName(self, myStr):
        # 如果名字相同，不做修改
        if myStr == self.userName:
            return True
        # 如果用户名违法，则设置失败
        if self.__isLegal(myStr):
            self.userName = myStr
            return True
        else:
            return False

    # 设置密码
    def setPassWord(self, myStr):
        if myStr == self.passWord:
            return True
        # 如果密码违法，则设置失败
        if self.__isLegal(myStr):
            self.passWord = myStr
            return True
        else:
            return False

    # 测试函数 打印用户信息
    def showUserInfo(self):
        print(f'用户名：{self.userName}\t密码：{self.passWord}\t编号：{self.ID}')


'''
7.7
User_Administrator
by 刘链凯

7/8
class User_Student
修改
by陈邱华
'''


class User_Administrator(User):
    def __init__(self, userName, password, ID, flag):
        super().__init__(userName, password, ID, flag)

    def getSingleGrades(self):
        pass
        # return self.gradeManager.getGrades(1)

    def getAllGrades(self):
        pass
        # return self.gradeManager.getGrades(2)

    def changeGrades(self, name, stuID, sub, grade):
        pass
        # self.gradeManager.changeGrades(name, stuID, sub, grade)


'''
7.7
class User_Teacher
by 刘链凯

7/8
class User_Student
修改
by陈邱华
'''


class User_Teacher(User):
    def __init__(self, userName, password, ID, flag):
        super().__init__(userName, password, ID, flag)

    def getSingleGrades(self, name, stuID, sub, grade):
        pass
        # return self.gradeManager.inputSingle(name, stuID, grade)

    def getAllGrades(self, mode, *args):
        pass
        # return self.gradeManager.inputGrades(mode, *args)

    def GradesCheck(self, name, stuID, subject):
        pass
        # return self.gradeManager.checkGrades(name, stuID, subject)


'''
7.7
class User_Student
by 刘链凯

7/8
class User_Student
修改
by陈邱华
'''


class User_Student(User):
    def __init__(self, userName, password, ID, flag):
        super().__init__(userName, password, ID, flag)

    def getSingleGrades(self, name, stuID, sub, grade) -> bool:
        pass
        # gradeManager = GradeManager.GradeManager(self.userName, self.ID, [])
        # return gradeManager.inputSingle(name, stuID, grade)

    def GradesCheck(self, name, stuID, subject) -> bool:
        pass
        # gradeManager = GradeManager.GradeManager(self.userName, self.ID, [])
        # return gradeManager.inputGrades(1, name, stuID, subject)


# 测试函数
if __name__ == '__main__':
    stu = User_Administrator("berber", 114514, 0)
    # print(stu.ID)
    stu.showUserInfo()
    stu.setUserName("liangjian")
    stu.showUserInfo()
    stu.setUserName(' ')
    stu.showUserInfo()
    stu.setPassWord(' ')
    stu.showUserInfo()
    stu.setPassWord('123456')
    stu.showUserInfo()
