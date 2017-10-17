# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import serializers


class ComputerSerializer(serializers.Serializer):
    """
    Serializer to manage `Computer` instances.
    """
    id = serializers.IntegerField(read_only=True, help_text="ID of the computer")

    stack = serializers.IntegerField(write_only=True, help_text="Size of the computer's program stack")

    def to_internal_value(self, data):
        score = data.get('score')
        player_name = data.get('player_name')
