from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ReportSerializer
from .models import Report
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_report_status(request, pk):
    try:
        report = Report.objects.get(pk=pk)
        new_status = request.data.get('status')
        
        if new_status:
            report.status = new_status
            report.save()
            return Response({'message': 'Status updated successfully!'})
            
        return Response({'error': 'No valid status provided'}, status=400)
        
    except Report.DoesNotExist:
        return Response({'error': 'Report not found'}, status=404)