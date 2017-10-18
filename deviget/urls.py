# -*- coding: utf-8 -*-


from __future__ import print_function, unicode_literals

from django.conf.urls import include, url

from api.urls import router


urlpatterns = [
    url(r'^v1/', include(router.urls)),
]
