from rest_framework import serializers
from .models import Report, Location, Image

class ReportSerializer(serializers.ModelSerializer):
    # --- WRITE ONLY (Inputs from Android) ---
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    accuracy = serializers.FloatField(write_only=True)
    image_file = serializers.ImageField(write_only=True)

    class Meta:
        model = Report
        fields = ['id', 'category', 'severity', 'status', 'timestamp', 
                  'latitude', 'longitude', 'accuracy', 'image_file']
        read_only_fields = ['status', 'timestamp']

    # --- 1. CREATE (Android Upload) ---
    def create(self, validated_data):
        # Pop the extra fields
        lat = validated_data.pop('latitude')
        long = validated_data.pop('longitude')
        acc = validated_data.pop('accuracy')
        img = validated_data.pop('image_file')

        # Create Report
        report = Report.objects.create(**validated_data)

        # Create Location
        Location.objects.create(
            report=report, 
            latitude=lat, 
            longitude=long, 
            accuracy=acc
        )

        # Create Image
        Image.objects.create(
            report=report, 
            file_path=img
        )

        return report

    # --- 2. REPRESENTATION (Dashboard Display) ---
    def to_representation(self, instance):
        # Start with standard data
        data = super().to_representation(instance)
        
        # Add GPS Data manually
        if hasattr(instance, 'location'):
            data['latitude'] = instance.location.latitude
            data['longitude'] = instance.location.longitude
        
        # Add Image URL manually
        if hasattr(instance, 'image') and instance.image.file_path:
            # This creates a full URL (http://...) for the browser
            request = self.context.get('request')
            if request:
                data['image_file'] = request.build_absolute_uri(instance.image.file_path.url)
            else:
                data['image_file'] = instance.image.file_path.url
                
        return data