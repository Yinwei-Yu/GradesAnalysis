'''

2024/7/5
class GradeManager

GradeManager:class
__init__()
inputSingle()
inputGrades()
renewTotalGrade()
changeGrade()

by 李胤玮

'''

import Student as stu
import CheckApplication
import Grades as gr
from Subject import *


class GradeManager:

    # student：存储学生数据的列表，元素类型是Student；
    # stuNum 整形，记录学生总数；
    # checkApplication 列表，元素类型是CheckApplication

    def __init__(self, student: list[stu], stuNum: int, checkApplication: list[CheckApplication]):
        self.student = student
        self.stuNum = stuNum
        self.checkApplication = checkApplication

    # name:str
    # stuID:int
    # grades:Grades
    # 实现从输入导入
    def inputSingle(self, name, stuID, grade):
        self.student.append(stu.Student(name, stuID, grade))

    # 导入学生成绩 mode==1单个导入，arg接收学生姓名学号和成绩信息
    # mode==2时接受文件路径
    def inputGrades(self, mode, *args):
        if mode == 1:
            self.inputSingle(*args)
        elif mode == 2:
            pass
        return

    # 修改成绩后用于修改总成绩
    def renewTotalGrade(self, num):
        self.student[num].stuGrades.totalGrades = (
                self.student[num].stuGrades.grades[0].score +
                self.student[num].stuGrades.grades[1].score +
                self.student[num].stuGrades.grades[2].score +
                self.student[num].stuGrades.grades[3].score +
                self.student[num].stuGrades.grades[4].score +
                self.student[num].stuGrades.grades[5].score +
                self.student[num].stuGrades.grades[6].score +
                self.student[num].stuGrades.grades[7].score +
                self.student[num].stuGrades.grades[8].score
        )

    # 修改学生成绩，修改成功返回True，否则返回False
    # name：学生姓名 stuID：学生学号 sub:学科名，英文全称 grade:修改后的分数
    def changeGrades(self, name, stuID, sub, grade):
        for i in range(len(self.student)):
            if self.student[i].stuID == stuID:
                if sub == "Chinese":
                    self.student[i].stuGrades.grades[0].score = grade
                elif sub == "Math":
                    self.student[i].stuGrades.math.score = grade
                elif sub == "English":
                    self.student[i].stuGrades.english.score = grade
                elif sub == "Physics":
                    self.student[i].stuGrades.physics.score = grade
                elif sub == "Chemistry":
                    self.student[i].stuGrades.chemistry.score = grade
                elif sub == "Biology":
                    self.student[i].stuGrades.biology.score = grade
                elif sub == "History":
                    self.student[i].stuGrades.history.score = grade
                elif sub == "Geography":
                    self.student[i].stuGrades.geography.score = grade
                elif sub == "Politics":
                    self.student[i].stuGrades.politics.score = grade
                self.renewTotalGrade(i)
            return True
        return False

    # 对学生按照总成绩进行排名
    # 成功返回True，否则返回False
    def sortGrades(self):
        try:
            self.student.sort(key=lambda s: s.stuGrades.totalGrades, reverse=True)
            return True
        except Exception as e:
            print(f"排序时出现错误: {e}")
            return False

    # 计算单科排名
    # 成功返回True，否则返回False
    def calculateRanking(self):
        pass


# 测试函数
if __name__ == '__main__':
    grade1 = gr.Grades(Chinese(120), Math(150), English(145), Physics(100), Chemistry(100), Biology(100), History(0),
                       Politics(0), Geography(0))
    grade2 = gr.Grades(Chinese(150), Math(100), English(149), Physics(0), Chemistry(0), Biology(0), History(100),
                       Politics(100), Geography(100))
    stu1 = stu.Student("张三", 1, grade1)
    stu2 = stu.Student("袁华", 2, grade2)
    stus = [stu1, stu2]
    manager = GradeManager(stus, 2, [])
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.totalGrades)
    grade3 = gr.Grades(Chinese(139), Math(100), English(149),
                       Physics(0), Chemistry(0), Biology(0), History(100), Politics(100), Geography(100))
    manager.inputGrades(1, "夏洛", 3, grade3)
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.totalGrades)  # 测试添加功能
    print("张三：", manager.student[0].stuGrades.grades[0].score)
    manager.changeGrades("张三", 1, "Chinese", 1)
    print("张三：", manager.student[0].stuGrades.grades[0].score)
    print("排序前:")
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.totalGrades)  # 测试修改功能
    manager.sortGrades()
    print("排序后：")
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.totalGrades)  # 测试排序功能
