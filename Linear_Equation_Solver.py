def calc_coefficient(variable, mul):
    coefficient, i = "0", 0
    while i < len(variable) and variable[i].isdigit():
        coefficient += variable[i]
        i += 1

    if i == 0 and not variable[i].isdigit():
        coefficient = mul
    else:
        coefficient = int(coefficient) * mul
    return coefficient, i


def update_coefficient_to_dict(variable, coefficient, i, is_right_side, var_dict):
    var_name = variable[i:]
    if var_name != '' and coefficient == 0:
        coefficient = 1
    if (is_right_side and var_name != "") or \
            (not is_right_side and var_name == ""):
        coefficient *= -1

    if var_name not in var_dict.keys():
        var_dict[var_name] = coefficient
    else:
        var_dict[var_name] += coefficient


def side_to_variables(side: list, is_right_side):
    var_dict = {}
    for variable in side:
        if variable[0] == '-':
            mul = -1
            variable = variable[1:]
        else:
            mul = 1

        coefficient, i = calc_coefficient(variable, mul)
        update_coefficient_to_dict(variable, coefficient, i, is_right_side, var_dict)

    return var_dict


def process_equation(equation):
    equation = equation[0] + equation[1:].replace('-', '+-')
    equation = equation.replace(' ', '')

    sides = equation.split('=')
    first_side = sides[0].split('+')
    second_side = sides[1].split('+')
    first_side = [item for item in first_side if item != '']
    second_side = [item for item in second_side if item != '']

    variables_coef1 = side_to_variables(first_side, False)
    variables_coef2 = side_to_variables(second_side, True)

    return {**variables_coef1, **variables_coef2}


def back_substitution(matrix, m, n):
    j = m - 1
    while j > 0:
        for k in range(j):
            matrix[k][n] -= matrix[k][j] * matrix[j][n]
            matrix[k][j] = 0
        j -= 1


def delete_zero_rows(matrix, m, n, j):
    i = j + 1
    while i < m:
        if matrix[i] == [0] * (n + 1):
            del matrix[i]
            m -= 1
            continue
        i += 1


def forward_substitution(matrix, m, n, j):
    matrix[j] = [item / matrix[j][j] for item in matrix[j]]
    for i in range(j + 1, m):
        prod = matrix[i][j]
        for k in range(j, n + 1):
            matrix[i][k] -= prod * matrix[j][k]

        if matrix[i][:-1] == [0] * n and matrix[i][-1] != 0:
            return False
    return True


def gauss_elimination(matrix):
    # m x (n+1) matrix where last column is the constants column
    # and we assume that n <= m means at least the same amount of equations as variables
    m, n = len(matrix), len(matrix[0]) - 1  # m is thee amount of equations and n is the amount of variables
    j = 0
    while j < n:
        if m < n:
            return None

        if matrix[j][j] == 0:
            for i in range(j + 1, m):
                if matrix[i][j] != 0:
                    matrix[i][j:], matrix[j][j:] = matrix[j][j:], matrix[i][j:]
                    break
            else:
                return None

        if not forward_substitution(matrix, m, n, j):
            return None

        # now deleting zero rows
        delete_zero_rows(matrix, m, n, j)
        j += 1

    # now doing back subtraction
    back_substitution(matrix, m, n)

    return [row[-1] for row in matrix]


def solve(*equations):
    all_equations_dict = []
    all_keys = []
    for equation in equations:
        all_vars = process_equation(equation)
        all_equations_dict.append(all_vars)

        for key in all_vars.keys():
            if key not in all_keys:
                all_keys.append(key)

    for i in range(len(all_equations_dict)):
        for var in all_keys:
            if var not in all_equations_dict[i].keys():
                all_equations_dict[i][var] = 0
        all_equations_dict[i] = list(all_equations_dict[i].items())

    for i in range(len(all_equations_dict)):
        all_equations_dict[i] = sorted(all_equations_dict[i], reverse=True)

    coef_matrix = [[item[1] for item in equation] for equation in all_equations_dict]

    number_of_variables = len(coef_matrix[0]) - 1
    number_of_equations = len(coef_matrix)

    # it means that it is not solvable
    if number_of_variables > number_of_equations:
        return None

    all_keys = sorted(all_keys, reverse=True)[:-1]
    solutions = gauss_elimination(coef_matrix)

    if solutions is None:
        return None

    return {all_keys[i]: solutions[i] for i in range(len(solutions))}


def main():
    solution = solve('6x+z=-3y', 'x+y=7z-1', '4y+10z=-8x')
    print(solution)


if __name__ == '__main__':
    main()
