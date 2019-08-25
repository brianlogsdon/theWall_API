from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.mail import send_mail
from django.contrib.auth.models import User
from rest_framework_jwt.settings import api_settings
from core.models import Messages
from django.conf import settings

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            
            )
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8)

    token = serializers.SerializerMethodField()
    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
             validated_data['password'])
        send_mail('Welcome to the Wall', 'Welcome to the wall, log in and leave a message. ', settings.EMAIL_HOST_USER, [user.email], fail_silently=False)     
        return user

    class Meta:
        model = User
        fields = ('id','token', 'username', 'email', 'password')

   
class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        exclude = ()
