# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import ComputerSerializer
from computer.enums import ComputerInstruction
from computer.models import Computer


class ComputerViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    API view to manage `Computer` instances.
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer

    @detail_route(methods=['patch'], url_path='stack/pointer')
    def pointer(self, request, pk=None):
        """
        Custom route to invoke the `set_address` method of a `Computer`.
        """
        addr = int(request.data.get('addr'))
        if addr:
            computer = self.get_object()
            computer.set_address(addr)
            computer.save()
        return Response()

    @detail_route(methods=['post'], url_path='stack/insert/(?P<possible_instruction>[^/.]+)')
    def insert(self, request, pk=None, possible_instruction=None):
        """
        Custom route to invoke the `insert` method of a `Computer`.
        """
        instruction = ComputerInstruction.get_value(possible_instruction)
        if instruction:
            arg_name = 'addr' if instruction == ComputerInstruction.CALL else 'arg'
            instruction_arg = request.data.get(arg_name)
            computer = self.get_object()
            computer.insert(possible_instruction, instruction_arg=instruction_arg)
            computer.save()
        return Response()

    @detail_route(methods=['post'], url_path='exec')
    def execute(self, request, pk=None):
        """
        Custom route to invoke the `execute` method of a `Computer`.
        """
        computer = self.get_object()
        return Response(computer.execute())

    @detail_route(methods=['post'], url_path='debug')
    def debug(self, request, pk=None):
        """
        Custom route to invoke the `debug` method of a `Computer`.
        """
        computer = self.get_object()
        return Response(computer.debug())
