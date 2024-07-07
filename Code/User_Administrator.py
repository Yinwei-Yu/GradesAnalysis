'''
7.7
User_Administrator
by 刘链凯
'''
import User
import GradeManager
class User_Administrator(User):
    def __init__(self, userName, passWord, ID):
        super().__init__(userName, passWord, ID)
    def getSingleGrades(self):
        return self.gradeManager.getGrades(1)
    def getAllGrades(self):
        return self.gradeManager.getGrades(2)
    def changeGrades(self, name, stuID, sub, grade):
        self.gradeManager.changeGrades(name, stuID, sub, grade)