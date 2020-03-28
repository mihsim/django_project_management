from django.shortcuts import render

# Create your views here.
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
 path('', TemplateView.as_view(template_name="project_app/index.html")),
 path('admin/', admin.site.urls),
 path('accounts/', include('allauth.urls'))
]