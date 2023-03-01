from rest_framework import serializers
from users.models import User


class UserCreationSerializer(serializers.ModelSerializer):
    """."""

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)

    class Meta:
        """."""

        model = User
        fields = ('username', 'email')

    def validated_username(self, value):
        """."""
        username = value.lower()
        if username == 'me':
            raise serializers.ValidationError('me недопустимо')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                'Такой пользователь с именем существует.'
            )

        return value

    def validate_email(self, value):
        """."""
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('Такой email существует.')
        return value


class UserSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        """."""

        model = User
        fields = (
            'username', 'email', 'bio', 'role', 'confirmation_code'
        )
