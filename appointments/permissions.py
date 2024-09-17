from rest_framework.permissions import BasePermission

class IsPatientOrAdmin(BasePermission):
    """
    Custom permission to allow only patients to create appointments.
    Admins can manage all appointments.
    """
    def has_permission(self, request, view):
        # Admins can create and manage all appointments
        if request.user.is_staff:
            return True

        # Only allow authenticated users with a patient profile to create appointments
        if request.user.is_authenticated:
            if request.method == 'POST':
                # Debugging: Log user info and check for patient profile
                print(f"User {request.user.username} is authenticated with is_patient: {request.user.is_patient}")
                return hasattr(request.user, 'patient_profile')
            
            # Allow GET requests for authenticated users (e.g., viewing appointments)
            return True

        return False

    def has_object_permission(self, request, view, obj):
        # Admins have access to all appointments
        if request.user.is_staff:
            return True

        # Patients can only access their own appointments
        if request.user.is_authenticated and hasattr(request.user, 'patient_profile'):
            if request.method in ['GET', 'DELETE'] and obj.patient == request.user.patient_profile:
                return True

        return False

class CanEditAppointment(BasePermission):
    """
    Custom permission to restrict editing appointments based on status.
    """
    def has_object_permission(self, request, view, obj):
        # Admins can edit appointments regardless of status
        if request.user.is_staff:
            return True

        # Only allow editing if the status is not 'completed'
        if request.method in ['PUT', 'PATCH']:
            return obj.status != 'completed'

        return True
