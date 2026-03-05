from django.urls import path
from .views import SubmitReportView, dashboard_view, update_report_status, submit_rating, UserReportsView

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='submit_report'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('<int:pk>/update-status/', update_report_status, name='update_status'),
    path('<int:pk>/rate/', submit_rating, name='submit_rating'),
    path('my-reports/', UserReportsView.as_view(), name='my_reports'),
]