"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self, program):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        for instruction in program:
            self.ram[address] = instruction
            address += 1

        # print(f"self.ram is loaded with instructions, it currently looks like: {self.ram}")

    # Returns the value found at the address in memory
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, data):
        self.ram[address] = data

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc

        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            
        else:
            raise Exception("Unsupported ALU operation")



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()



    # sets a specified register to a specified value
    def ldi(self, reg_a, data):
        self.reg[reg_a] = data



    # Print the value at the designated register address
    def prn(self, reg):
        print(self.reg[reg])



    def run(self):
        """Run the CPU."""
        # We're extracting the instructions from RAM it seems

        active = True
        # Initialize Instruction Register

        while active is True:
            # Store address of data
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # `HLT`: halt the CPU and exit the emulator.
            if IR == 0b00000001:
                print("Closing run loop")
                active = False
                break
            
            # "PRN". `PRN`: a pseudo-instruction that prints the numeric value stored in a register.
            elif IR == 0b01000111:
                self.prn(operand_a)
                self.pc += 2

            elif IR == 0b10100010:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            # * `LDI`: load "immediate", store a value in a register, or "set this register to this value".
            elif IR == 0b10000010:
                # print(f"Storing {operand_b} in register[{operand_a}]")
                self.ldi(operand_a, operand_b)
                self.pc += 3

            else:
                print(f"Invalid instruction {IR}")
                sys.exit(1)


