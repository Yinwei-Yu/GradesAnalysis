class CheckApplication:

    def __init__(self, teacherName, stuName, stuID, subject):
        self.teacherName = teacherName
        self.stuName = stuName
        self.stuID = stuID
        self.subjectToCheck = subject

    def printCheckApplication(self):
        print('申请老师姓名：' + self.teacherName + '被申请学生姓名：' + self.stuName + ' 学生学号：' + str(
            self.stuID) + ' 请求复核的学科：' + self.subjectToCheck + '\n')


if __name__ == '__main__':
    People = CheckApplication('szk', '2023302112035', '物理')
    print(People.createCheckApplication())

