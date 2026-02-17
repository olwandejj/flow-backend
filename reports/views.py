from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ReportSerializer
from .models import Report
from django.contrib.auth.models import User

class SubmitReportView(generics.CreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny] 
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # 1. Try to get the existing admin user
        user = User.objects.first()
        
        # 2. SAFETY NET: If no user exists, create one on the fly
        if not user:
            print("WARNING: No user found. Creating 'admin' automatically.")
            user = User.objects.create_superuser('admin', 'admin@flow.com', 'password123')
            
        # 3. Save the report with this user
        serializer.save(user=user)