import mcschematic

def parse_part(part, schem, offset_x, offset_z):
    for i in range(8):
        if(part[i] == '1'):
            schem.setBlock((-1 + offset_x, 14 - i * 2, offset_z), 'minecraft:redstone_block')
        else:
            schem.setBlock((-1 + offset_x, 14 - i * 2, offset_z), 'minecraft:air')
    return 0

def parse(binary_array):
    schem = mcschematic.MCSchematic()
    offset_x = -1
    offset_z = 0
    words_count = 0
    for word in binary_array:
        if(words_count // 8 == 1):
            offset_z -= 8
            offset_x = -1
            words_count = 0
        words_count += 1
        first_part = word[8:]
        second_part = word[:8]
        parse_part(second_part, schem, offset_x, offset_z)
        offset_x -= 8
        parse_part(first_part, schem, offset_x, offset_z)
        offset_x -= 2

    return schem