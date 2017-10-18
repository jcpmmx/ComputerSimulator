# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import serializers

from computer.models import Computer, ProgramStack


class ComputerSerializer(serializers.ModelSerializer):
    """
    Serializer to manage `Computer` instances.
    """
    stack = serializers.IntegerField(write_only=True, help_text="Size of the computer's program stack")

    class Meta:
        model = Computer
        fields = ('id', 'stack')

    def create(self, validated_data):
        """
        This method uses some custom calls to bypass the fact our __init__ methods in `Computer` and `ProgramStack` have
        custom values.
        """
        stack_size = validated_data['stack']
        ps = ProgramStack(stack_size=stack_size)
        ps.save()
        computer = Computer(stack_size=stack_size)
        computer.program_stack = ps
        computer.save()
        return computer
