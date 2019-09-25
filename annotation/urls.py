from django.urls import path
from . import views

app_name = 'annotation'

urlpatterns = [
    path('', views.FunctionAnnView.as_view(), name='ann_table'),
]
