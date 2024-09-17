from django.contrib import admin
from .models import Appointment
from django import forms

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
        }

class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__user__username', 'doctor__user__username')
    ordering = ('-date', '-time')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new appointment
            if request.user.is_superuser:
                # Admin can create appointment for any patient
                pass
            else:
                # Ensure user has a PatientProfile
                try:
                    patient_profile = request.user.patientprofile
                except AttributeError:
                    raise ValueError("User does not have an associated PatientProfile")
                
                # Assign patient profile to the appointment
                obj.patient = patient_profile
        
        super().save_model(request, obj, form, change)

admin.site.register(Appointment, AppointmentAdmin)
class AppointmentAdmin(admin.ModelAdmin):
    form = AppointmentForm
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__user__username', 'doctor__user__username')
    ordering = ('-date', '-time')
    readonly_fields = ('created_at', 'updated_at')

    # Comment out this method temporarily
    # def save_model(self, request, obj, form, change):
    #     if not change:  # If creating a new appointment
    #         if request.user.is_superuser:
    #             # Admin can create appointment for any patient
    #             pass
    #         else:
    #             # Ensure user has a PatientProfile
    #             try:
    #                 patient_profile = request.user.patientprofile
    #             except AttributeError:
    #                 raise ValueError("User does not have an associated PatientProfile")
                
    #             # Assign patient profile to the appointment
    #             obj.patient = patient_profile
        
    #     super().save_model(request, obj, form, change)
