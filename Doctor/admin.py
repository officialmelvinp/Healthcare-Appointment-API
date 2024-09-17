from django.contrib import admin
from .models import Doctor

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    # Display these fields in the list view of the admin panel
    list_display = ('name', 'specialization', 'availability')
    
    # Add filters for these fields to easily filter doctors by specialization and availability
    list_filter = ('specialization', 'availability')
    
    # Enable searching by name and specialization fields
    search_fields = ('name', 'specialization')
    
    # Order the list of doctors by name by default
    ordering = ('name',)
    
    # Define the fields to be displayed in the form view in a custom order
    fields = ('name', 'specialization', 'availability')
    
    # Make the ID field read-only to prevent accidental changes
    readonly_fields = ('id',)
