from rest_framework import permissions

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permission for UserViewSet: Users can only edit their own data.
    """
    def has_permission(self, request, view):
        # Allow all users to GET or POST
        if request.method in ['GET', 'POST']:
            return True
        # Allow only authenticated users for other methods
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow object edits only if the user is the owner
        return request.user == obj

class IsDoctorOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for DoctorViewSet: Doctors can edit their own profile.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow edits only if the request user matches the doctor profile's user
        return request.user == obj.user

class IsPatientProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission for PatientProfileViewSet: Users can edit their own profile.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        # Allow safe methods for all users
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow edits only if the request user matches the patient profile's user
        return request.user == obj.user
