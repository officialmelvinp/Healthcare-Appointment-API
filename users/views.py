from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class LogoutView(APIView):
    def post(self, request):
        # Handle session logout
        logout(request)

        # Handle token logout (OAuth2)
        token = request.auth
        if token:
            token.delete()
            return Response({"detail": "Successfully logged out from session and token."}, status=status.HTTP_200_OK)
        
        return Response({"detail": "Successfully logged out from session."}, status=status.HTTP_200_OK)
