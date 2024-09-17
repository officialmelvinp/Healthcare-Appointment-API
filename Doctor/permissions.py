from rest_framework import permissions

class IsDoctorOrNone(permissions.BasePermission):
    """
    Custom permission to allow only doctors to edit their own profile and restrict non-doctors from performing unsafe methods.
    """

    def has_permission(self, request, view):
        # Allow safe methods (GET, HEAD, OPTIONS) for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow unsafe methods only for authenticated users who have a doctor profile
        return request.user.is_authenticated and hasattr(request.user, 'doctor_from_doctor_app')

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Allow unsafe methods only if the user is authenticated, is a doctor, and owns the profile
        return (
            request.user.is_authenticated and 
            hasattr(request.user, 'doctor_from_doctor_app') and 
            request.user.doctor_from_doctor_app == obj
        )
