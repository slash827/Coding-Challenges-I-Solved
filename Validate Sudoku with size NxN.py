import math


class Sudoku(object):
    def __init__(self, data):
        self.data = data
        self.N = len(data)
        t = math.sqrt(self.N)
        if round(t) != t:
            print("error wrong sudoku format")

    def transpose(self):
        for i in range(self.N):
            for j in range(i, self.N):
                self.data[i][j], self.data[j][i] = self.data[j][i], self.data[i][j]

    def check_rows(self):
        for row in self.data:
            ls = list(range(1, 1 + self.N))
            if sorted(row) != ls:
                return False
        return True

    def check_sqr(self, ls: list):
        ls2 = list(range(1, 1 + self.N))
        if sorted(ls) == ls2:
            return True
        return False

    def check_squares(self):
        t = round(math.sqrt(self.N))
        for i in range(t):
            for j in range(t):
                ls = []
                for k in range(i*t, (i+1)*t):
                    for m in range(j*t, (j+1)*t):
                        ls.append(self.data[k][m])
                if not self.check_sqr(ls):
                    print(f"{i} and {j}")
                    return False
        return True

    def check_format(self):
        for i in range(len(self.data)):
            for j in range(len(self.data[i])):
                if type(self.data[i][j]) == str:
                    if not self.data[i][j].isnumeric():
                        return False
                    else:
                        self.data[i][j] = int(self.data[i][j])
                if type(self.data[i][j]) == int:
                    if self.data[i][j] < 1 or self.data[i][j] > self.N:
                        return False
                else:  # means not an int nor an str type
                    return False
        return True

    def is_valid(self):
        print(self.data)
        if not self.check_format():
            return False
        if not self.check_rows():
            return False
        self.transpose()
        if not self.check_rows():
            return False
        # so far checks rows and columns
        if not self.check_squares():
            return False
        return True