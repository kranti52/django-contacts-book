from django.contrib.auth.models import User
from rest_framework import serializers


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        validation_error = {}
        user = None
        try:
            user = User.objects.get(email=validated_data.get('email'))
            pw_check = user.check_password(validated_data.get('password'))
            if not pw_check:
                validation_error['email'] = [" Email and password doesn't match. "]
        except User.DoesNotExist as e:
            validation_error['email'] = [" Email and password doesn't match. "]

        if validation_error:
            raise serializers.ValidationError(validation_error)

        return user

    class Meta:
        model = User
        fields = ('email', 'password')
