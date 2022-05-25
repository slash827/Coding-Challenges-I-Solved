def calc_derivative_on_point(coefficient_arr, point):
    total = 0
    for coeff in coefficient_arr:
        if coeff[1] >= 1:
            total += coeff[0] * coeff[1] * (point ** (coeff[1] - 1))
    return total


def handle_non_linear(equ_ls, i):
    index = equ_ls[i].index('^')
    deg = int(equ_ls[i][index + 1:])
    equ_ls[i] = equ_ls[i][:index - 1]

    if equ_ls[i] != '' and equ_ls[i] != '-':
        coefficient = int(equ_ls[i])
    elif equ_ls[i] == '-':
        coefficient = -1
    else:
        coefficient = 1
    return coefficient, deg


def handle_linear(equ_ls, i):
    deg = 1
    equ_ls[i] = equ_ls[i][:-1]

    if equ_ls[i] != '' and equ_ls[i] != '-':
        coefficient = int(equ_ls[i])
    elif equ_ls[i] == '-':
        coefficient = -1
    else:
        coefficient = 1
    return coefficient, deg


def calc_poly(equ_ls, point):
    coefficient_arr = []
    for i in range(len(equ_ls)):
        if equ_ls[i] == '':
            continue
        coefficient, deg = 1, 0

        if '^' in equ_ls[i]:
            coefficient, deg = handle_non_linear(equ_ls, i)

        elif 'x' in equ_ls[i]:  # linear
            coefficient, deg = handle_linear(equ_ls, i)

        else:  # constant
            coefficient = int(equ_ls[i])

        coefficient_arr.append([coefficient, deg])
    return calc_derivative_on_point(coefficient_arr, point)


def differentiate(equation, point):
    equ_ls = list(equation)
    i = 0
    while i < len(equ_ls):
        if equ_ls[i] == '-':
            i += 1
            equ_ls.insert(i-1, '+')
        i += 1
    equation = "".join(equ_ls).split('+')[1:]
    print(equation)
    return calc_poly(equation, point)


def main():
    equation = '-5x^2+10x+4'
    print(differentiate(equation, 0))


if __name__ == '__main__':
    main()
