import sys

def generate_machine_code(line: str, symbol_table: dict, next_variable_address: int, comp_lookup: dict, dest_lookup: dict, jump_lookup: dict) -> (str, int):
    # Process A-instruction
    if line.startswith('@'):
        symbol = line[1:]
        if symbol.isdigit():
            # Direct address
            address = int(symbol)
        else:
            # Symbolic address
            if symbol not in symbol_table:
                symbol_table[symbol] = next_variable_address
                next_variable_address += 1
            address = symbol_table[symbol]
        # Return binary representation of the address
        return f'0{address:015b}', next_variable_address
    else:
        # Process C-instruction
        dest, comp, jump = 'null', '', 'null'
        if '=' in line:
            parts = line.split('=')
            dest = parts[0].strip()
            line = parts[1].strip()
        if ';' in line:
            parts = line.split(';')
            comp = parts[0].strip()
            jump = parts[1].strip()
        else:
            comp = line.strip()
        # Return binary representation of the C-instruction
        return f'111{comp_lookup[comp]}{dest_lookup[dest]}{jump_lookup[jump]}', next_variable_address

def init_jump_lookup_dict() -> dict:
    # Initialize jump lookup table
    jump_lookup = {
        "null": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"
    }
    return jump_lookup

def init_dest_lookup_dict() -> dict:
    # Initialize dest lookup table
    dest_lookup = {
        "null": "000",
        "M": "001",
        "D": "010",
        "MD": "011",
        "A": "100",
        "AM": "101",
        "AD": "110",
        "AMD": "111"
    }
    return dest_lookup

def init_comp_lookup_dict() -> dict:
    # Initialize comp lookup table
    comp_lookup = {
        "0": "0101010",
        "1": "0111111",
        "-1": "0111010",
        "D": "0001100",
        "A": "0110000",
        "!D": "0001101",
        "!A": "0110001",
        "-D": "0001111",
        "-A": "0110011",
        "D+1": "0011111",
        "A+1": "0110111",
        "D-1": "0001110",
        "A-1": "0110010",
        "D+A": "0000010",
        "D-A": "0010011",
        "A-D": "0000111",
        "D&A": "0000000",
        "D|A": "0010101",
        "M": "1110000",
        "!M": "1110001",
        "-M": "1110011",
        "M+1": "1110111",
        "M-1": "1110010",
        "D+M": "1000010",
        "D-M": "1010011",
        "M-D": "1000111",
        "D&M": "1000000",
        "D|M": "1010101"
    }
    return comp_lookup

def parse(input_line: str) -> str:
    # Remove white spaces and comments
    output_line = input_line.strip()
    output_line = output_line.split("//")[0].strip()
    return output_line

def main():
    # Read input file name from command line arguments
    input_filename = sys.argv[1]
    output_filename = input_filename.replace('.asm', '.hack')

    # Read the content of the input file
    input_file_contents = []
    with open(input_filename, "r") as input_file:
        input_file_contents = input_file.readlines()

    # Initialize the symbol table with predefined symbols
    symbol_table = {
        'SP': 0,
        'LCL': 1,
        'ARG': 2,
        'THIS': 3,
        'THAT': 4,
        'R0': 0,
        'R1': 1,
        'R2': 2,
        'R3': 3,
        'R4': 4,
        'R5': 5,
        'R6': 6,
        'R7': 7,
        'R8': 8,
        'R9': 9,
        'R10': 10,
        'R11': 11,
        'R12': 12,
        'R13': 13,
        'R14': 14,
        'R15': 15,
        'SCREEN': 16384,
        'KBD': 24576
    }
    next_variable_address = 16

    # Initialize lookup tables
    jump_lookup = init_jump_lookup_dict()
    dest_lookup = init_dest_lookup_dict()
    comp_lookup = init_comp_lookup_dict()

    # First pass: Resolve labels
    rom_address = 0
    for line in input_file_contents:
        parsed_line = parse(line)
        if parsed_line:
            if parsed_line.startswith('(') and parsed_line.endswith(')'):
                # Label found, add to symbol table
                symbol = parsed_line[1:-1]
                symbol_table[symbol] = rom_address
            else:
                rom_address += 1

    # Second pass: Generate machine code
    machine_code = []
    for line in input_file_contents:
        parsed_line = parse(line)
        if parsed_line and not (parsed_line.startswith('(') and parsed_line.endswith(')')):
            binary_line, next_variable_address = generate_machine_code(parsed_line, symbol_table, next_variable_address, comp_lookup, dest_lookup, jump_lookup)
            machine_code.append(binary_line)

    # Write the machine code to the output file
    with open(output_filename, "w") as output_file:
        for code in machine_code:
            output_file.write(code + '\n')

if __name__ == "__main__":
    main()
