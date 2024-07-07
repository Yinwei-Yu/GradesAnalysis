'''
7.7
class User_Student
by 刘链凯
'''
import GradeManager
from User import User
class User_Student(User):
    def __init__(self, userName, passWord, ID):
        super().__init__(userName, passWord, ID)
    def getSingleGrades(self)->list:
        gradeManager = GradeManager.GradeManager(self.userName, self.ID, []);
        return gradeManager.getSingleGrades();
    def GradesCheck(self, name, stuID, subject)->bool:
        gradeManager = GradeManager.GradeManager(self.userName, self.ID, []);
        return gradeManager.GradesCheck(name, stuID, subject);

























