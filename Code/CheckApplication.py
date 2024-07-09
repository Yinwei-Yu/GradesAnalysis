class CheckApplication:
<<<<<<< Updated upstream
    def __init__(self, teacherName, stuName, stuID, subject):
        self.teacherName = teacherName
=======
    def __init__(self, applicationReviewer, stuName, stuID, subject):
        self.applicationReviewer = applicationReviewer
>>>>>>> Stashed changes
        self.stuName = stuName
        self.stuID = stuID
        self.subjectToCheck = subject

    def createCheckApplication(self):
<<<<<<< Updated upstream
        return '申请老师姓名：' + self.teacherName + '被申请学生姓名：' + self.Name + ' 学生学号：' + self.StuID + ' 请求复核的学科：' + self.SubjectToCheck + '\n'
=======
        return '姓名：' + self.stuName + ' 学号：' + self.stuID + ' 请求复核的学科：' + self.subjectToCheck + '\n'
>>>>>>> Stashed changes


if __name__ == '__main__':
    People = CheckApplication('szk', '2023302112035', '物理')
    print(People.createCheckApplication())
