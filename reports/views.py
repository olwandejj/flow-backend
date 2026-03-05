import os
import firebase_admin
from firebase_admin import credentials, messaging
from django.shortcuts import render
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ReportSerializer
from .models import Report, Feedback
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

# --- INITIALIZE FIREBASE ADMIN ---
# This looks for 'firebase-key.json' in your main project folder (next to manage.py)
if not firebase_admin._apps:
    try:
        cred_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'firebase-key.json')
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        print(f"Firebase Init Error: Ensure firebase-key.json is in the root directory. Error: {e}")

class SubmitReportView(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.AllowAny] 
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        # Safety check to ensure user is handled correctly if anonymous
        user = self.request.user if self.request.user.is_authenticated else None
        serializer.save(user=user)

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
            
            # --- ACTUAL FIREBASE PUSH NOTIFICATION TRIGGER ---
            if new_status == 'Resolved' and report.fcm_token:
                try:
                    # CHANGED: We removed 'notification=' and put everything inside 'data='
                    # This ensures the Android app stays in 100% control of the click behavior
                    message = messaging.Message(
                        data={
                            'title': 'Water Leak Repaired! 💧',
                            'body': f'Your report for a {report.category} has been resolved. Tap here to rate the repair!',
                            'report_id': str(report.id),
                            'action': 'rate_repair'
                        },
                        token=report.fcm_token,
                    )
                    response = messaging.send(message)
                    print(f"Successfully sent Firebase message: {response}")
                except Exception as e:
                    print(f"Error sending Firebase notification: {e}")
            
            return Response({'message': 'Status updated successfully!'})
            
        return Response({'error': 'No valid status provided'}, status=400)
        
    except Report.DoesNotExist:
        return Response({'error': 'Report not found'}, status=404)

# --- Submit Citizen Rating Endpoint ---
@api_view(['POST'])
@permission_classes([AllowAny]) # Allows Android app to post without logging in
def submit_rating(request, pk):
    try:
        report = Report.objects.get(pk=pk)
        rating = request.data.get('rating')
        comments = request.data.get('feedback')
        
        if not rating:
            return Response({'error': 'Rating is required'}, status=400)
            
        # Create or update the Feedback table entry linked to this Report
        Feedback.objects.update_or_create(
            report=report,
            defaults={'rating': int(rating), 'comments': comments}
        )
        
        return Response({'message': 'Thank you! Your feedback has been received.'})
    except Report.DoesNotExist:
        return Response({'error': 'Report not found'}, status=404)

class UserReportsView(generics.ListAPIView):
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only reports belonging to the logged-in user, newest first
        return Report.objects.filter(user=self.request.user).order_by('-timestamp')