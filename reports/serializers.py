from rest_framework import serializers
from .models import Report, Location, Image

class ReportSerializer(serializers.ModelSerializer):
    # We explicitly define these fields to accept data from the App
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    accuracy = serializers.FloatField(write_only=True)
    image_file = serializers.ImageField(write_only=True)

    class Meta:
        model = Report
        fields = ['id', 'category', 'severity', 'status', 'timestamp', 
                  'latitude', 'longitude', 'accuracy', 'image_file']
        read_only_fields = ['status', 'timestamp']

    def create(self, validated_data):
        # 1. Extract the nested data
        lat = validated_data.pop('latitude')
        long = validated_data.pop('longitude')
        acc = validated_data.pop('accuracy')
        img = validated_data.pop('image_file')

        # 2. Create the Report (The "Parent")
        report = Report.objects.create(**validated_data)

        # 3. Create the Location (The "Child")
        Location.objects.create(
            report=report, 
            latitude=lat, 
            longitude=long, 
            accuracy=acc
        )

        # 4. Create the Image (The "Child")
        Image.objects.create(
            report=report, 
            file_path=img
        )

        return report