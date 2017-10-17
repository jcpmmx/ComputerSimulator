# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from django.conf.urls import include, url

from api import urls


urlpatterns = [
    url(r'^v1/computers', include(urls)),
]
