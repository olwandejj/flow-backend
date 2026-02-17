from django.urls import path
from .views import SubmitReportView

urlpatterns = [
    path('submit/', SubmitReportView.as_view(), name='submit_report'),
]