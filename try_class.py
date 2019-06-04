#coding=utf-8

class A():
    name = 'A'

    def __init__(self, some):
        self.some = some
        self._score = None

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score


class B(A):
    name = 'B'

    def __init__(self, some, some2):
        super(B, self).__init__(self, some)
        self.some2 = some2
