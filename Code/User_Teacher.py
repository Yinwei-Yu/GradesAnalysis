'''
7.7
class User_Teacher
by 刘链凯
'''
import User
import GradeManager
import CheckApplication

class User_Teacher(User):
    def __init__(self, userName, passWord, ID):
        super().__init__(userName, passWord, ID)
    def getSingleGrades(self, stuID):
        pass

    def GradesCheck(self, subject) -> bool:
        stu = CheckApplication.CheckApplication(self.userName, self.ID, subject)
        list[CheckApplication].append(stu)



