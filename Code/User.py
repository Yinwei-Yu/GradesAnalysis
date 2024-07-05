'''
2024/7/5
    class User
by 刘杨健
'''

'''
用户基类
'''

class User():
    def __init__(self,userName,passWord,ID):
        self.__userName=userName
        self.__passWord=passWord
        self.__ID=ID


    #判断用户名和密码是否合法的函数
    def __isLegal(self,str):
        flag=True   #合法标志
        if str == ' ':
            flag = False
        else:
            for i in str:
                if i == ' ':
                    flag=False
                    break
        return flag


    #设置用户名
    def setUserName(self,str):
        #如果名字相同，不做修改
        if str==self.__userName:
            return True
        #如果用户名违法，则设置失败
        if self.__isLegal(str):
            self.__userName=str
            return True
        else:
            return False


    #设置密码
    def setPassWord(self,str):
        if str==self.__passWord:
            return True
        # 如果密码违法，则设置失败
        if self.__isLegal(str):
            self.__passWord = str
            return True
        else:
            return False
