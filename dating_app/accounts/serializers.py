from rest_framework import serializers

from .models import City,User

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id','name']


class UserSerializer(serializers.ModelSerializer):
    city = CitySerializer(read_only=True)
    age = serializers.ReadOnlyField()
    gender_display = serializers.CharField(source='get_gender_display',read_only=True)

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','bio','city','age','gender_display','avatar']
        

