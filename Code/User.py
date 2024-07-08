'''
2024/7/5
    class User
    setUserName()
    setPassWord()
by 刘杨健
'''


# User基类
# userName:string 用户姓名
# passWord:string 密码
# ID:int 编号，每个用户应该具有唯一编号
class User:
    def __init__(self, userName, passWord, ID):
        self.__userName = userName
        self.__passWord = passWord
        self.__ID = ID

    # 判断用户名和密码是否合法的函数
    def __isLegal(self, str):
        flag = True  # 合法标志
        if str == ' ':
            flag = False
        else:
            for i in str:
                if i == ' ':
                    flag = False
                    break
        return flag

    # 设置用户名
    def setUserName(self, str):
        # 如果名字相同，不做修改
        if str == self.__userName:
            return True
        # 如果用户名违法，则设置失败
        if self.__isLegal(str):
            self.__userName = str
            return True
        else:
            return False

    # 设置密码
    def setPassWord(self, str):
        if str == self.__passWord:
            return True
        # 如果密码违法，则设置失败
        if self.__isLegal(str):
            self.__passWord = str
            return True
        else:
            return False

    # 测试函数 打印用户信息
    def showUserInfo(self):
        print(f'用户名：{self.__userName}\t密码：{self.__passWord}\t编号：{self.__ID}')


# 测试函数
if __name__ == '__main__':
    stu = User("berber", 114514, 0)
    stu.showUserInfo()
    stu.setUserName("liangjian")
    stu.showUserInfo()
    stu.setUserName(' ')
    stu.showUserInfo()
    stu.setPassWord(' ')
    stu.showUserInfo()
    stu.setPassWord('123456')
    stu.showUserInfo()
