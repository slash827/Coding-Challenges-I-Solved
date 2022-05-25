def binomial(n, k):
    n, k = abs(n), abs(k)

    if n == k or k == 0 or n == 0:
        return 1
    if n < k or n < 0:
        return 0

    prod = 1
    for i in range(2, n + 1):
        prod *= i
    for i in range(2, k + 1):
        prod //= i
    for i in range(2, n - k + 1):
        prod //= i
    return prod


def find_letter(expr: str):
    arr = [str(x) for x in range(10)] + ['+', '-']
    i = 0
    while i < len(expr) and expr[i] in arr:
        i += 1
    if i == len(expr):
        print("cant find a variable in the expression")
        return None
    return expr[i]


def create_coefficients_array(deg, a, b):
    # creating the array of the result's coefficients
    coef = []
    for i in range(0, deg + 1):
        coef.append(binomial(deg, i))
        print(f"current coef is: {coef[i]}")
        print(f'a is: {a} and b is: {b} and deg is: {deg}')
        coef[i] *= (a ** i) * (b ** (deg - i))
    print(f'coef is: {coef}')
    return coef


def create_from_monomials(coefficient_arr, letter):
    # creating the result array of all monomials and their coefficients in their place
    results = []
    for index, coeff in enumerate(coefficient_arr):
        if coeff == 0:
            continue
        elif abs(coeff) == 1 and index > 0:
            results.append('')
            if coeff == -1:
                results[len(results) - 1] += '-'
        elif (abs(coeff) != 1 and coeff != 0 ) or (abs(coeff) == 1 and index == 0):
            results.append(str(coeff))
        elif abs(coeff) != 1:
            results.append(str(coeff))

        if index == 1:
            results[len(results) - 1] += letter
        elif index > 0:
            results[len(results) - 1] += letter + '^' + str(index)

    results.reverse()
    return results


def combine_coefficients_to_string(results):
    final, results = [results[0]], results[1:]
    for value in results:
        if value[0] != '-':
            final += '+'
        final += value

    return ''.join(final)


def find_coefficient_and_const(expr, let_index):
    # a will contain the value of the coefficient of the letter and b will contain the constant's value
    a = expr[:let_index]
    b = expr[let_index + 1:]
    signs = [1, 1]

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

    return int(a), int(b)


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
    a, b = find_coefficient_and_const(expr, let_index)

    # now we finished interpreting all the numbers and the variable values
    if b == 0:  # specific east case when there is no constant value
        a = a ** deg
        return str(a) + letter + '^' + str(deg)

    # creating the array of the result's coefficients
    coef = create_coefficients_array(deg, a, b)
    results = create_from_monomials(coef, letter)
    return combine_coefficients_to_string(results)


def main():
    expr = '(5m+3)^4'
    print(expand(expr))


if __name__ == '__main__':
    main()


