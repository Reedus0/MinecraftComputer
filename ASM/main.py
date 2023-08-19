import sys
import os

import mcschematic

from src.config import schematics_path
from src.compiler import compile
from src.parser import parse

if __name__ == '__main__':
    filename = sys.argv[1]
    with open(filename) as f:
        content = f.read()
        binary_array = compile(content)
        schem = parse(binary_array)
        schem.save(schematics_path, 'asm', mcschematic.Version.JE_1_20_1)
    
