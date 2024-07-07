from django.urls import path

from wc_tool import views

urlpatterns = [
    path('wc/', views.wc_view, name='wc_view'),
    path('batch_wc/', views.batch_wc_view, name='batch_wc_view'),
]