from tkinter import messagebox

import mysql.connector  # pip install mysql-connector-python

from GradeManager import gradeManager
from User import *
from csvToSQL import *

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

2024/7/14
AccountManager
    getAllGrades()
by陈邱华

2024/7/15
AccountManager
    getAllUsers()
    getAllApplications()
by陈邱华

2024/7/17
AccountManager
    setRankings()
    addCheckApplication()
    delteteCheckApplication()
    修改了login()
by陈邱华
2024/7/18
AccountManager
   TruncateUsers() 
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
        # self.inputUsers('./excelFiles/users.csv')
        self.getUserFromSql()
        self.setRankings()

    # 读取用户信息
    # 文件格式为.csv
    # path为文件路径信息
    def inputUsers(self, path):
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            flag = row['类型']
            if flag == 1:
                user = User_Administrator(row['用户名'], str(row['密码']), int(row['学号或工号']), flag)
            if flag == 2:
                user = User_Teacher(row['用户名'], str(row['密码']), int(row['学号或工号']), flag)
            if flag == 3:
                user = User_Student(row['用户名'], str(row['密码']), int(row['学号或工号']), flag)

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
    def login(self, ID: int, password: str):
        if self.users.get(ID) is None:
            return False, 0, 0  # 用户名不存在
        if self.users[ID].password == password:
            self.ID = ID
            self.userName = self.users[ID].userName
            self.password = password
            self.flag = self.users[ID].flag
            return True, self.flag, self.userName  # 用户名存在且密码正确
        return True, 0, 0  # 用户存在但密码错误

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
    def changePassword(self, originPassword: str, newPassword_first: str, newPassword_second: str, user_id) -> bool:
        # 错误检测
        if originPassword == "":
            messagebox.showinfo('提示', "原密码为空")
            return False
        if originPassword != self.users[user_id].password:
            messagebox.showinfo('提示', "原密码错误")
            return False
        if newPassword_first == "":
            messagebox.showinfo('提示', "新密码为空")
            return False
        if newPassword_second == "":
            messagebox.showinfo('提示', "请再次输入新密码")
            return False
        if newPassword_first != newPassword_second:
            messagebox.showinfo('提示', "重复密码不一致")
            return False

            # 修改密码
        self.users[user_id].password = newPassword_first
        self.saveUserInfoToCSV()
        self.updateUserInfoToMySQL(user_id)  # 保存信息到数据库
        return True

    # 修改密码
    def updateUserInfoToMySQL(self, user_id,
                              host=host,  # 主机地址
                              user=user,  # 数据库用户名
                              password=password,  # 密码
                              database=database,  # 数据库名称
                              table=usersTable,  # 数据库表名
                              ):

        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        sqlUpdate = f"""UPDATE {table} SET `密码` = %s WHERE `学号或工号` = %s"""
        data = (self.users[user_id].password, user_id)
        # 更新
        mycursor.execute(sqlUpdate, data)
        # 提交更改并关闭数据库连接
        mydb.commit()  # 提交更改
        mycursor.close()  # 关闭游标对象
        mydb.close()  # 关闭数据库连接
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
            self.saveUserInfoToCSV()
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
            self.saveUserInfoToCSV()
            return True
        else:
            return False

    def getUserInofoTable(self):
        data = []
        user_name_list = [self.users[key].userName for key in self.users]
        user_password_list = [self.users[key].password for key in self.users]
        user_ID_list = [self.users[key].ID for key in self.users]
        user_flag_list = [self.users[key].flag for key in self.users]
        data = {'用户名': user_name_list, '密码': user_password_list, '学号或工号': user_ID_list,
                '类型': user_flag_list}
        return data

    # 保存用户信息，便于下次系统启动时获取信息
    def saveUserInfoToCSV(self, path='./excelFiles/users.csv'):
        try:
            data = self.getUserInofoTable()
            df = pd.DataFrame(data)
            df.to_csv(path, index=False)
            return True
        except Exception as e:
            print("保存用户信息至csv文件时出现错误：{}".format(e))
            return False

    def saveUserInfoToMySQL(self,
                            host=host,  # 主机地址
                            user=user,  # 数据库用户名
                            password=password,  # 密码
                            database=database,  # 数据库名称
                            table=usersTable,  # 数据库表名
                            ):
        # 将数据转换为 DataFrame
        data = self.getUserInofoTable()

        df = pd.DataFrame(data)
        # print(df)
        # 将dataframe保存至数据库
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:

            # for row in df.itertuples(index=False, name=None):  # name=None 使得返回的namedtuple不包含额外的索引名
            #     sql = (f'INSERT IGNORE INTO {table} '
            #            f'(用户名,密码,学号或工号,类型) '
            #            f'VALUES (%s,%s,%s,%s)')  # 注意这里全部使用%s作为占位符
            #     values = (row.用户名, row.密码, row.学号或工号, row.类型)  # 使用属性名来访问列的值
            #     print("正在插入数据至{}:".format(table), values)  # 输出正在插入的数据
            #     mycursor.execute(sql, values)  # 执行SQL插入语句
            for row in df.itertuples(index=False):  # 遍历DataFrame中的每一行
                sql = (f'INSERT IGNORE INTO {table} '
                       f'(用户名,密码,学号或工号,类型) '
                       f'VALUES (%s,%s,%s,%s)')
                val = row  # 插入的数据
                print("正在插入数据至{}:".format(table), val)  # 输出正在插入的数据
                mycursor.execute(sql, val)  # 执行SQL插入语句
        except Exception as e:
            print("插入数据时出现错误：{}".format(e))
            print(data)
            mycursor.close()
            mydb.rollback()
            return False

        # 提交更改并关闭数据库连接
        mydb.commit()  # 提交更改
        mycursor.close()  # 关闭游标对象
        mydb.close()  # 关闭数据库连接
        return True

    def saveSingleUser(self, name,
                       stuID,
                       newPassword='123456',
                       host=host,  # 主机地址
                       user=user,  # 数据库用户名
                       password=password,  # 密码
                       database=database,  # 数据库名称
                       table=usersTable,  # 数据库表名):
                       ):
        val = [name, newPassword, stuID, 3]
        global mydb
        try:

            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.rollback()
        mycursor = mydb.cursor()
        try:
            sql = (
                f"INSERT INTO {table} "
                f"(用户名, 密码, 学号或工号, 类型) "
                f"VALUES (%s, %s, %s, %s) "
                f"ON DUPLICATE KEY UPDATE 密码=VALUES(密码)")
            print("正在插入数据至{}:".format(table), val)  # 输出正在插入的数据
            print(sql)
            mycursor.execute(sql, val)  # 执行SQL插入语句
        except Exception as e:
            print('插入数据时出现错误：{}'.format(e))
            mycursor.close()
            mydb.rollback()
        # 提交更改并关闭数据库连接
        mydb.commit()  # 提交更改
        mycursor.close()  # 关闭游标对象
        mydb.close()  # 关闭数据库连接

    # 从数据库中读取用户信息
    def getUserFromSql(self,
                       host=host,  # 主机地址
                       user=user,  # 数据库用户名
                       password=password,  # 密码
                       database=database,  # 数据库名称
                       table=usersTable  # 数据库表名
                       ):

        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            return False

        cursor = mydb.cursor(dictionary=True)

        try:
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            results = cursor.fetchall()

            df = pd.DataFrame(results)
            # print(df)

            for index, row in df.iterrows():
                flag = row['类型']
                if flag == 1:
                    user = User_Administrator(row['用户名'], row['密码'], row['学号或工号'], flag)
                elif flag == 2:
                    user = User_Teacher(row['用户名'], row['密码'], row['学号或工号'], flag)
                elif flag == 3:
                    user = User_Student(row['用户名'], row['密码'], row['学号或工号'], flag)
                else:
                    continue

                self.users.update({user.ID: user})

            self.userNum = len(self.users)

        except Exception as e:
            cursor.close()
            mydb.rollback()
            print("从数据库获取用户数据时出现错误！{}".format(e))
            return False

        if mydb.is_connected():
            cursor.close()
            mydb.close()

        return True

    def truncateUsers(self, host=host,  # 主机地址
                      user=user,  # 数据库用户名
                      password=password,  # 密码
                      database=database,  # 数据库名称
                      table=usersTable,  # 数据库表名
                      ):
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:
            sql = f"DELETE FROM {table} WHERE 类型 = 3"
            # 更新
            mycursor.execute(sql)
            mydb.commit()  # 提交更改
            # 提交更改并关闭数据库连接
        except Exception as e:
            mydb.rollback()
            raise e
        finally:
            mycursor.close()  # 关闭游标对象
            mydb.close()  # 关闭数据库连接

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
        # i = 0
        # for id in self.users.keys():
        #     i = i + 1
        #     print(i)

    # 获取成绩
    # mode==1时返回学生分析
    # mode==2时返回全班分析
    # 待完成
    def getGrades(self, mode, stuID=0):
        if mode == 1:
            for stu in gradeManager.student:
                if stu.stuID == stuID:
                    stuName = stu.name
                    gradeList = [subject.score for subject in stu.stuGrades.grades]
                    return stuName, gradeList
            return False, []
        if mode == 2:
            for stu in gradeManager.student:
                if stu.stuID == stuID:
                    stuName = stu.name
                    rankings = [stu.stuGrades.totalRanking] + [ranking for ranking in stu.stuGrades.rankings]
                    gradeList = [subject.score for subject in stu.stuGrades.grades]
                    return stuName, gradeList, rankings
            return False, [], []
        if mode == 3:
            for stu in gradeManager.student:
                if stu.stuID == stuID:
                    stuName = stu.name
                    totalGrades = [stu.stuGrades.totalScores, stu.stuGrades.totalRanking]
                    gradeList = [subject.score for subject in stu.stuGrades.grades]
                    return stuName, gradeList, totalGrades
            return False, [], []

    # mode1==0物理类mode1==1历史类
    # mode2==0总分排序
    # mode2==1语文排序
    # 以此类推
    # mode3==0 降序，分数高到低，mode3==1升序，分数低到高
    # 返回字典列表
    def getAllGrades(self, mode1, mode2, mode3):
        return gradeManager.getAllGrades(mode1, mode2, mode3)

    def changeGrades(self, stuID, subject, new_grade):
        if gradeManager.changeGrades(stuID, subject, new_grade):
            self.setRankings()
            return True
        return False

    def setRankings(self):
        # 十二种选科排序
        for physics_or_history in [3, 6]:
            for subjects in range(9):
                selected_subjects = [stu for stu in gradeManager.student if
                                     stu.stuGrades.grades[physics_or_history].score != -1 and stu.stuGrades.grades[
                                         subjects].score != -1]
                unselected_subjects = [stu for stu in gradeManager.student if
                                       stu.stuGrades.grades[physics_or_history].score == -1 or stu.stuGrades.grades[
                                           subjects].score == -1]
                selected_subjects = sorted(selected_subjects, key=lambda sub: sub.stuGrades.grades[subjects].score,
                                           reverse=True)
                is_same = 0
                for i in range(len(selected_subjects)):
                    if i >= 1 and selected_subjects[i].stuGrades.grades[subjects].score != \
                            selected_subjects[i - 1].stuGrades.grades[subjects].score:
                        is_same = i
                    selected_subjects[i].stuGrades.rankings[subjects] = is_same + 1
                gradeManager.student = selected_subjects + unselected_subjects
                # for stu in gradeManager.student:
                #     for i in range(9):
                #         print(stu.stuGrades.grades[i].score, end=' ')
                #     print(end='|')
                #     print(stu.stuGrades.totalRanking, end=' |')
                #     for i in range(9):
                #         print(stu.stuGrades.rankings[i], end=' ')
                #     print(end='|')
                #     print()
                # print('----------------------------------------------------------------')
            # 总分排序以及排名赋值
            selected_subjects = [stu for stu in gradeManager.student if
                                 stu.stuGrades.grades[physics_or_history].score != -1]
            unselected_subjects = [stu for stu in gradeManager.student if
                                   stu.stuGrades.grades[physics_or_history].score == -1]
            selected_subjects = sorted(selected_subjects, key=lambda sub: sub.stuGrades.totalScores, reverse=True)
            is_same = 0
            for i in range(len(selected_subjects)):
                if i >= 1 and selected_subjects[i].stuGrades.totalScores != \
                        selected_subjects[i - 1].stuGrades.totalScores:
                    is_same = i
                selected_subjects[i].stuGrades.totalRanking = is_same + 1

            gradeManager.student = selected_subjects + unselected_subjects
            # for stu in gradeManager.student:
            #     for i in range(9):
            #         print(stu.stuGrades.grades[i].score, end=' ')
            #     print(end='|')
            #     print(stu.stuGrades.totalRanking, end=' |')
            #     for i in range(9):
            #         print(stu.stuGrades.rankings[i], end=' ')
            #     print(end='|')
            #     print()
            # print('----------------------------------------------------------------')

    # 获得所有用户的字典列表

    def getAllUsers(self):
        data = []
        for id in self.users:
            user_data = {'姓名': self.users[id].userName,
                         '密码': self.users[id].password,
                         '学号或工号': self.users[id].ID,
                         '类型': self.users[id].flag}
            data.append(user_data)
        return data

    def getAllApplications(self):
        return gradeManager.getCheckApplicaionsTable()

    # 增加成绩审核申请表
    def addCheckApplication(self, stuName, stuID, subject):
        gradeManager.addCheckApplication(self.userName, stuName, stuID, subject)

    # 删除成绩审核申请表功能
    def deleteCheckApplication(self, index):
        stuID = gradeManager.checkApplication[index].stuID
        subject = gradeManager.checkApplication[index].subjectToCheck
        try:
            gradeManager.deleteCheckApplicationFromMySQL(stuID, subject)
            del gradeManager.checkApplication[index]
            gradeManager.saveCheckApplicationsToCSV()
        except Exception as e:
            print('删除审核表时出现错误：{}'.format(e))
            return False
        return True

    def dispAllGrades(self):
        gradeManager.dispAllGrades()

    def refreshAll(self, file_path):
        global importedGrades
        try:
            importedGrades = True
            # self.inputExcelGrades(file_path)
            # self.saveGradesToMySQL()
            print(importedGrades)
            importedGrades = formationCheckAndInputToMySQL(file_path)
            print(importedGrades)
            if importedGrades is False:
                return
            importedGrades = gradeManager.inputMySQL()
            self.setRankings()
            print(importedGrades)
            if importedGrades is False:
                return
            importedGrades = gradeManager.saveGradesToCSV()
            print(1, importedGrades)
            if importedGrades is False:
                return
            print(2, importedGrades)
            self.refreshUserInfo()
            if importedGrades is False:
                return
            print(3, importedGrades)
            importedGrades = self.saveUserInfoToMySQL()
            if importedGrades is False:
                return
            print(4, importedGrades)
            importedGrades = self.getUserFromSql()
            if importedGrades is False:
                return
            print(5, importedGrades)
            importedGrades = self.saveUserInfoToCSV()
            if importedGrades is False:
                return
        except Exception as e:
            print("出现错误", e)
            importedGrades = False

    def getImportedGrades(self):
        return importedGrades

    # 返回值：
    # 2，未选完科目就点击提交了
    # 3  学号重复
    # 4  分数越界
    # 5  导入数据库时出现错误
    # 6 导入成功
    def inputSingleGrades(self, name, ID, chinese, Math, english, sub1, sub2, sub3, grade1, grade2, grade3):
        if (sub1 in ['选科一', ''] or sub2 in ['选科一', ''] or sub3 in ['选科一', '']
                or name == '' or ID == '' or chinese == '' or Math == '' or english == ''):
            return 2
        try:
            ID = int(ID)
            chinese = int(chinese)
            Math = int(Math)
            english = int(english)
            grade1 = int(grade1)
            grade2 = int(grade2)
            grade3 = int(grade3)
        except Exception as e:
            print("格式错误{}".format(e))
            return 1
        # 注明flag变量为非本地变量
        if gradeManager.hasRepeated(ID) is False:
            return 3
        elif 0 <= chinese <= 150 and 0 <= Math <= 150 and 0 <= english <= 150 and 0 <= grade1 <= 100 and 0 <= grade2 <= 100 and 0 <= grade3 <= 100:
            gradesDict = {'语文': chinese, '数学': Math, '英语': english, sub1: grade1, sub2: grade2, sub3: grade3}
            temp = gradeManager.inputGrades(1, name, ID, gradesDict)
            if temp == 6:
                try:
                    self.setRankings()
                    self.refreshUserInfo()
                    self.saveUserInfoToCSV()
                    self.saveSingleUser(name, ID)
                except:
                    return 5
            return temp
        else:
            return 4

    def inputExcelGrades(self, path):
        gradeManager.inputGrades(2, path)

    def saveGradesToMySQL(self):
        gradeManager.saveGradesToMySQL()

    def saveGradesToCSV(self):
        gradeManager.saveGradesToCSV()

    def resetGrades(self):
        try:
            gradeManager.truncateGrades()
            gradeManager.truncateCheckApplication()
            self.truncateUsers()
        except Exception as e:
            print(e)
            return False
        return True


