import math


def search_non_zero_row(matrix: list, i):  # assuming i is a row starts with 0
    n = len(matrix)
    j = i + 1
    while j < n:
        if matrix[j][i] != 0:
            return j
        j += 1
    return -1  # in case all rows starts with 0 means det = 0


def add_row_to_row(matrix: list, i, j, mul):
    for k in range(len(matrix[i])):
        matrix[i][k] += mul * matrix[j][k]


def div_row_by_num(matrix: list, i, number):
    if number == 0:
        raise ZeroDivisionError
    for j in range(len(matrix[i])):
        matrix[i][j] /= number


def exchange_rows(matrix: list, i, j):
    matrix[i], matrix[j] = matrix[j], matrix[i]


def determinant(matrix):
    n = len(matrix)
    if len(matrix) == 1:
        return matrix[0][0]
    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    mul = 1
    for i in range(n):
        if matrix[i][i] == 0:
            j = search_non_zero_row(matrix, i)
            if j == -1:
                return 0
            exchange_rows(matrix, i, j)
            mul *= -1
        if matrix[i][i] != 1:
            mul *= matrix[i][i]
            div_row_by_num(matrix, i, matrix[i][i])
        for j in range(i+1, n):
            if matrix[j][i] == 0:
                continue
            add_row_to_row(matrix, j, i, -matrix[j][i])
    print(matrix)
    return round(mul)


def main():
    mat = [[1, 1], [1, 1]]
    print(determinant(mat))


if __name__ == '__main__':
    main()
