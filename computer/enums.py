# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals


class ComputerInstruction(object):
    """
    Enum that lists all possible instructions for `Computer`.
    """
    MULT = 'mult'
    CALL = 'call'
    RET = 'ret'
    STOP = 'stop'
    PRINT = 'print'
    PUSH = 'push'

    _ALL_INTRUCTIONS = {
        MULT: MULT,
        CALL: CALL,
        RET: RET,
        STOP: STOP,
        PRINT: PRINT,
        PUSH: PUSH,
    }

    @classmethod
    def get_value(cls, possible_instruction):
        """
        Returns the cleaned version of `possible_instruction`, if available.
        :param possible_instruction: The instruction to verify and clean
        :return:
        """
        return cls._ALL_INTRUCTIONS.get(possible_instruction.lower())
