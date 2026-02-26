from django.contrib.auth.models import User
from rest_framework import serializers
from resources.models import Department

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    department = serializers.ChoiceField(choices=Department.choices,required=True, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'department']

    def create(self, validated_data):
        dept = validated_data.pop('department')
        
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        
        user.profile.department = dept
        user.profile.save()
        
        return user