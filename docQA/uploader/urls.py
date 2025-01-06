from django.urls import path
from . import views

urlpatterns = [
    path('', views.upload_document, name='upload'),  # Root page mapped to upload
    path('success/', views.upload_success, name='upload_success'),
]
