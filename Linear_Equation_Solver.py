def merge_dict(dict1: dict, dict2: dict):
    for key in dict2.keys():
        if key in dict1.keys():
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    return dict1


def side_to_variables(side: list, is_right_side):
    var_dict = {}
    for variable in side:
        if variable[0] == '-':
            mul = -1
            variable = variable[1:]
        else: mul = 1

        coef, i = "0", 0
        while i < len(variable) and variable[i].isdigit():
            coef += variable[i]
            i += 1

        if i == 0 and not variable[i].isdigit():
            coef = mul
        else:
            coef = int(coef) * mul

        var_name = variable[i:]
        if var_name != '' and coef == 0:
            coef = 1
        if (is_right_side and var_name != "") or \
                (not is_right_side and var_name == ""):
            coef *= -1

        if var_name not in var_dict.keys():
            var_dict[var_name] = coef
        else:
            var_dict[var_name] += coef

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

    return merge_dict(variables_coef1, variables_coef2)


def gauss_elimination(matrix):
    # m x (n+1) matrix where last column is the constants column
    # and we assume that n <= m means at least the same amount of equations as variables
    m, n = len(matrix), len(matrix[0]) - 1  # m is thee amount of equations and n is the amount of variables
    j = 0
    while j < n:
        if m < n:
            return None

        if matrix[j][j] == 0:
            for i in range(j+1, m):
                if matrix[i][j] != 0:
                    matrix[i][j:], matrix[j][j:] = matrix[j][j:], matrix[i][j:]
                    break
            return None

        matrix[j] = [item / matrix[j][j] for item in matrix[j]]
        for i in range(j+1, m):
            prod = matrix[i][j]
            for k in range(j, n+1):
                matrix[i][k] -= prod * matrix[j][k]

            if matrix[i][:-1] == [0] * n and matrix[i][-1] != 0:
                return None

        # now deleting zero rows
        i = j + 1
        while i < m:
            if matrix[i] == [0] * (n + 1):
                del matrix[i]
                m -= 1
                continue
            i += 1

        j += 1

    # now doing back subtraction
    j = m - 1
    while j > 0:
        for k in range(j):
            matrix[k][n] -= matrix[k][j] * matrix[j][n]
            matrix[k][j] = 0
        j -= 1

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

    coef_matrix = [[item[1] for item in all_equations_dict[i]] for i in range(len(all_equations_dict))]

    amount_of_variables = len(coef_matrix[0]) - 1
    amount_of_equation = len(coef_matrix)

    # it means that it is not solvable
    if amount_of_variables > amount_of_equation:
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
