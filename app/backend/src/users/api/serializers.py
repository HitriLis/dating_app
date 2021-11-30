from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from common import add_watermark

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'password', 'avatar', 'longitude', 'latitude')

    def get_avatar(self, obj):
        return self.context['request'].build_absolute_uri(obj.get_avatar())

    def save(self, **kwargs):
        validated_data = dict(
            list(self.validated_data.items()) +
            list(kwargs.items())
        )

        validated_data['password'] = make_password(validated_data['password'])
        if 'avatar' in validated_data:
            image = validated_data['avatar']
            validated_data['avatar'] = add_watermark(image)

        if self.instance is not None:
            self.instance = self.update(self.instance, validated_data)
        else:
            self.instance = self.create(validated_data)

        return self.instance


class UserSerializerSimple(serializers.ModelSerializer):
    distance = serializers.IntegerField(min_value=0)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'gender', 'avatar', 'distance')
        read_only_fields = ('email', 'first_name', 'last_name', 'gender', 'avatar', 'distance')
