'''

2024/7/7
class Student

Student:class
__init__()
generateGrades()

by 廖雨龙

'''

from Grades import Grades
from Subject import *

class Student:
    #name : 学生姓名 类型 string
    #stuID: 学生学号 类型 int
    #stuGrades: 学生成绩 类型 Grades
    def __init__(self, name: str, stuID: int, stuGrades: Grades):
        self.name = name
        self.stuID = stuID
        self.stuGrades = stuGrades

    #ranking : 总排名 类型 int
    #rankings: 六科排名 类型 int[]
    #gradeAnalysis: 成绩分析 类型 str
    #函数功能: 生成学生成绩
    def generateGrades(self, ranking: int, rankings: list[int], gradeAnalysis: str) -> bool:
        self.stuGrades.setRanking(ranking)
        self.stuGrades.gradesAnalysis = gradeAnalysis
        self.stuGrades.generateGradesAnalysis()
        return True

# 测试函数
if __name__ == '__main__':
    # 创建 Subject 类的实例
    class Subject:
        def __init__(self, score: int):
            self.score = score

    # 创建 Grades 类的实例
    chinese = Chinese(score=90)
    math = Math(score=95)
    english = English(score=85)
    physics = Physics(score=88)
    chemistry = Chemistry(score=92)
    biology = Biology(score=89)
    history = History(score=87)
    politics = Politics(score=90)
    geography = Geography(score=91)

    grades = Grades(chinese, math, english, physics, chemistry, biology, history, politics, geography)

    # 创建 Student 类的实例
    student = Student(stuID= 1, name="John Doe", stuGrades=grades)

    # 调用 generate_grades 方法
    student.generateGrades(ranking=1,rankings=[1,2,3,4,5,6,7,8,9], gradeAnalysis="Excellent")

    # 调用 generate_grades_analysis 方法
    student.stuGrades.generateGradesAnalysis()



