from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, DoctorsProfile, PatientProfile

# Inline admin classes to display DoctorsProfile and PatientProfile in the User admin page
class DoctorsProfileInline(admin.StackedInline):
    model = DoctorsProfile
    can_delete = False
    verbose_name_plural = 'Doctors Profile'

class PatientProfileInline(admin.StackedInline):
    model = PatientProfile
    can_delete = False
    verbose_name_plural = 'Patients Profile'

# Custom User admin to include inline profiles
class CustomUserAdmin(BaseUserAdmin):
    inlines = (DoctorsProfileInline, PatientProfileInline)
    list_display = ('username', 'email', 'is_patient', 'is_doctor', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_patient', 'is_doctor', 'is_staff', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Roles', {'fields': ('is_patient', 'is_doctor')}),
    )
    readonly_fields = ('id',)  # Add id as read-only if needed

# Registering the User model with the custom admin
admin.site.register(User, CustomUserAdmin)

# Separate admin for DoctorsProfile
class DoctorsProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization')
    search_fields = ('user__username', 'specialization')

# Separate admin for PatientProfile
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth')
    search_fields = ('user__username', 'date_of_birth')

# Register the profiles
admin.site.register(DoctorsProfile, DoctorsProfileAdmin)
admin.site.register(PatientProfile, PatientProfileAdmin)
















