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
        # print(self.totalScores)
        self.grades = [chinese, math, english, physics, chemistry, biology,
                       history, politics, geography]
        self.totalScores = 0
        for i in range(9):
            # if self.grades[i].score == 0:
            #     self.grades[i].score = -1
            self.totalScores += self.grades[i].score if self.grades[i].score != -1 else 0

        self.gradesAnalysis: str = ""
        self.totalRanking: int = 0
        self.rankings = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

    # 待实现
    def generateGradesAnalysis(self, ranking: int, rankings: list):
        self.totalRanking = ranking
        self.rankings = rankings

    def getGradesAnalysis(self):
        if 0 < self.totalRanking < 6:
            self.gradesAnalysis = "Excellent"
        elif 5 < self.totalRanking < 11:
            self.gradesAnalysis = "Good"
        else:
            self.gradesAnalysis = "OK"
        return self.gradesAnalysis

    def displayGradesAnalysis(self, ):
        grades_str = (
            f'总分：{self.totalScores}排名：{self.totalRanking}语文：{self.grades[0].score}数学：{self.grades[1].score}英语：{self.grades[2].score}'
            f'物理：{self.grades[3].score}化学：{self.grades[4].score}生物：{self.grades[5].score}'
            f'历史:{self.grades[6].score}政治:{self.grades[7].score}地理:{self.grades[8].score}')
        return grades_str


# 测试函数
if __name__ == '__main__':
    myGrades = Grades(Chinese(100), Math(120), English(130), Physics(99), Chemistry(98), Biology(97), History(-1),
                      Politics(-1), Geography(-1))
    myGrades.displayGradesAnalysis()
