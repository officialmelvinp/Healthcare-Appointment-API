from rest_framework import permissions #giving partial permission(POST, GET) to first time users who dont have an account yet

class IsUserOwnerOrGetAndPostOnly(permissions.BasePermission):
    """
    Custom permissions for UserViewSet to only allow user to edit their own user. Othwerwise, Get and Post Only.
    """

    def has_permission(self, request, view): #endpoints that deals with get and post for non user
        return True

    def has_object_permission(self, request, view, obj): #put # to check if the user owns it

        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user.is_anonymous: #this is to make non user not able to put request
            return request.user == obj

        return False
    
    #after permission we move back to the view set to import

class IsProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for ProfileViewSet to only allow user to edit their own profile. Otherwise, Get and Post Only.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            # Adjust based on your actual field or related name
            return getattr(request.user, 'doctor_profile', None) == obj
    
        return False
    
    
    
class IsPatientProfileOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permissions for PatientProfileViewSet to only allow users to edit their own profile. Otherwise, Get and Post Only.
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if not request.user.is_anonymous:
            # Adjust based on your actual field or related name
            return getattr(request.user, 'patient_profile', None) == obj
        return False


    
    #after permisions we move back to the viewset to load