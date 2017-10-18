# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.serializers import ComputerSerializer
from computer.models import Computer


class ComputerViewset(mixins.CreateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """
    API view to manage `Computer` instances.
    """
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
