from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ReportSerializer
from .models import Report
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

class SubmitReportView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny] 
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # This automatically gets the user from the Token!
        serializer.save(user=self.request.user)

@login_required(login_url='/login/')
def dashboard_view(request):
    return render(request, 'reports/dashboard.html')