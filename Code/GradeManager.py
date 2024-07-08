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
import pandas as pd


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
        self.stuNum += 1
        return

    # 从csv文件导入
    # path:文件路径，需要为csv格式文件，excel自带保存为csv格式功能
    def inputCSV(self, path):
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            grades = gr.Grades(
                Chinese(row['语文']), Math(row['数学']), English(row['英语']),
                Physics(row['物理']), Chemistry(row['化学']), Biology(row['生物']),
                History(row['历史']), Politics(row['政治']), Geography(row['地理'])
            )
            stuTemp = stu.Student(row['姓名'], row['学号'], grades)
            self.student.append(stuTemp)
        self.stuNum = len(self.student)
        return

    # 导入学生成绩 mode==1单个导入，arg接收学生姓名学号和成绩信息
    # mode==2时接受文件路径
    def inputGrades(self, mode, *args):
        if mode == 1:
            self.inputSingle(*args)
        elif mode == 2:
            self.inputCSV(*args)
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

    '''
    单科排名的包装函数
    num接收科目参数：语文0，数学1，英语2，物理3，化学4，生物5，历史6，政治7，地理8
    isReverse接收大小关系，True从大到小，False从小到大
    '''
    def subRanking(self, num, isReverse):
        if num < 0 or num > 8:
            print("科目不存在！")
            return []
        tempStuList = sorted(self.student, key=lambda sub: sub.stuGrades.grades[num].score, reverse=isReverse)
        return tempStuList


    '''
    计算单科排名
    subject接收科目名
    mode==1时从大到小 mode==2时从小到大
    成功返回一个存储排序结果的列表，原有的student列表中内容顺序不变
    失败返回一个空列表
    '''
    def calculateRanking(self, subject, mode):
        if mode != 1 and mode != 2:
            print("请选择正确的排序方式!")
            return []

        # 根据 mode 设置 isReverse 值
        isReverse = (mode == 1)

        # 主要处理
        if subject in ["Chinese", "chinese", "语文"]:
            return self.subRanking(0, isReverse)
        elif subject in ["Math", "math", "数学"]:
            return self.subRanking(1, isReverse)
        elif subject in ["English", "english", "英语"]:
            return self.subRanking(2, isReverse)
        elif subject in ["Physics", "physics", "物理"]:
            return self.subRanking(3, isReverse)
        elif subject in ["Chemistry", "chemistry", "化学"]:
            return self.subRanking(4, isReverse)
        elif subject in ["Biology", "biology", "生物"]:
            return self.subRanking(5, isReverse)
        elif subject in ["History", "history", "历史"]:
            return self.subRanking(6, isReverse)
        elif subject in ["Politics", "politics", "政治"]:
            return self.subRanking(7, isReverse)
        elif subject in ["Geography", "geography", "地理"]:
            return self.subRanking(8, isReverse)
        else:
            print("请输入正确的科目名！")
            return []

    '''
    # 成绩分析
    # mode==1:直方图
    # mode==2:折线分析图
    '''
    def generateGradesAnalysis(self, mode):
        pass


# gradeManager=GradeManager()
# 测试函数
if __name__ == '__main__':
    '''
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
   '''

    # 测试从csv文件导入

    manager = GradeManager([], 0, [])
    manager.inputGrades(2, r"C:\\Users\\32284\Desktop\Grades\GradesAnalysis\Code\student.csv")
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.totalGrades)
    '''
    manager.sortGrades()
    print("排序后：")
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.totalGrades)
    '''
    print("按语文排名前：")
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.grades[0].score)

    templist = manager.calculateRanking("chinese", 0)

    print("按语文排名后：")
    for x in templist:
        print(x.name, " ", x.stuID, " ", x.stuGrades.grades[0].score)
