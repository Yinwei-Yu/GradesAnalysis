from Subject import *

'''
2024/7/4 
        __init__()
        setRanking()
        generateGradesAnalysis()
        getGradesAnalysis()
        displayGradesAnalysis()
by 陈邱华

2024/7/xx 
        func()
by XXX
'''


class Grades:
    def __init__(self, chinese: Chinese, math: Math, english: English, physics: Physics,
                 chemistry: Chemistry, biology: Biology, history: History, politics: Politics,
                 geography: Geography):
        self.totalScores = (
                chinese.score + math.score + english.score + physics.score + chemistry.score + biology.score + history.score +
                politics.score + geography.score)
        self.grades = [chinese, math, english, physics, chemistry, biology,
                       history, politics, geography]
        self.gradesAnalysis: str = ""
        self.totalRanking: int = 0
        self.rankings = []

    # 待实现
    def generateGradesAnalysis(self, ranking: int, rankings: list):
        self.totalRanking = ranking
        self.rankings = rankings

    def getGradesAnalysis(self):
        return self.gradesAnalysis

    def displayGradesAnalysis(self):
        print(self.totalScores)
        print(self.totalRanking)
        print(self.gradesAnalysis)
        print(self.totalRanking)
        print(self.rankings)


# 测试函数
if __name__ == '__main__':
    myGrades = Grades(Chinese(100), Math(120), English(130), Physics(99), Chemistry(98), Biology(97), History(-1),
                      Politics(-1), Geography(-1))
    myGrades.displayGradesAnalysis()
