def binomial(n: int, k:int):
    n = abs(n)
    k = abs(k)
    prod = 1
    if n == k or k == 0 or n == 0:
        return 1
    if n < k or n < 0:
        return 0
    for i in range(2, n + 1):
        prod *= i
    for i in range(2, k + 1):
        prod //= i
    for i in range(2, n - k + 1):
        prod //= i
    return prod


def find_letter(expr: str):
    arr = [str(x) for x in range(10)] + ['+','-']
    i = 0
    while i < len(expr) and expr[i] in arr:
        i += 1
    if i == len(expr):
        print("cant find a variable in the expression")
        return None
    return expr[i]


def expand(expr: str):
    # first we split the expression from the carrot and parenthesis and calculate the degree
    spl = expr.split("^")
    deg = int(spl[1].strip())
    if deg == 0:
        return '1'
    if deg == 1:
        return spl[0][1:-1]
    expr = spl[0].strip()[1:-1].strip()  # get rid of spaces in the () and outside of it
    del spl

    # now finding the letter of the variable and it's index
    if len(expr) == 1:  # in case the expression is the variable itself alone
        return expr + '^' + str(deg)
    letter = find_letter(expr)
    let_index = expr.index(letter)

    # a will contain the value of the coefficient of the letter and b will contain the constant's value
    a = expr[:let_index]
    b = expr[let_index+1:]
    signs = [1,1]
    if a != '':
        if a[0] == '-':
            if len(a) > 1:
                signs[0] = -1
                a = signs[0] * int(a[1:])
            else:
                a = -1
    else:
        a = 1
    if b != '':
        if b[0] == '-':
            signs[1] = -1
        b = signs[1] * int(b[1:])
    else:
        b = 0
    a = int(a)
    b = int(b)
    # now we finished interpreting all the numbers and the variable values

    if b == 0:  # specific east case when there is no constant value
        a = a ** deg
        return str(a) + letter + '^' + str(deg)

    # creating the array of the result's coefficients
    coef = []
    for i in range(0, deg + 1):
        coef.append(binomial(deg, i))
        print(f"current coef is: {coef[i]}")
        print(f'a is: {a} and b is: {b} and deg is: {deg}')
        coef[i] *= (a ** i) * (b ** (deg - i))
    print(f'coef is: {coef}')

    # creating the result array of all monomials and their coefficients in their place
    results = []
    for i in range(0, deg + 1):
        if coef[i] == 0:
            continue
        elif abs(coef[i]) == 1 and i > 0:
            results.append('')
            if coef[i] == -1:
                results[len(results) - 1] += '-'
        elif (abs(coef[i]) != 1 and coef[i] != 0 ) or (abs(coef[i]) == 1 and i == 0):
            results.append(str(coef[i]))
        elif abs(coef[i]) != 1:
            results.append(str(coef[i]))

        if i == 1:
            results[len(results) - 1] += letter
        elif i > 0:
            results[len(results) - 1] += letter + '^' + str(i)
    results.reverse()
    print(f'results are: {results}')

    # adding them all together
    final = [results[0]]
    for i in range(1, len(results)):
        if results[i][0] != '-':
            final += '+'
        final += results[i]

    return ''.join(final)


def main():
    expr = '(5m+3)^4'
    print(expand(expr))


if __name__ == '__main__':
    main()


