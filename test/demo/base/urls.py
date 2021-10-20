# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from django.urls import path

urlpatterns = [
    path('api/', include('dms2.urls.api')),
    path('adm/', include('dms2.urls.adm')),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
