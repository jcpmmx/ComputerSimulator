# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from jsonfield import JSONField

from django.core.validators import validate_comma_separated_integer_list
from django.db import models

from computer.enums import ComputerInstruction
from computer.utils import ComputerException, generate_computer_id


class ProgramStack(models.Model):
    """
    Model that implements the program stack of a computer.

    A program stack is just a place to store all instructions of the computer inside an internal dict.
    Data resulting from those instructions will be stored in a simple 'local memory' attribute.
    """
    data = JSONField('Data of the program stack', default={})
    stack_pointer = models.PositiveSmallIntegerField(default=0)
    stack_size = models.PositiveSmallIntegerField(default=0)
    memory = models.CharField(max_length=1000, validators=[validate_comma_separated_integer_list])

    def __init__(self, *args, **kwargs):
        """
        Creates a new `ProgramStack` with `stack_size` slots (initially empty).

        :param stack_size: The size for the current stack
        """
        stack_size = kwargs.pop('stack_size', 0)
        super(ProgramStack, self).__init__(*args, **kwargs)
        if stack_size:
            self.data = {idx: (None, None) for idx in xrange(stack_size)}
            self.stack_size = stack_size

    def set_index(self, index):
        """
        Sets the specific value to serve as index of the program stack.

        :param index: The target index
        :return: None
        """
        if index <= self.stack_size:
            self.stack_pointer = index

    def add_instruction(self, item):
        """
        Stores `item` into the program stack, to the position of the stack pointer.
        It also sets the stack pointer to the index that the next item should have.

        :param item: The item to be added to the stack
        :return: None
        """
        self.data[self.stack_pointer] = item
        self.stack_pointer += 1

    def get_instruction(self, index):
        """
        Returns (without removing) the item that sits in the program stack at index.

        :return: The value from the stack at index, if any
        """
        return self.data.get(index, (None, None))

    def push_to_memory(self, value):
        """
        Pushes `value` to local memory.

        :param value: The item to be added to local memory
        """
        _memory = list(self.memory)
        _memory.append(value)
        self.memory = _memory

    def pop_from_memory(self):
        """
        Pops the latest value stored in local memory, if any.

        :return: The value from the stack at index, if any
        """
        _memory = list(self.memory)
        try:
            value_to_pop = _memory.pop()
            self.memory = _memory
            return value_to_pop
        except IndexError:
            pass


class Computer(models.Model):
    """
    Model that implements a 'Computer Simulator' using a `ProgramStack` as 'memory'.

    The current state of the Computer supports the following instructions:
    - PUSH(arg): Pushes an argument to the stack
    - PRINT: Pops from stack and prints the value
    - MULT: Pops the latest 2 arguments from the stack, multiplies them and pushes the result back to the stack
    - CALL(addr): Sets the program counter (PC) to the given addr
    - RET: Pops address from stack and set PC to address
    - STOP: Exits the program
    """
    id = models.CharField(primary_key=True, default=generate_computer_id, max_length=7, editable=False)
    program_stack = models.OneToOneField(ProgramStack)
    program_counter = models.PositiveSmallIntegerField('Program counter (PC)', default=0)

    def __init__(self, *args, **kwargs):
        """
        Creates a new `Computer` with `number_of_addresses` addresses, assuming `number_of_addresses` is a positive int.

        :param number_of_addresses: The number of addresses that the current `Computer` will support
        """
        stack_size = kwargs.pop('stack_size', 0)
        super(Computer, self).__init__(*args, **kwargs)
        if stack_size:
            self.program_stack = ProgramStack(stack_size=stack_size)

    def set_address(self, address_index):
        """
        Sets the current value for the index of the program stack.

        :param address_index: The value to set the program stack index to
        :return: Computer
        """
        if address_index <= self.program_stack.stack_size:
            self.program_stack.set_index(address_index)
        else:
            raise ComputerException(
                "You cannot set the address of Computer to {} since it only has support to {} addresses".format(
                address_index, self.program_stack.stack_size))
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
            self.program_stack.add_instruction((instruction, instruction_arg))
        return self

    def execute(self):
        """
        Executes the stored set of instructions (inside the program stack) starting by the address hold by the program
        counter. It uses local memory to store temporary data that might result from instructions.

        :return: None
        """
        program_output = []
        while self.program_counter <= self.program_stack.stack_size:
            instruction, instruction_arg = self.program_stack.get_instruction(self.program_counter)

            if instruction == ComputerInstruction.PUSH:
                self.program_stack.push_to_memory(instruction_arg)

            elif instruction == ComputerInstruction.PRINT:
                value_to_print = self.program_stack.pop_from_memory()
                program_output.append(value_to_print)

            elif instruction == ComputerInstruction.CALL:
                self.program_counter = instruction_arg

            elif instruction == ComputerInstruction.MULT:
                operand1 = self.program_stack.pop_from_memory()
                operand2 = self.program_stack.pop_from_memory()
                if operand1 and operand2:
                    self.program_stack.push_to_memory(operand1 * operand2)

            elif instruction == ComputerInstruction.RET:
                value_to_ret_to = self.program_stack.pop_from_memory()
                if value_to_ret_to:
                    self.program_counter = value_to_ret_to

            elif instruction == ComputerInstruction.STOP:
                break

            # Moving forward with our program execution
            if instruction not in (ComputerInstruction.RET, ComputerInstruction.CALL):
                self.program_counter += 1

        return program_output
