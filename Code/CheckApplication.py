'''
2024/7/5
    class CheckApplication
        __init__()
        printCheckApplication()
by  沈智恺
'''
class CheckApplication:
#教师姓名，学生姓名，学号，学科
    def __init__(self, teacherName, stuName, stuID, subject):
        self.teacherName = teacherName
        self.stuName = stuName
        self.stuID = stuID
        self.subjectToCheck = subject

    #打印申请表
    def printCheckApplication(self):
        print('申请老师姓名：' + self.teacherName + '被申请学生姓名：' + self.stuName + ' 学生学号：' + str(
            self.stuID) + ' 请求复核的学科：' + self.subjectToCheck + '\n')

#测试用例
if __name__ == '__main__':
    People = CheckApplication('lf','szk', '2023302112035', '物理')
    print(People.printCheckApplication())