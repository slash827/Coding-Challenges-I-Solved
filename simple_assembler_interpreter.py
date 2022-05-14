def execute(line: list, regs: list):  # returns array of registers if its not jnz or the jump value otherwise
    # the list is a split of the line by sepertor of space
    flag = 0
    if not line[1].isnumeric():
        first_reg = ord(line[1]) - 97
    else:
        flag = 1
        first_reg = int(line[1])
    second_reg = -1
    if len(line) > 2 and line[2].isalpha():
        second_reg = ord(line[2]) - 97
    if line[0] == 'mov' and flag == 0:
        if second_reg == -1:
            regs[first_reg] = int(line[2])
        else:
            regs[first_reg] = regs[second_reg]
    if line[0] == 'inc' and flag == 0:
        regs[first_reg] += 1
    if line[0] == 'dec' and flag == 0:
        regs[first_reg] -= 1
    if (flag == 1 and first_reg != 0) or (line[0] == 'jnz' and regs[first_reg] != 0):
        return int(line[2])
    return [regs,first_reg]  # first is the value of possible jump , then the value of the modified reg


def simple_assembler(program: list):
    regs = [0 for x in range(0, 26)]
    been_used = []
    pos = 0
    while pos < len(program):
        line = program[pos].split(' ')
        line = [x for x in line if x != '']
        res = execute(line, regs)
        if type(res) == int:
            pos += res
            continue
        else:
            regs = res[0]
            been_used.append(res[1])
        pos += 1
    dict = {}
    for i in range(0, len(regs)):
        if regs[i] != 0 or i in been_used:
            dict[chr(i+97)] = regs[i]
    return dict


def main():
    program = ['mov a 1','mov b 1','mov c 0','mov d 26','jnz c 2','jnz 1 5','mov c 7']
    program += ['inc d','dec c','jnz c -2','mov c a','inc a','dec b','jnz b -2','mov b c']
    program += ['dec d','jnz d -6','mov c 18','mov d 11','inc a','dec d','jnz d -2','dec c','jnz c -5']
    print(simple_assembler(program))


if __name__ == '__main__':
    main()