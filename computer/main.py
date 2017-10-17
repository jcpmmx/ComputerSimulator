# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from computer.enums import ComputerInstruction
from computer.utils import ComputerException, ComputerStack


class Computer(object):
    """
    Class that implements a 'Computer Simulator' using a `ComputerStack` as 'memory'.

    The current state of the Computer supports the following instructions:
    - PUSH(arg): Pushes an argument to the stack
    - PRINT: Pops from stack and prints the value
    - MULT: Pops the latest 2 arguments from the stack, multiplies them and pushes the result back to the stack
    - CALL(addr): Sets the program counter (PC) to the given addr
    - RET: Pops address from stack and set PC to address
    - STOP: Exits the program
    """
    _computer_stack = ComputerStack(0)
    _program_counter = 0
    _number_of_addresses = 0

    def __init__(self, number_of_addresses):
        """
        Creates a new `Computer` with `number_of_addresses` addresses, assuming `number_of_addresses` is a positive int.

        :param number_of_addresses: The number of addresses that the current `Computer` will support
        """
        self._computer_stack = ComputerStack(number_of_addresses)
        self._number_of_addresses = number_of_addresses

    def set_address(self, address_index):
        """
        Sets the current value for the index of the program stack.

        :param address_index: The value to set the program stack index to
        :return: Computer
        """
        if address_index <= self._number_of_addresses:
            self._computer_stack.set_index(address_index)
        else:
            raise ComputerException(
                "You cannot set the address of Computer to {} since it only has support to {} addresses".format(
                address_index, self._number_of_addresses))
        return self

    def insert(self, possible_instruction, instruction_arg=None):
        """
        Inserts `possible_instruction` into the current program stack slot.

        :param possible_instruction: The instruction to insert into the program stack
        :param instruction_arg: Optional arg to pass to tied to `possible_instruction`
        :return: Computer
        """
        instruction = ComputerInstruction.get_value(possible_instruction)
        if instruction:
            self._computer_stack.add_instruction((instruction, instruction_arg))  # Storing instructions as tuple
        return self

    def execute(self):
        """
        Executes the stored set of instructions (inside the program stack) starting by the address hold by the program
        counter. It uses local memory to store temporary data that might result from instructions.

        :return: None
        """
        while self._program_counter <= self._number_of_addresses:
            instruction, instruction_arg = self._computer_stack.get_instruction(self._program_counter)

            if instruction == ComputerInstruction.PUSH:
                self._computer_stack.push_to_memory(instruction_arg)

            elif instruction == ComputerInstruction.PRINT:
                value_to_print = self._computer_stack.pop_from_memory()
                print(value_to_print)

            elif instruction == ComputerInstruction.CALL:
                self._program_counter = instruction_arg

            elif instruction == ComputerInstruction.MULT:
                operand1 = self._computer_stack.pop_from_memory()
                operand2 = self._computer_stack.pop_from_memory()
                if operand1 and operand2:
                    self._computer_stack.push_to_memory(operand1 * operand2)

            elif instruction == ComputerInstruction.RET:
                value_to_ret_to = self._computer_stack.pop_from_memory()
                if value_to_ret_to:
                    self._program_counter = value_to_ret_to

            elif instruction == ComputerInstruction.STOP:
                return

            # Moving forward with our program execution
            if instruction not in (ComputerInstruction.RET, ComputerInstruction.CALL):
                self._program_counter += 1

    def _debug(self):
        """
        Prints all internal data store in the current `Computer`.
        :return: None
        """
        print('-------')
        print('Number of addresses: {}'.format(self._number_of_addresses))
        print('Program stack:')
        print('{}'.format(self._computer_stack))
        print('Program stack pointer: {}'.format(self._computer_stack.pointer))
        print('Program counter: {}'.format(self._program_counter))
        print('-------')


# TODO(Julian): Remove this and add proper test cases
# For quick, local testing
if __name__ == '__main__':
    PRINT_TENTEN_BEGIN = 50
    MAIN_BEGIN = 0
    computer = Computer(100)
    # Instructions for the print_tenten function
    computer.set_address(PRINT_TENTEN_BEGIN).insert("MULT").insert("PRINT").insert("RET")
    # The start of the main function
    computer.set_address(MAIN_BEGIN).insert("PUSH", 1009).insert("PRINT")
    # Return address for when print_tenten function finishes
    computer.insert("PUSH", 6)
    # Setup arguments and call print_tenten
    computer.insert("PUSH", 101).insert("PUSH", 10).insert("CALL", PRINT_TENTEN_BEGIN)
    # Stop the program
    computer.insert("STOP")
    # Execute the program
    computer.set_address(MAIN_BEGIN).execute()
