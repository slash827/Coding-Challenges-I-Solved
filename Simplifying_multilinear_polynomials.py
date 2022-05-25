import operator


def eliminating_zeros(coef_and_mono: list):
    i = 0
    while i < len(coef_and_mono):
        if coef_and_mono[i][0] == 0 or '0' in coef_and_mono[i][1]:
            del coef_and_mono[i]
            i -= 1
        i += 1


def creating_string(coef_and_mono_arr: list):
    # changing coefficients numbers to strings
    for coef_and_mono in coef_and_mono_arr:
        if coef_and_mono[0] == -1:
            coef_and_mono[0] = '-'

        elif coef_and_mono[0] == 1:
            coef_and_mono[0] = '+'

        elif coef_and_mono[0] > 0:
            coef_and_mono[0] = '+' + str(coef_and_mono[0])

        else:
            coef_and_mono[0] = str(coef_and_mono[0])

    final = coef_and_mono_arr[0][0] + coef_and_mono_arr[0][1]
    if final[0] == '+':
        final = final[1:]
    for i in range(1, len(coef_and_mono_arr)):
        final += coef_and_mono_arr[i][0] + coef_and_mono_arr[i][1]
    return final


def add_monomials_together(coef_and_mono: list):
    i = 0
    while i < len(coef_and_mono) - 1:
        if coef_and_mono[i][1] == coef_and_mono[i + 1][1]:
            coef_and_mono[i][0] += coef_and_mono[i + 1][0]
            del coef_and_mono[i + 1]
            i -= 1
        i += 1


def sort_in_monomial(coef_and_mono: list):
    for i in range(len(coef_and_mono)):
        coef_and_mono[i][1] = ''.join(sorted(coef_and_mono[i][1]))
    coef_and_mono = sorted(coef_and_mono, key=operator.itemgetter(2, 1))
    return coef_and_mono


def sep_coef_and_mono(monom: str):
    # taking string representing specific monom with it's coef and separating them
    coef = ''
    i = 0
    while i < len(monom) and monom[i].isdigit():
        coef += monom[i]
        i += 1

    if i == len(monom):
        print("error there is no variable in this monomial")
        return None

    monomial = monom[i:]
    if coef == '':
        coef = 1
    else:
        coef = int(coef)
    return [coef, monomial, len(monomial)]


def calc_coef(sep_list: list):
    coef_and_mono = []
    for i in range(len(sep_list)):
        sign = 1
        if sep_list[i][0] == '-':  # means negative coefficient
            sign = -1
            sep_list[i] = sep_list[i][1:]
        coef_and_mono.append(sep_coef_and_mono(sep_list[i]))
        coef_and_mono[i][0] *= sign
    return coef_and_mono


def separate_poly(polist: list):
    i = 0
    while i < len(polist):
        if polist[i] == '-':
            i += 1
            polist.insert(i - 1, '+')
        i += 1

    sep_list = "".join(polist).split('+')
    if sep_list[0] == '':
        del sep_list[0]
    return sep_list


def simplify(poly: str):
    print(poly)

    # separating poly to monomials
    polist = list(poly)
    sep_list = separate_poly(polist)

    # now separating the monomials and their coefficients
    coef_and_mono = calc_coef(sep_list)

    # eliminating zeros in the coef or in the monomials themselves
    eliminating_zeros(coef_and_mono)
    print(coef_and_mono)

    # now sorting each monomial in it's own lexicographic order
    coef_and_mono = sort_in_monomial(coef_and_mono)

    # adding same monomials together
    add_monomials_together(coef_and_mono)
    eliminating_zeros(coef_and_mono)

    # concatenating all monomials together
    final = creating_string(coef_and_mono)
    return final


def main():
    poly = '+dc+dcba-ae+5rt+7abdc-a'
    print(simplify(poly))
    poly = '4a+b-ab+4ac0bc'
    print(simplify(poly))


if __name__ == '__main__':
    main()
