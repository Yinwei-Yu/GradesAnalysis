class CheckApplication:
    def __init__(self, name, idc, subject):
        self.Name = name
        self.StuID = idc
        self.SubjectToCheck = subject
    def createCheckApplication(self):
        return '姓名：' + self.Name + ' 学号：' + self.StuID + ' 请求复核的学科：' + self.SubjectToCheck+'\n'
People = CheckApplication('szk', '2023302112035', '物理')
print(People.createCheckApplication())