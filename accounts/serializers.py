from rest_framework import serializers
from .models import CustomUser, Role


class CustomUserSerializer(serializers.ModelSerializer):
    """
    CustomUserSerializer handles the serialization of user data.

    It includes fields for user details and role_id.
    """
    role_id = serializers.UUIDField()
    school_id = serializers.UUIDField()
    school_name = serializers.CharField(source='school.school_name', read_only=True)
    role_name = serializers.CharField(source='role.role_name', read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['id', 
                  'first_name', 
                  'last_name', 
                  'email',
                  'password',
                  'role_id',
                  'role_name',
                  'school_id', 
                  'school_name']
        
    def create(self, validated_data):
        """
        Create a new user instance and set the password.
        """
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    
    def update(self, instance, validated_data):
        """
        Update the user instance with the provided validated data.
        """
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance


class RoleSerializer(serializers.ModelSerializer):
    """
    RoleSerializer handles the serialization of role data.
    """
    class Meta:
        model = Role
        fields = ["role_id", "role_name"]


class UserResetPasswordSerailizer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["password"]