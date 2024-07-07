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
    def getSingleGrades(self, name, stuID, sub, grade):
        return self.gradeManager.inputSingle(name, stuID, grade)
    def getAllGrades(self, mode, *args):
        return self.gradeManager.inputGrades(mode, *args)
    def GradesCheck(self, name, stuID, subject):
        return self.gradeManager.checkGrades(name, stuID, subject)