accountManager = AccountManager()
# accountManager.resetGrades()
gradeManager.getApplicationFromSql()
gradeManager.inputMySQL()
# accountManager.getAllGrades(1,0,0)

if __name__ == "__main__":
    print(accountManager.getAllUsers())
    print(accountManager.getAllApplications())
    # gradeManager = GradeManager([], 0, [])
    # gradeManager.inputCSV("./student.csv")
    # for x in gradeManager.student:
    #     print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)
    # accountManager = AccountManager()
    while True:
        print('管理员账号：user1，密码：111111')
        print("请输入选项：1、登录，2、注册（仅限管理员和教师），3、退出系统：")
        try:
            op = eval(input())
        except Exception as e:
            print("非法输入!", e)
            continue

        # 错误处理
        if op not in [1, 2, 3]:
            print("非法输入!\n请重试!")
            continue

        if op == 1:
            print('请输入账号：')
            account = input()
            print('请输入密码：')
            password = input()
            if accountManager.login(account, password, 1) is False:
                continue

        elif op == 2:
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

        elif op == 3:
            break

        if accountManager.flag == 1:
            print('登录成功')
            while True:
                print(
                    '请输入选项：\n1、查看成绩\n2、修改账号名称\n3、修改密码\n4、导入学生账号\n5、查看成绩修改申请单\n'
                    '6、输出当前账号信息\n7、输出所有账号信息\n8、查看所有学生成绩\n9、查看成绩复核申请表\n10、保存成绩信息至数据库\n'
                    '11、保存用户信息至数据库\n12、保存成绩审核申请表至数据库\n13、退出至登录界面')

                op = eval(input())
                if op <= 0 or op > 13:
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
                    accountManager.printCheckApplication()
                    print('按enter继续……')
                    input()

                if op == 10:
                    gradeManager.saveGradesToMySQL()
                    print('按enter继续……')
                    input()

                if op == 11:
                    accountManager.saveUserInfoToMySQL()
                    print('按enter继续……')
                    input()

                if op == 12:
                    gradeManager.saveCheckApplicationsToMySQL()
                    print('按enter继续……')
                    input()

                if op == 13:
                    accountManager.logout()
                    accountManager.saveUserInfoToCSV()
                    break

# accountManager.inputUsers("./users.csv")
# accountManager.login('user1', 111111)
# accountManager.printUserInfo()
# accountManager.refreshUserInfo()
# accountManager.printUserInfo()
# accountManager.saveUserInfo()
