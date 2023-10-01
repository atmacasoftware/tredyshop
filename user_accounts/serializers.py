from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from user_accounts.models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','mobile']
        extra_Kwargs = {
            'password':{'write_only':True}
        }

    def validate(self, attrs):
        email = attrs.get('email')
        is_exists = User.objects.filter(email=email).first()
        if is_exists:
            raise serializers.ValidationError("Bu email adresi ile kullanıcı mevcut.")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(is_superuser=False,is_staff=False, is_customer=True, **validated_data)


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    mobile = serializers.CharField()
    # username = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = '__all__'

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'mobile': self.validated_data.get('mobile', '')
        }
