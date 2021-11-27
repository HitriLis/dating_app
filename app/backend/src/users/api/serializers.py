from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'password', 'avatar')

    def get_avatar(self, obj):
        return self.context['request'].build_absolute_uri(obj.get_avatar())

    def validate(self, attrs):
        if self.instance is None and len(attrs.get('password', '')) < 5:
            raise serializers.ValidationError({
                'password': 'При создании пользователя необходимо указать пароль'
            })
        return attrs

    def save(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )
        validated_data['password'] = make_password(validated_data['password'])

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
        else:
            self.instance = self.create(validated_data)

        return self.instance
