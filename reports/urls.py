from django.urls import path
from .views import SubmitReportView, dashboard_view, update_report_status

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='submit_report'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('<int:pk>/update-status/', update_report_status, name='update_status'),
]