from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload-file/', views.upload_file, name='upload_file'),
    path('query-data/', views.query_data, name='query_data'),
    path('vat-summary/', views.vat_summary, name='vat_summary'),
]
