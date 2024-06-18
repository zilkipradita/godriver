from rest_framework import serializers 
from driver.models import Users_roles
from driver.models import Users 
from driver.models import Trips 
from driver.models import Order_trips 
 
class Users_rolesSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Users_roles
        fields = ('id','name')

class Users_Serializer(serializers.ModelSerializer):
 
    class Meta:
        model = Users
        fields = ('id','username','password','name','telp','email','users_roles')

class Trips_Serializer(serializers.ModelSerializer):
 
    class Meta:
        model = Trips
        fields = ('id','destination','location','status','users','cost','created_at','updated_at')

class Order_tripsSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Order_trips
        fields = ('id','trips','driver')

class User_loginSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Users
        fields = ('username','password')

class Create_userSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Users
        fields = ('username','password','name','telp','email','users_roles')

class Create_tripsSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Trips
        fields = ('destination','location','users')

class Takes_orderSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Order_trips
        fields = ('trips','driver')