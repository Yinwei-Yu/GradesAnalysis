'''
2024/7/5
GradeManager：

1. __init__(self, student: list[stu], stuNum: int, checkApplication: list[CheckApplication])
   - student:包含学生信息的列表，可以传入空列表[]
   - stuNum：传入初始值为0
   - checkApplication：接收申请修改成绩的列表，初始值为空列表
2. inputExcelGrades(self, mode, *args)
   - 输入成绩
   - mode：
     - mode==1时传入单个学生成绩
       - args请提供三个参数：
         - name：学生姓名
         - stuID：学生学号
         - grade：类型为Grades的学生成绩
     - mode==2时传入文件路径，文件需要为excel或者csv文件格式

3. changeGrades(self,name,stuID,sub,grade)
   - name:学生姓名
   - stuID：学生学号
   - sub：需要修改的科目，为学科英文名，首字母大写
   - grade：对应科目需要修改为的分数
4. sortGrades（self）
   - 按照总成绩进行排序
   - 会修改student列表
   - 成功返回True 失败返回False
5. caculateRanking(self,subject,mode)
   - 按照单科排名
   - 不会修改student列表顺序
   - 返回一个存储排序结果的新列表，失败返回空列表
   - subject：学科名，接受对应学科英文名（首字母大小写均可），中文名
   - mode：排序模式，mode==1从大到小，mode==2从小到大
6. generateGradesAnalysis(self,mode,*subOrway)
   - 产生成绩分析图表
   - mode==1生成总成绩，subOrway接受学科名，需为对应学科英文名，首字母大写
   - mode==2生成折线图，subOrway接受1或2
     - subOrway==1时产生语数英物化生线性关系图
     - subOrway==2时产生语数英史政地线性关系图

by 李胤玮

2024/7/9
GradeManager：
    inputCheckApplications() //根据csv文件导入成绩复核申请表
    addCheckApplication()//老师可以进行成绩复核申请
    saveCheckApplication()//保存成绩申请到csv文件中

2024/7/10
GradeManager
    创建了inputMySQL() (未实现)
    getGradesTable() //将学生成绩列表转换为字典列表类型
    修改了saveGradesToCSV()
    saveGradesToMySQL()//将学生成绩存储到数据库

by陈邱华

2024/7/11
GradeManager
   补充了inputMysQL()
   by 刘链凯

2024/7/12
GradeManager
    添加从数据库中读取checkApplication功能
    getAppliFromSql()
by 李胤玮

2024/7/14
GradeManager
    getAllGrades()
by陈邱华

2024/7/15
GradeManager
    修改了inputSingle()
by陈邱华

2024/7/17
GradeManager
    deleteCheckApplicationFromMySQL()
by陈邱华

2024/7/18
GradeManager
   TruncateGrades()
   TruncateCheckApplication()
by陈邱华
'''

import os

import mysql.connector  # pip install mysql-connector-python
import pandas as pd  # 导入pandas库，用于读取Excel文件和处理数据
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import statistics


import CheckApplication
import Grades as gr
import Student as stu
from MySQLInfo import *
from Subject import *


