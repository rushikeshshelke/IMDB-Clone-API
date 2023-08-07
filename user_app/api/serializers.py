from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(style={'input_type': 'password'},write_only=True)
    
    class Meta:
        model = User
        fields = ["username","email","password","confirm_password"]
        extra_kwargs = {
            "password" : {"write_only": True}
        }
    
    def save(self):
        
        password = self.validated_data.get('password')
        confirm_password = self.validated_data.get('confirm_password')
        
        if password != confirm_password:
            raise serializers.ValidationError({'error':'Password and Confirm Password should be same!'})
        
        if User.objects.filter(email=self.validated_data.get('email')).exists():
            raise serializers.ValidationError({'error':'Email already exists'})
        
        account = User(
            email=self.validated_data.get('email'),
            username=self.validated_data.get('username')
            )
        account.set_password(password)
        account.save()
        
        return account