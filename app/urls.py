# -*- coding: utf-8 -*-
"""investment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from channels.routing import route
import app.views as app_views
# 单进程路由
# import app.routings_sp as app_routings
# 多进程路由
import app.routings_mp as app_routings

urlpatterns = [
    url(r'^$', app_views.index),
    url(r'get_presets$', app_views.get_presets),
]

channel_routing = [
    route("websocket.connect", app_routings.ws_connect),
    route("websocket.receive", app_routings.ws_receive),
    route("websocket.disconnect", app_routings.ws_disconnect),
]