class GradeManager:

    # student：存储学生数据的列表，元素类型是Student；
    # stuNum 整型，记录学生总数；
    # checkApplication 列表，元素类型是CheckApplication

    def __init__(self, student: list[stu], stuNum: int, checkApplication: list[CheckApplication],
                 checkApplicationNum: int):

        self.student: list[stu] = student
        self.stuNum = stuNum
        self.checkApplication = checkApplication
        self.checkApplicationNum = checkApplicationNum

    # name:str
    # stuID:int
    # grades:Grades
    # 实现从输入导入
    def saveSingleGrades(self, name,
                         stuID,
                         gradeDict,
                         host=host,  # 主机地址
                         user=user,  # 数据库用户名
                         password=password,  # 密码
                         database=database,  # 数据库名称
                         table=rankedGradesTable,  # 数据库表名

                         ):
        # 将数据转换为 DataFrame
        val = [name, stuID, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0]
        ind = {'语文': 2, '数学': 3, '英语': 4, '物理': 5, '化学': 6, '生物': 7, '历史': 8, '政治': 9, '地理': 10}
        for key in gradeDict:
            val[ind[key]] = gradeDict[key]
        print(val)
        # 将dataframe保存至数据库
        for i in range(2, 11):
            val[11] += val[i] if val[i] != -1 else 0
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.rollback()

        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:
            sql = (f"INSERT IGNORE INTO {table} "
                   f"(姓名,学号,语文,数学,英语,物理,化学,生物,历史,政治,地理,总分) "
                   f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            print("正在插入数据至{}:".format(table), val)  # 输出正在插入的数据
            mycursor.execute(sql, val)  # 执行SQL插入语句
        except Exception as e:
            print('插入数据时出现错误：{}'.format(e))
            mycursor.close()
            mydb.rollback()
            return 5
        # 提交更改并关闭数据库连接
        mydb.commit()  # 提交更改
        mycursor.close()  # 关闭游标对象
        mydb.close()  # 关闭数据库连接
        self.student.append(stu.Student(name, stuID,
                                        gr.Grades(Chinese(val[2]), Math(val[3]), English(val[4]), Physics(val[5]),
                                                  Chemistry(val[6]), Biology(val[7]), History(val[8]), Politics(val[9]),
                                                  Geography(val[10]))))
        self.sortGrades()
        self.saveGradesToCSV()

        self.stuNum += 1
        return 6

    # 将传入的excel文件转换为csv文件
    def excelToCsv(self, excelFilePath, sheetName, csvFilePath):
        # 读取excel文件
        df = pd.read_excel(excelFilePath)
        # 将数据保存为csv文件
        df.to_csv(csvFilePath)
        return True

    # 从csv文件导入
    # path:文件路径，需要为csv格式文件，excel自带保存为csv格式功能
    def inputCSV(self, path):
        if not path:
            print("文件不存在！")
            return False
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            grades = gr.Grades(
                Chinese(int(row['语文'])), Math(int(row['数学'])), English(int(row['英语'])),
                Physics(int(row['物理'])), Chemistry(int(row['化学'])), Biology(int(row['生物'])),
                History(int(row['历史'])), Politics(int(row['政治'])), Geography(int(row['地理']))
            )
            stuTemp = stu.Student(row['姓名'], row['学号'], grades)
            self.student.append(stuTemp)
        self.stuNum = len(self.student)

        return
    # 批量导入函数
    def inputMore(self, path, sheetName=None, outputPath=None):
        fileExtension = os.path.splitext(path)[1].lower()
        csvFilePath = r"tempPath.csv"
        # 如果是excel文件
        if fileExtension in ['.xls', '.xlsx']:
            # 转化为csv文件
            self.excelToCsv(path, sheetName, csvFilePath)
            self.inputCSV(csvFilePath)
            try:
                os.remove("tempPath.csv")
            except FileNotFoundError:
                print(f"文件不存在\n\n")
        elif fileExtension == '.csv':
            self.inputCSV(path)
        else:
            print("请导入excel文件或者csv文件！")

    # 待实现
    def inputMySQL(self,
                   host=host,  # 主机地址
                   user=user,  # 数据库用户名
                   password=password,  # 密码
                   database=database,  # 数据库名称
                   table=rankedGradesTable,  # 数据库表名
                   ):
        self.student.clear()
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)

        # 创建游标
        cursor = mydb.cursor(dictionary=True)
        try:
            # 执行SQL查询语句
            query = f"SELECT * FROM {table} ORDER BY 总分 DESC "
            cursor.execute(query)
            # 获取所有记录列表
            results = cursor.fetchall()
            # 将结果转换为DataFrame
            df = pd.DataFrame(results)
            for index, row in df.iterrows():
                grades = gr.Grades(
                    Chinese(row['语文']), Math(row['数学']), English(row['英语']),
                    Physics(row['物理']), Chemistry(row['化学']), Biology(row['生物']),
                    History(row['历史']), Politics(row['政治']), Geography(row['地理'])
                )
                stuTemp = stu.Student(row['姓名'], row['学号'], grades)
                self.student.append(stuTemp)
            self.stuNum = len(self.student)
        except Exception as e:
            cursor.close()
            mydb.rollback()
            print("从数据库获取成绩信息时出现错误:{}".format(e))
            return False

        if mydb.is_connected():
            cursor.close()
            mydb.close()
        return True

    # 导入学生成绩 mode==1单个导入，arg接收学生姓名学号和成绩信息
    # mode==2时接受文件路径
    # mode==3时通过sql数据库导入
    def inputGrades(self, mode, *args):
        if mode == 1:
            return self.saveSingleGrades(*args)
        elif mode == 2:
            self.inputMore(*args)
        elif mode == 3:
            self.inputMySQL(*args)
        else:
            print("非法的导入模式！")
            return False
        return

    def inputCheckApplications(self, path):
        df = pd.read_csv(path)
        for index, row in df.iterrows():
            check_application = CheckApplication.CheckApplication(row['申请老师'], row['被申请学生姓名'],
                                                                  row['学生学号'],
                                                                  row['申请科目'])
            self.checkApplication.append(check_application)
        self.checkApplicationNum = len(self.checkApplication)
        return

    def addCheckApplication(self, teacherName, stuName, stuID, subject):

        for stu in self.student:
            if stu.name == stuName and stu.stuID == stuID:
                check_application = CheckApplication.CheckApplication(teacherName, stuName, stuID, subject)
                self.checkApplication.append(check_application)
                self.checkApplicationNum = len(self.checkApplication)
                # print(self.checkApplicationNum)
                self.saveCheckApplicationsToMySQL()
                return True

        return False

    # 从数据库删除成绩审核申请表功能
    def deleteCheckApplicationFromMySQL(self, stuID, subject,
                                        host=host,  # 主机地址
                                        user=user,  # 数据库用户名
                                        password=password,  # 密码
                                        database=database,  # 数据库名称
                                        table=checkApplicationsTable,  # 数据库表名
                                        ):

        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:
            sqlUpdate = f"""DELETE FROM {table} WHERE `学生学号` = %s AND `申请科目` = %s"""
            data = (stuID, subject)
            # 更新
            mycursor.execute(sqlUpdate, data)
            mydb.commit()  # 提交更改
            # 提交更改并关闭数据库连接
        except Exception as e:
            mydb.rollback()
            raise e
        finally:
            mycursor.close()  # 关闭游标对象
            mydb.close()  # 关闭数据库连接

    # 修改成绩后用于修改总成绩
    def renewTotalGrade(self, num):
        self.student[num].stuGrades.totalScores = 0
        for i in range(9):
            score = self.student[num].stuGrades.grades[i].score
            self.student[num].stuGrades.totalScores += self.student[num].stuGrades.grades[i].score if score != -1 else 0

    # 修改学生成绩，修改成功返回True，否则返回False
    # name：学生姓名 stuID：学生学号 sub:学科名，英文全称 grade:修改后的分数
    def changeGrades(self, stuID, subject, new_grade):
        print(stuID, subject, new_grade)
        for i in range(len(self.student)):
            if self.student[i].stuID == stuID:
                if subject == "语文":
                    self.student[i].stuGrades.grades[0].score = new_grade
                elif subject == "数学":
                    self.student[i].stuGrades.grades[1].score = new_grade
                elif subject == "英语":
                    self.student[i].stuGrades.grades[2].score = new_grade
                elif subject == "物理":
                    self.student[i].stuGrades.grades[3].score = new_grade
                elif subject == "化学":
                    self.student[i].stuGrades.grades[4].score = new_grade
                elif subject == "生物":
                    self.student[i].stuGrades.grades[5].score = new_grade
                elif subject == "历史":
                    self.student[i].stuGrades.grades[6].score = new_grade
                elif subject == "政治":
                    self.student[i].stuGrades.grades[7].score = new_grade
                elif subject == "地理":
                    self.student[i].stuGrades.grades[8].score = new_grade
                try:
                    self.renewTotalGrade(i)
                    self.updateGradesToMySQL(stuID, subject, new_grade)
                    self.saveGradesToCSV()
                except Exception as e:
                    print('更新数据时出现异常：{}'.format(e))
                    return False
                return True
        return False

    # 对学生按照总成绩进行排名
    # 成功返回True，否则返回False
    def sortGrades(self):
        try:
            self.student.sort(key=lambda s: s.stuGrades.totalScores, reverse=True)
            for i in range(len(self.student)):
                self.student[i].stuGrades.totalRanking = i + 1
            self.saveGradesToCSV()
            # self.saveGradesToMySQL()
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

    # 检测学号是否重复
    def hasRepeated(self, ID):
        for stu in self.student:
            if stu.stuID == ID:
                return False
        return True

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
    直方图分析
    subject接收需要分析的科目
    '''

    def plotHistograms(self, subjectName: str):


        # 设置支持中文显示的字体
        rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
        rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号显示问题

        subjects = ['语文', '数学', '英语', '物理', '化学', '生物', '历史', '政治', '地理']

        if subjectName not in subjects:
            print(f"学科：{subjectName}不存在！")
            return

        scores = {subject: [] for subject in subjects}

        # Collect scores for each subject
        for student in self.student:
            for i, subject in enumerate(subjects):
                if student.stuGrades.grades[i].score != -1:
                    scores[subject].append(student.stuGrades.grades[i].score)

        if not scores[subjectName]:
            print(f"学科：{subjectName}没有成绩数据！")
            return

        # Calculate statistics
        subject_scores = scores[subjectName]
        mean_score = np.mean(subject_scores)
        max_score = np.max(subject_scores)
        min_score = np.min(subject_scores)
        mode_score = statistics.mode(subject_scores)
        median_score = np.median(subject_scores)

        # Plot the histogram
        plt.figure(figsize=(10, 6))
        plt.hist(subject_scores, bins=10, edgecolor='black')

        # 中位数线
        plt.axvline(median_score, color='red', linestyle='-', linewidth=1, label='中位数')
        # 平均数线
        plt.axvline(mean_score, color='green', linestyle='-', linewidth=1, label='平均数')

        # Add text for statistics
        stats_text = (f'平均数: {mean_score:.2f}\n'
                      f'最高分: {max_score}\n'
                      f'最低分: {min_score}\n'
                      f'众数: {mode_score}\n'
                      f'中位数: {median_score}')
        plt.text(0.05, 0.7, stats_text, fontsize=12, verticalalignment='center', horizontalalignment='left',
                 transform=plt.gca().transAxes, bbox=dict(facecolor='white', alpha=0.7))

        plt.title(f'{subjectName} 成绩分布')
        plt.xlabel('成绩')
        plt.ylabel('学生人数')
        plt.grid(False)
        plt.legend()
        plt.show()

    '''
    折线图分析，接收一个参数way
    way==1时产生语数英和物化生的折线图
    way==2时产生语数英和史政地的折线图
    '''

    def plotLineCharts(self, way):

        # 设置支持中文显示的字体
        rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
        rcParams['axes.unicode_minus'] = False  # 解决坐标轴负号显示问题

        total_scores_chinese_math_english = []
        total_scores_physics_chemistry_biology = []
        total_scores_history_politics_geography = []

        # 将学生的每三科总分分别存储
        # 只计算物化生选科和史政地选科
        for student in self.student:
            total_cme = (student.stuGrades.grades[0].score + student.stuGrades.grades[1].score +
                         student.stuGrades.grades[2].score)
            total_pcb=0
            if all(grade.score !=-1 for grade in student.stuGrades.grades[3:6]):
                total_pcb = (student.stuGrades.grades[3].score + student.stuGrades.grades[4].score +
                         student.stuGrades.grades[5].score)
            total_hpg=0
            if all(grade.score !=-1 for grade in student.stuGrades.grades[6:9]):
                total_hpg = (student.stuGrades.grades[6].score + student.stuGrades.grades[7].score +
                         student.stuGrades.grades[8].score)

            # 保证两个数据长度一样，排除为0的数据
            if way == 1:
                if total_pcb != 0:
                    total_scores_physics_chemistry_biology.append(total_pcb)
                    total_scores_chinese_math_english.append(total_cme)

            elif way == 2:
                if total_hpg != 0:
                    total_scores_history_politics_geography.append(total_hpg)
                    total_scores_chinese_math_english.append(total_cme)

        # 将数据转换为numpy数组
        if way == 1:
            x = np.array(total_scores_physics_chemistry_biology)
        if way == 2:
            x = np.array(total_scores_history_politics_geography)
        y = np.array(total_scores_chinese_math_english)

        # 计算线性回归
        coefficients = np.polyfit(x, y, 1)
        poly = np.poly1d(coefficients)
        y_fit = poly(x)

        # 绘制散点图和拟合线
        plt.figure(figsize=(10, 6))
        plt.scatter(x, y, marker='o', label='数据点')
        plt.plot(x, y_fit, color='red', label='拟合线')

        # 添加线性回归系数文本注释
        slope = coefficients[0]
        intercept = coefficients[1]
        plt.text(0.05, 0.8, f'回归方程: y = {slope:.2f}x + {intercept:.2f}', transform=plt.gca().transAxes,
                 fontsize=12, verticalalignment='top')

        plt.title('物化生与语数英总分线性拟合' if way == 1 else '史政地与语数英总分线性拟合')
        plt.xlabel('物化生总分' if way == 1 else '史政地总分')
        plt.ylabel('语数英总分')
        plt.legend()
        plt.grid(True)
        plt.show()

    '''
    # 成绩分析
    # mode==1:直方图
    # mode==2:折线分析图
    '''

    def generateGradesAnalysis(self, mode, *subOrway):
        if mode == 1:
            self.plotHistograms(*subOrway)
        elif mode == 2:
            self.plotLineCharts(*subOrway)
        else:
            print("分析模式不存在！")
            return False

    def dispAllGrades(self):
        for stu in self.student:
            print(f"姓名:{stu.name},学号:{stu.stuID}")
            stu.stuGrades.displayGradesAnalysis()

    # 获取dict类型学生成绩表格
    def getGradesTable(self, mode, sortedStudent) -> list:
        # 创建一个字典列表存储每个学生的数据
        data = []
        if mode == 1:
            for student in sortedStudent:
                # 创建一个字典存储单个学生的信息
                student_data = {
                    '姓名': student.name,
                    '学号': student.stuID,
                    '语文': student.stuGrades.grades[0].score,
                    '数学': student.stuGrades.grades[1].score,
                    '英语': student.stuGrades.grades[2].score,
                    '物理': student.stuGrades.grades[3].score,
                    '化学': student.stuGrades.grades[4].score,
                    '生物': student.stuGrades.grades[5].score,
                    '历史': student.stuGrades.grades[6].score,
                    '政治': student.stuGrades.grades[7].score,
                    '地理': student.stuGrades.grades[8].score,
                    '总分': student.stuGrades.totalScores
                }
                # 将这个学生的信息字典添加到数据列表中
                data.append(student_data)
        if mode == 2:
            for student in sortedStudent:
                # 创建一个字典存储单个学生的信息
                student_data = {
                    '姓名': student.name,
                    '学号': student.stuID,
                    '语文': student.stuGrades.grades[0].score,
                    '语文排名': student.stuGrades.rankings[0],
                    '数学': student.stuGrades.grades[1].score,
                    '数学排名': student.stuGrades.rankings[1],
                    '英语': student.stuGrades.grades[2].score,
                    '英语排名': student.stuGrades.rankings[2],
                    '物理': student.stuGrades.grades[3].score,
                    '物理排名': student.stuGrades.rankings[3],
                    '化学': student.stuGrades.grades[4].score,
                    '化学排名': student.stuGrades.rankings[4],
                    '生物': student.stuGrades.grades[5].score,
                    '生物排名': student.stuGrades.rankings[5],
                    '历史': student.stuGrades.grades[6].score,
                    '历史排名': student.stuGrades.rankings[6],
                    '政治': student.stuGrades.grades[7].score,
                    '政治排名': student.stuGrades.rankings[7],
                    '地理': student.stuGrades.grades[8].score,
                    '地理排名': student.stuGrades.rankings[8],
                    '总分': student.stuGrades.totalScores,
                    '总排名': student.stuGrades.totalRanking,
                }
                # 将这个学生的信息字典添加到数据列表中
                data.append(student_data)
        print(data)
        return data

    # mode1==0物理类mode1==1历史类
    # mode2==0总分排序
    # mode2==1语文排序
    # 以此类推
    # mode3==0 降序，分数高到低，mode3==1升序，分数低到高
    # 返回字典列表
    def getAllGrades(self, mode1, mode2, mode3):
        switch = [3, 6]
        mode1 = switch[mode1]
        selected_subjects = [stu for stu in self.student if
                             stu.stuGrades.grades[mode1].score != -1]
        if mode2 != 0:
            selected_subjects = sorted(selected_subjects,
                                       key=lambda sub: (
                                           sub.stuGrades.rankings[mode2 - 1] == -1, sub.stuGrades.rankings[mode2 - 1]),
                                       reverse=mode3)
        else:
            selected_subjects = sorted(selected_subjects,
                                       key=lambda sub: sub.stuGrades.totalRanking,
                                       reverse=mode3)
        for stu in selected_subjects:
            for i in range(9):
                print(stu.stuGrades.grades[i].score, end='\t')
            print(end='|')
            print(stu.stuGrades.totalRanking, end=' |')
            for i in range(9):
                print(stu.stuGrades.rankings[i], end='\t')
            print(end='|')
            print()
        print('----------------------------------------------------------------')
        return self.getGradesTable(2, selected_subjects)

    def saveGradesToCSV(self, path='./excelFiles/rankedGrades.csv'):
        try:
            # 将数据转换为 DataFrame
            df = pd.DataFrame(self.getGradesTable(1, self.student))
            # 将 DataFrame 保存到 CSV 文件中
            df.to_csv(path, index=False)
            print(f"学生数据已成功保存到 {path}")
            return True
        except Exception as e:
            print(e)
            return False

    # 将学生成绩数据保存到数据库中
    def saveGradesToMySQL(self,
                          host=host,  # 主机地址
                          user=user,  # 数据库用户名
                          password=password,  # 密码
                          database=database,  # 数据库名称
                          table=rankedGradesTable,  # 数据库表名
                          ):
        # 将数据转换为 DataFrame
        df = pd.DataFrame(2, self.getGradesTable(self.student))
        # 将dataframe保存至数据库
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()

        # 创建一个游标对象
        mycursor = mydb.cursor()
        # 先清空表格
        # sql = 'TRUNCATE TABLE {};'.format(table)
        # mycursor.execute(sql)
        # try:
        #     mycursor.execute(sql)
        # except mysql.connector.errors.ProgrammingError as e:
        #     print("表格还未创建，正在创建表格……", e)
        #     createGradesTable(table, host, user, password, 3306, 'utf8mb4', database=database)
        try:
            # 遍历Excel表格中的每一行，并将每一行插入到数据库中
            for row in df.itertuples(index=False):  # 遍历DataFrame中的每一行
                sql = (f"INSERT IGNORE INTO {table} "
                       f"(姓名,学号,语文,数学,英语,物理,化学,生物,历史,政治,地理,总分) "
                       f"VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                val = row  # 插入的数据
                print("正在插入数据至{}:".format(table), val)  # 输出正在插入的数据
                mycursor.execute(sql, val)  # 执行SQL插入语句
        except Exception as e:
            print('插入数据时出现错误：{}'.format(e))
            mycursor.close()
            mydb.rollback()
            return False
        # 提交更改并关闭数据库连接
        mydb.commit()  # 提交更改
        mycursor.close()  # 关闭游标对象
        mydb.close()  # 关闭数据库连接
        return True

    # 修改成绩至数据库
    def updateGradesToMySQL(self, stuID, subject, new_grade,
                            host=host,  # 主机地址
                            user=user,  # 数据库用户名
                            password=password,  # 密码
                            database=database,  # 数据库名称
                            table=rankedGradesTable,  # 数据库表名
                            ):

        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:
            sqlUpdate = f"""UPDATE {table} SET `{subject}` = %s WHERE `学号` = %s"""
            data = (new_grade, stuID)
            # 更新
            mycursor.execute(sqlUpdate, data)
            mydb.commit()  # 提交更改
            # 提交更改并关闭数据库连接
        except Exception as e:
            mydb.rollback()
            raise e
        finally:
            mycursor.close()  # 关闭游标对象
            mydb.close()  # 关闭数据库连接

    # 清空成绩
    def truncateGrades(self, host=host,  # 主机地址
                       user=user,  # 数据库用户名
                       password=password,  # 密码
                       database=database,  # 数据库名称
                       table=rankedGradesTable,  # 数据库表名
                       ):
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:
            sql = f"TRUNCATE TABLE {table}"
            # 更新
            mycursor.execute(sql)
            mydb.commit()  # 提交更改
            # 提交更改并关闭数据库连接
        except Exception as e:
            mydb.rollback()
            raise e
        finally:
            mycursor.close()  # 关闭游标对象
            mydb.close()  # 关闭数据库连接

    # 将申请表列表转换为字典列表类型
    def getCheckApplicaionsTable(self):
        teacher_name_list = [check_application.teacherName for check_application in self.checkApplication]
        stu_name_list = [check_application.stuName for check_application in self.checkApplication]
        stu_ID_list = [check_application.stuID for check_application in self.checkApplication]
        subject_list = [check_application.subjectToCheck for check_application in self.checkApplication]
        data = {'申请老师': teacher_name_list, '被申请学生姓名': stu_name_list, '学生学号': stu_ID_list,
                '申请科目': subject_list}
        return data

    # 保存申请表到CSV文件中
    def saveCheckApplicationsToCSV(self):
        teacher_name_list = [check_application.teacherName for check_application in self.checkApplication]
        stu_name_list = [check_application.stuName for check_application in self.checkApplication]
        stu_ID_list = [check_application.stuID for check_application in self.checkApplication]
        subject_list = [check_application.subjectToCheck for check_application in self.checkApplication]
        data = {'申请老师': teacher_name_list, '被申请学生姓名': stu_name_list, '学生学号': stu_ID_list,
                '申请科目': subject_list}

        df = pd.DataFrame(data)
        df.to_csv('./excelFiles/checkApplications.csv', index=False, mode='w')

    # 从数据库中读取申请表信息并加入列表中
    def saveCheckApplicationsToMySQL(self,
                                     host=host,  # 主机地址
                                     user=user,  # 数据库用户名
                                     password=password,  # 密码
                                     database=database,  # 数据库名称
                                     table=checkApplicationsTable,  # 数据库表名
                                     ):
        # 将数据转换为 DataFrame
        df = pd.DataFrame(self.getCheckApplicaionsTable())
        # print(df)
        # 将dataframe保存至数据库
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
            return False
        # 创建一个游标对象
        # 先清空表格
        # sql = 'TRUNCATE TABLE {};'.format(table)
        # # mycursor.execute(sql)
        # try:
        #     mycursor.execute(sql)
        # except mysql.connector.errors.ProgrammingError as e:
        #     print("表格还未创建，正在创建表格……", e)
        #     createCheckApplicationsTable(table, host, user, password, 3306, 'utf8mb4', database=database)

        mycursor = mydb.cursor()
        try:
            # 遍历Excel表格中的每一行，并将每一行插入到数据库中
            for row in df.itertuples(index=False):  # 遍历DataFrame中的每一行
                sql = (f"INSERT IGNORE INTO {table} "
                       f"(申请老师,被申请学生姓名,学生学号,申请科目) "
                       f"VALUES (%s,%s,%s,%s)")
                val = row  # 插入的数据
                print("正在插入数据至{}:".format(table), val)  # 输出正在插入的数据
                mycursor.execute(sql, val)  # 执行SQL插入语句
        except Exception as e:
            print('插入数据时出现错误{}'.format(e), e)
            mydb.rollback()
            mycursor.close()
            return False
            # 提交更改并关闭数据库连接
        mydb.commit()  # 提交更改
        mycursor.close()  # 关闭游标对象
        mydb.close()  # 关闭数据库连接

    def getApplicationFromSql(self,
                              host=host,  # 主机地址
                              user=user,  # 数据库用户名
                              password=password,  # 密码
                              database=database,  # 数据库名称
                              table=checkApplicationsTable  # 数据库表名
                              ):

        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            return False

        cursor = mydb.cursor(dictionary=True)
        try:
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            results = cursor.fetchall()

            df = pd.DataFrame(results)
            #print(df)

            for index, row in df.iterrows():
                check_application = CheckApplication.CheckApplication(row['申请老师'], row['被申请学生姓名'],
                                                                      row['学生学号'], row['申请科目'])
                self.checkApplication.append(check_application)
            self.checkApplicationNum = len(self.checkApplication)

        except Exception as e:
            cursor.close()
            mydb.rollback()
            print('从服务器获取申请表信息时出现错误{}'.format(e))
            return False

        if mydb.is_connected():
            cursor.close()
            mydb.close()

        return True

    # 清空申请表
    def truncateCheckApplication(self, host=host,  # 主机地址
                                 user=user,  # 数据库用户名
                                 password=password,  # 密码
                                 database=database,  # 数据库名称
                                 table=checkApplicationsTable,  # 数据库表名
                                 ):
        global mydb
        try:
            mydb = mysql.connector.connect(
                host=host,  # 数据库主机地址
                user=user,  # 数据库用户名
                password=password,  # 数据库密码
                database=database  # 数据库名称
            )
        except Exception as e:
            print('无法连接至数据库{}'.format(database), e)
            mydb.close()
        # 创建一个游标对象
        mycursor = mydb.cursor()
        try:
            sql = f"TRUNCATE TABLE {table}"
            # 更新
            mycursor.execute(sql)
            mydb.commit()  # 提交更改
            # 提交更改并关闭数据库连接
        except Exception as e:
            mydb.rollback()
            raise e
        finally:
            mycursor.close()  # 关闭游标对象
            mydb.close()  # 关闭数据库连接


gradeManager = GradeManager([], 0, [], 0)

# gradeManager.inputMore("./excelFiles/rankedGrades.csv")
# gradeManager.inputCheckApplications("./excelFiles/checkApplications.csv")
# for i in range(10):
#     for j in range(2):
#         gradeManager.getAllGrades(i, j)
#         print('\n')
# gradeManager=GradeManager()

# gradeManager.inputMySQL()
# gradeManager.renewTotalGrade()
# gradeManager.sortGrades()
# gradeManager.saveGradesToMySQL()
# gradeManager.inputCheckApplications('./excelFiles/checkApplications.csv')
# gradeManager.getApplicaFromSql()

# gradeManager.addCheckApplication('user2', '杨浩焱', 20501004, '语文')

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
       print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)
   grade3 = gr.Grades(Chinese(139), Math(100), English(149),
                      Physics(0), Chemistry(0), Biology(0), History(100), Politics(100), Geography(100))
   manager.inputExcelGrades(1, "夏洛", 3, grade3)
   for x in manager.student:
       print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)  # 测试添加功能
   print("张三：", manager.student[0].stuGrades.grades[0].score)
   manager.changeGrades("张三", 1, "Chinese", 1)
   print("张三：", manager.student[0].stuGrades.grades[0].score)
   print("排序前:")
   for x in manager.student:
       print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)  # 测试修改功能
   manager.sortGrades()
   print("排序后：")
   for x in manager.student:
       print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)  # 测试排序功能
   '''

    # 测试从csv文件导入

    # gradeManager = GradeManager([], 0, [], 0)
    # gradeManager.inputCSV("./excelFiles/student.csv")
    # gradeManager.addCheckApplication('user2', '张三', 200001, '语文')
    # manager = GradeManager([], 0, [],0)
    # manager.inputExcelGrades(2, r"C:\\Users\\32284\Desktop\Grades\GradesAnalysis\Code\student.xlsx")

    # for x in manager.student:
    #     print(x.name, " ", x.stuID, " ", x.stuGrades.totalScores)

    # 测试单科排名
    '''
    print("按语文排名前：")
    for x in manager.student:
        print(x.name, " ", x.stuID, " ", x.stuGrades.grades[0].score)

    templist = manager.calculateRanking("chinese", 1)

    print("按语文排名后：")
    for x in templist:
        print(x.name, " ", x.stuID, " ", x.stuGrades.grades[0].score)
    '''

    # manager.generateGradesAnalysis(1, "Math")
    # manager.generateGradesAnalysis(2,1)
