from  rest_framework.serializers import ModelSerializer
from .models import *
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email', 'phone','first_name', 'last_name', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class CategorySerializer(ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"

class ProductSerializer(ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"

class UserDetailsSerializer(ModelSerializer):
    class Meta:
        model=UserProfile
        exclude=['user']

 
class UserProductSerializer(ModelSerializer):
    class Meta:
        model = UserProduct
        exclude = ['user']

class UserList(ModelSerializer):
    class Meta:
        model=User
        fields=['username']

class ProductList(ModelSerializer):
    class Meta:
        model=Product
        fields=['name','price','discription']

class UserProductListSerializer(ModelSerializer):
    user=UserList()
    product=ProductList()
    class Meta:
        model = UserProduct
        fields = "__all__"

class MyTokenObtainPairSerializer(TokenObtainSerializer):
    token_class = RefreshToken

    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


    
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)