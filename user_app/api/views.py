from rest_framework.decorators import api_view
from user_app.api.serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
# from rest_framework.authtoken.models import Token
# from user_app import models
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(["POST"])
def registration_view(request):
    
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            status_code = status.HTTP_201_CREATED
            data['username'] = account.username
            data['email'] = account.email
            
            # token = Token.objects.get(user=account).key
            # data['token'] = token
            refresh = RefreshToken.for_user(account)
            
            data['token'] = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
            
            data['response'] = "Registration Successful!"
        else:
            data = serializer.errors
            status_code = status.HTTP_400_BAD_REQUEST
        
        return Response(data, status=status_code)

@api_view(["POST"])
def logout_view(request):
    
    if request.method == "POST":
        request.user.auth_token.delete()
        content = {"message":"Logged out successfully!"}
        return Response(content,status=status.HTTP_200_OK)