from rest_framework import serializers

from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the create user object"""

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'password'
        )
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'style': {
                    'input_type': 'password'
                }
            }
        }

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)


class DisplayUserSerializer(serializers.ModelSerializer):
    """Serializer for display user object"""

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'age',
            'biography'
        )
