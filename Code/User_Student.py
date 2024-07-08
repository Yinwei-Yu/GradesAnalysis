'''
7.7
class User_Student
by 刘链凯
'''
import User
import GradeManager
import Grades
import Student
import AccountManager
import CheckApplication
class User_Student(User):
    def __init__(self, userName, passWord, ID):
        super().__init__(userName, passWord, ID)
    def getSingleGrades(self)->bool:
       pass



    def GradesCheck(self,subject)->bool:
        stu=CheckApplication.CheckApplication(self.userName,self.ID,subject)
        list[CheckApplication].append(stu)

























