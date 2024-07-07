'''
7.7
class User_Student
by 刘链凯
'''
import User
import GradeManager
class User_Student(User):
    def __init__(self, userName, passWord, ID):
        super().__init__(userName, passWord, ID)
    def getSingleGrades(self, name, stuID, sub, grade)->bool:
        gradeManager = GradeManager.GradeManager(self.userName, self.ID, [])
        return gradeManager.inputSingle(name, stuID, grade)
    def GradesCheck(self, name, stuID, subject)->bool:
        gradeManager = GradeManager.GradeManager(self.userName, self.ID, [])
        return gradeManager.inputGrades(1, name, stuID, subject)

























