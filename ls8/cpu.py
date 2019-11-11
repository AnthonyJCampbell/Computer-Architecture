"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,

            
            0b00000001, # HLT
        ]

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
        print(self.reg)

    # Print the value at the designated register address
    def prn(self, reg):
        print(self.reg[self.pc])

    def run(self):
        """Run the CPU."""
        # We're extracting the instructions from RAM it seems

        active = True
        # Initialize Instruction Register
        IR = None

        while active is True:
            # Store address of data
            IR = self.reg[self.pc]
            
            for value in self.ram:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)


                # "HLT". Halt loop immediately.
                if value == 1:
                    print("Closing run loop")
                    active = False
                    break
                
                # "PRN". Print passed in value
                elif value == 71:
                    self.prn(operand_a)
                    self.pc += 1

                # "LDI". Store a value in register. Passed in value and register
                elif value == 130:
                    # print(f"Storing {operand_b} in register[{operand_a}]")
                    self.ldi(operand_a, operand_b)
                    self.pc += 1

                # print(self.pc)

            break
            # Pass over every instruction in self.ram (through `pc`?)

            # Evaluate the value at self.ram[pc]

            # elif chaning for every operation




        # * `LDI`: load "immediate", store a value in a register, or "set this register to this value".
            # Dec: 130
        # * `PRN`: a pseudo-instruction that prints the numeric value stored in a register.
            # Dec: 71
        # * `HLT`: halt the CPU and exit the emulator.
            # exit the loop if a `HLT` instruction is encountered,regardless of whether or not there are more lines of code in the LS-8 program you loaded. 
            # Dec: 1

        # Read the memory address stored in reg[pc] & store it in Instruction Register (a local variable)

        # Using `ram_read()`, read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them.

        # depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec.

        # After running code for any particular instruction, the `PC` needs to be updated to point to the next instruction for the next iteration of the loop in `run()`. The number of bytes an instruction uses can be determined from the two high bits (bits 6-7) of the instruction opcode.


