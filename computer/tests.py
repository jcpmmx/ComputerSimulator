# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from django.test import TestCase

from computer.models import Computer


class ComputerTestCase(TestCase):
    """
    Test case that check the behavior of `Computer` when tested as a standalone model.
    """
    
    def test_good_program(self):
        """
        The program is as given originally by the test description and produces the expected output.
        """
        PRINT_TENTEN_BEGIN = 50
        MAIN_BEGIN = 0
        computer = Computer(program_stack_size=100)
        computer.set_address(PRINT_TENTEN_BEGIN).insert('MULT').insert('PRINT').insert('RET')
        computer.set_address(MAIN_BEGIN).insert('PUSH', 1009).insert('PRINT')
        computer.insert('PUSH', 6)
        computer.insert('PUSH', 101).insert('PUSH', 10).insert('CALL', PRINT_TENTEN_BEGIN)
        computer.insert('STOP')
        computer.set_address(MAIN_BEGIN)
        output_data = computer.execute()
        self.assertEqual(output_data, ['1009', '1010'])

    def test_bad_program(self):
        """
        We explicitly remove the STOP instruction, making the program enter an infinite loop that causes a failure when
        trying to execute MULT (line 50) without data in memory (since it has been already removed by the 1st run).
        """
        PRINT_TENTEN_BEGIN = 50
        MAIN_BEGIN = 0
        computer = Computer(program_stack_size=100)
        computer.set_address(PRINT_TENTEN_BEGIN).insert('MULT').insert('PRINT').insert('RET')
        computer.set_address(MAIN_BEGIN).insert('PUSH', 1009).insert('PRINT')
        computer.insert('PUSH', 6)
        computer.insert('PUSH', 101).insert('PUSH', 10).insert('CALL', PRINT_TENTEN_BEGIN)
        #computer.insert('STOP')
        computer.set_address(MAIN_BEGIN)
        self.assertRaises(IndexError, computer.execute)

    def test_different_program(self):
        """
        We create a different program to make sure everything works as expected.
        """
        computer = Computer(program_stack_size=30)
        computer.insert('PUSH', 7).insert('PUSH', 7).insert('PUSH', 49).insert('CALL', 13)
        computer.set_address(13)
        computer.insert('PRINT').insert('MULT').insert('PRINT').insert('STOP')
        computer.set_address(0)
        output_data = computer.execute()
        self.assertEqual(output_data, ['49', '49'])
