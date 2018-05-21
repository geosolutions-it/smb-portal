
from rest_framework import serializers
from .models import Vehicle, User, prize, Tag, receipt


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        exclude = []
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        exclude= []
        
        
class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model= prize
        exclude = []
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = []
        
        
class ReceiptSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = receipt
        exclude = []