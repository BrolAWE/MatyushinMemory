"""MatyushinMemory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views import color_table, start_test, memory_test, export_xls, update_database

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', start_test, name='start_test'),
    path('table/<str:table_pk>/<str:member_pk>', color_table, name='color_table'),
    path('memory_test/<str:table_pk>/<str:member_pk>', memory_test, name='memory_test'),
    path('export_xls/', export_xls, name='export_xls'),
    path('update_database/', update_database, name='update_database'),
]
