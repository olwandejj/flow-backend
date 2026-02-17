from django.contrib import admin
from .models import Report, Location, Image

# 1. Setup Location to appear inside the Report page
class LocationInline(admin.StackedInline):
    model = Location
    extra = 0  # Don't show empty extra rows

# 2. Setup Image to appear inside the Report page
class ImageInline(admin.StackedInline):
    model = Image
    extra = 0

# 3. Configure the Main Report List
class ReportAdmin(admin.ModelAdmin):
    # These fields match your models.py EXACTLY:
    list_display = ('id', 'category', 'severity', 'status', 'user', 'timestamp')
    
    # Add filters for easier searching
    list_filter = ('severity', 'status', 'timestamp')
    
    # Add a search bar
    search_fields = ('category', 'user__username')

    # This magic line puts the Location and Image sections inside the Report detail view
    inlines = [LocationInline, ImageInline]

# 4. Register it!
admin.site.register(Report, ReportAdmin)