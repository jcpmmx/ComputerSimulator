# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import serializers

from computer.models import Computer


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
        Creates a new `Computer` instance via API.
        """
        validated_data['program_stack_size'] = validated_data.pop('stack', 0)
        return super(ComputerSerializer, self).create(validated_data)
