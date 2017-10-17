# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

import os
import sys
import django

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir))
os.environ['DJANGO_SETTINGS_MODULE'] = 'deviget.settings'
django.setup()


# TODO(Julian): Remove this and add proper test cases
# For quick, local testing
if __name__ == '__main__':
    PRINT_TENTEN_BEGIN = 50
    MAIN_BEGIN = 0
    from computer.models import Computer
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
    computer.set_address(MAIN_BEGIN)
    output = computer.execute()
    print('---')
    print('\n'.join('{}'.format(x) for x in output))
    print('---')
