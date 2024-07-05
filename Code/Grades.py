from Subject import *

'''
2024/7/4 
        __init__()
        setRanking()
        generateGradesAnalysis()
        getGradesAnalysis()
by 陈邱华

2024/7/xx 
        func()
by XXX
'''


class Grades:
    def __init__(self, chinese: Chinese, math: Math, english: English, physics: Physics,
                 chemistry: Chemistry, biology: Biology, history: History, politics: Politics,
                 geography: Geography):
        self.totalGrades = (
                chinese.score + math.score + english.score + physics.score+chemistry.score + biology.score + history.score +
                politics.score + geography.score)
        self.grades = [chinese, math, english, physics, chemistry, biology,
                       history, politics, geography]
        self.gradesAnalysis: str = ""
        self.ranking: int = 0

    def setRanking(self, ranking: int):
        self.ranking = ranking

    # 待实现
    def generateGradesAnalysis(self):
        pass

    def getGradesAnalysis(self):
        return self.gradesAnalysis


# 测试函数
if __name__ == '__main__':
    pass
