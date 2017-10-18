# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from jsonfield import JSONField

from django.db import models

from computer.enums import ComputerInstruction
from computer.utils import ComputerException, generate_computer_id


class Computer(models.Model):
    """
    Model that implements a 'Computer Simulator'.

    The current state of the Computer supports the following instructions:
    - PUSH(arg): Pushes an argument to the stack
    - PRINT: Pops from stack and prints the value
    - MULT: Pops the latest 2 arguments from the stack, multiplies them and pushes the result back to the stack
    - CALL(addr): Sets the program counter (PC) to the given addr
    - RET: Pops address from stack and set PC to address
    - STOP: Exits the program
    """
    id = models.CharField(primary_key=True, default=generate_computer_id, max_length=7, editable=False)
    program_counter = models.PositiveSmallIntegerField('Program counter (PC)', default=0)
    program_stack = JSONField('Data of the program stack', default={})
    program_stack_size = models.PositiveSmallIntegerField()
    program_stack_pointer = models.PositiveSmallIntegerField(default=0)

    def __init__(self, *args, **kwargs):
        """
        Creates a new `Computer` with `number_of_addresses` addresses, assuming `number_of_addresses` is a positive int.

        :param number_of_addresses: The number of addresses that the current `Computer` will support
        """
        stack_size = kwargs.pop('stack_size', 0)
        super(Computer, self).__init__(*args, **kwargs)
        if stack_size:
            self.program_stack = {idx: (None, None) for idx in xrange(stack_size)}
            self.program_stack_size = stack_size

    def set_address(self, address_index):
        """
        Sets the current value for the index of the program stack.

        :param address_index: The value to set the program stack index to
        :return: Computer
        """
        if address_index <= self.program_stack_size:
            self.program_stack_pointer = address_index
        else:
            raise ComputerException(
                "You cannot set the address of Computer to {} since it only has support to {} addresses".format(
                address_index, self.program_stack_size))
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
            self.program_stack[self.program_stack_pointer] = (instruction, instruction_arg)
            self.program_stack_pointer += 1
        return self

    def execute(self):
        """
        Executes the stored set of instructions (inside the program stack) starting by the address hold by the program
        counter. It uses local memory to store temporary data that might result from instructions.

        :return: None
        """
        program_output = []
        memory = []
        initial_program_counter = self.program_counter

        while self.program_counter <= self.program_stack_size:
            instruction, instruction_arg = self.program_stack.get(self.program_counter, (None, None))

            if instruction == ComputerInstruction.PUSH:
                memory.append(instruction_arg)

            elif instruction == ComputerInstruction.PRINT:
                value_to_print = memory.pop()
                program_output.append('{}'.format(value_to_print))

            elif instruction == ComputerInstruction.CALL:
                self.program_counter = instruction_arg

            elif instruction == ComputerInstruction.MULT:
                operand1 = int(memory.pop())
                operand2 = int(memory.pop())
                if operand1 and operand2:
                    memory.append(operand1 * operand2)

            elif instruction == ComputerInstruction.RET:
                value_to_ret_to = int(memory.pop())
                if value_to_ret_to:
                    self.program_counter = value_to_ret_to

            elif instruction == ComputerInstruction.STOP:
                break

            # Moving forward with our program execution
            if instruction not in (ComputerInstruction.RET, ComputerInstruction.CALL):
                self.program_counter += 1

        self.program_counter = initial_program_counter
        return program_output

    def debug(self):
        """
        Returns data about the internals of the current `Computer`.

        :return: str
        """
        return {
            'program_counter': '{}'.format(self.program_counter),
            'program_stack': {addr: inst for addr, inst in self.program_stack.items() if inst[0] is not None},
            'program_stack_size': '{}'.format(self.program_stack_size),
            'program_stack_pointer': '{}'.format(self.program_stack_pointer),
        }
