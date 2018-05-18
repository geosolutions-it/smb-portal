
from rest_framework import serializers
from .models import Vehicles, EndUser, prize, Tag, receipt


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicles
        exclude = []
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=EndUser
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