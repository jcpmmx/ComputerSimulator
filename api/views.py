# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import mixins
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import ComputerSerializer
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
        return Response()

    @detail_route(methods=['post'], url_path='stack/insert/(?P<possible_instruction>[^/.]+)')
    def insert(self, request, pk=None, possible_instruction=None):
        """
        Custom route to invoke the `insert` method of a `Computer`.
        """
        instruction_arg = int(request.data.get('arg'))  # Assuming only ints as possible args to instructions
        if possible_instruction:
            computer = self.get_object()
            computer.insert(possible_instruction, instruction_arg=instruction_arg)
        return Response({'asd': 123})

    @detail_route(methods=['patch'], url_path='exec')
    def execute(self, request, pk=None):
        """
        Custom route to invoke the `execute` method of a `Computer`.
        """
        computer = self.get_object()
        return Response(computer.execute())
