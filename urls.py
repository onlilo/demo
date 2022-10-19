from django.contrib import admin
from django.urls import path

from .import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', views.health, name='health'),
    path('data2dB/',views.data2dB,name='data2dB'),
    path('login/', views.login, name='login'),
    path('get_devices/',views.device_list,name='device_list'),
    path('change_device/',views.update_device,name='update_device'),
]
