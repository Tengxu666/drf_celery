from django.contrib import admin
from django.urls import path

import message.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('send_code', message.views.async_send_code),
    path('order_kill', message.views.order_seconds_kill)
]
