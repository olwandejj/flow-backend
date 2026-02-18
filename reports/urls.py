from django.urls import path
from .views import SubmitReportView, dashboard_view

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='submit_report'),
    path('dashboard/', dashboard_view, name='dashboard'),
]