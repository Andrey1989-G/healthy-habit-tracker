from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для юзера"""

    class Meta:
        model = User
        fields = ['email', 'password', 'chat_id', 'is_active']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            chat_id=validated_data['chat_id'],
            is_staff=False,
            is_superuser=False,
            is_active=True
        )

        user.set_password(validated_data['password'])
        user.save()
        return user