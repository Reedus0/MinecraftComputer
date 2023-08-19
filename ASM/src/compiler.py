import re

operations = {
    'NOP': 0b0000,
    'HLT': 0b1111,
    'ADD': 0b0001,
    'SUB': 0b0010,
    'STR': 0b0011,
    'LOD': 0b0100,
    'LDI': 0b0101,
    'JMP': 0b0110,
    'JIZ': 0b0111,
}

alu_operations = [
    operations['ADD'],
    operations['SUB']
]

immediate_operations = [
    operations['LDI']
]

memory_operations = [
    operations['LOD'],
    operations['STR']
]

jump_operations = [
    operations['JMP'],
    operations['JIZ']
]

alu_map = ['r', 'r', 'r']
immediate_map = ['r', 'v']
memory_map = ['r', 'v']
jump_map = ['v']


def check_single_operand(operand):
    try:
        int(operand)
        return 'v'
    except ValueError:
        return 'r'


def check_operands(operands, map):
    result = ''
    for i in range(len(operands)):
        if (map[i] != check_single_operand(operands[i])):
            result = operands[i]
    return result


def register_to_number(register):
    if (re.match('^r[0-7]$', register) == None):
        raise ValueError("Incorrect register: " + register)

    return re.match('r[0-7]', register).group(0)[1]


def parse_operands(operands, map):
    result = []
    for i in range(len(operands)):
        if (map[i] == 'v'):
            result.append(int(operands[i]))
        elif (map[i] == 'r'):
            result.append(int(register_to_number(operands[i])))
    return result


def compile_line(line):
    result = 0b0
    operation = line[:3].upper()
    operands = line[4:].split(', ')

    if (operands[0] == ''):
        operands = operands.pop()
    try:
        operations[operation]
    except KeyError:
        raise ValueError(line + " |  Incorrect operation: " + operation)

    result = result | operations[operation]

    if (operations[operation] in alu_operations):
        if (len(operands) != 3):
            raise ValueError(
                line + " | Incorrect operands, excepted 3, got " + str(len(operands)))
        check_result = check_operands(operands, alu_map)
        if (check_result != ''):
            raise ValueError(line + " | Incorrect operand: " + check_result)

        operands_values = parse_operands(operands, alu_map)
        result = result | operands_values[0] << 5 | operands_values[1] << 10 | operands_values[2] << 13

    elif (operations[operation] in immediate_operations):
        if (len(operands) != 2):
            raise ValueError(
                line + " | Incorrect operands, excepted 2, got " + str(len(operands)))
        check_result = check_operands(operands, immediate_map)
        if (check_result != ''):
            raise ValueError(line + " | Incorrect operand: " + check_result)

        operands_values = parse_operands(operands, immediate_map)
        if (operands_values[1] > 255):
            raise ValueError(
                line + " | Incorrect value, should be less than 256: " + str(operands_values[1]))
        result = result | operands_values[0] << 5 | operands_values[1] << 8

    elif (operations[operation] in memory_operations):
        if (len(operands) != 2):
            raise ValueError(
                line + " | Incorrect operands, excepted 2, got " + str(len(operands)))
        check_result = check_operands(operands, memory_map)
        if (check_result != ''):
            raise ValueError(line + " | Incorrect operand: " + check_result)

        operands_values = parse_operands(operands, memory_map)
        if (operands_values[1] > 63):
            raise ValueError(
                line + " | Incorrect value, should be less than 64: " + str(operands_values[1]))
        result = result | operands_values[0] << 5 | operands_values[1] << 10

    elif (operations[operation] in jump_operations):
        if (len(operands) != 1):
            raise ValueError(
                line + " | Incorrect operands, excepted 1, got " + str(len(operands)))
        check_result = check_operands(operands, jump_map)
        if (check_result != ''):
            raise ValueError(line + " | Incorrect operand: " + check_result)

        operands_values = parse_operands(operands, jump_map)
        if (operands_values[0] > 31):
            raise ValueError(
                line + " | Incorrect value, should be less than 32: " + str(operands_values[0]))
        result = result | operands_values[0] << 11

    return ('{:016b}'.format(result))


def compile(assembly):
    machine_code_array = []
    assembly_lines = assembly.split('\n')
    if (len(assembly_lines) > 32):
        raise ValueError(
            "Too large assembly file, maximum is 32 lines, but got " + str(len(assembly_lines)))
    for line in assembly_lines:
        machine_code_array.append(compile_line(line))
    return machine_code_array
