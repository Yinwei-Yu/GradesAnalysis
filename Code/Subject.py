'''
2024/7/4
    __init__()
    setScore()
by 陈邱华

2024/xx/xx
    func()
by xxx
'''


class Subject:

    def __init__(self, score: int):
        self.score = score

    def setScore(self, score: int):
        self.score = score


class Chinese(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class Math(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class English(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class Physics(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class Chemistry(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class Biology(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class History(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class Politics(Subject):
    def __init__(self, score: int):
        super().__init__(score)


class Geography(Subject):
    def __init__(self, score: int):
        super().__init__(score)


# 测试函数
if __name__ == '__main__':
    myChinese = Chinese(135)
    print(myChinese.score)
