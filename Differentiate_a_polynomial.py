def calc(res, point):
    total = 0
    for i in range(len(res)):
        if res[i][1] < 1:
            continue
        total += res[i][0] * res[i][1] * (point ** (res[i][1]-1))
    return total


def calc_poly(equ_ls, point):
    res = []
    print(equ_ls)
    for i in range(len(equ_ls)):
        if equ_ls[i] == '':
            continue
        deg = 0
        coffee = 1
        if '^' in equ_ls[i]:
            index = equ_ls[i].index('^')
            deg = int(equ_ls[i][index+1:])
            equ_ls[i] = equ_ls[i][:index-1]
            if equ_ls[i] != '' and equ_ls[i] != '-':
                coffee = int(equ_ls[i])
            elif equ_ls[i] == '-':
                coffee = -1
        elif 'x' in equ_ls[i]:  # linear
            deg = 1
            equ_ls[i] = equ_ls[i][:-1]
            if equ_ls[i] != '' and equ_ls[i] != '-':
                print(f"string is {equ_ls[i]}")
                coffee = int(equ_ls[i])
            elif equ_ls[i] == '-':
                coffee = -1
        else:  # constant
            coffee = int(equ_ls[i])
        res.append([coffee, deg])
    return calc(res, point)


def differentiate(equation, point):
    equ_ls = list(equation)
    i = 0
    while i < len(equ_ls):
        if equ_ls[i] == '-':
            i += 1
            equ_ls.insert(i-1, '+')
        i += 1
    equation = "".join(equ_ls).split('+')
    print(equation)
    return calc_poly(equation, point)


def main():
    equation = '-5x^2+10x+4'
    print(differentiate(equation, 0))


if __name__ == '__main__':
    main()
