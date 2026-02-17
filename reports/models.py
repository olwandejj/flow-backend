from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# 2. Reports Table
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(max_length=50) # e.g., Burst Pipe
    severity = models.CharField(max_length=20) # e.g., High
    status = models.CharField(max_length=20, default='New')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'reports'

# 3. Locations Table (1-to-1 with Report)
class Location(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='location')
    latitude = models.FloatField()
    longitude = models.FloatField()
    accuracy = models.FloatField()
    
    # We add this purely for the "Geospatial Dashboard" requirement
    # but the schema mainly relies on the lat/long floats above.
    
    class Meta:
        db_table = 'locations'

# 4. Images Table (1-to-1 with Report)
class Image(models.Model):
    report = models.OneToOneField(Report, on_delete=models.CASCADE, related_name='image')
    file_path = models.ImageField(upload_to='damage_images/') 
    metadata = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'images'