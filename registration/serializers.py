
from rest_framework import serializers
from .models import bike, EndUser, prize, Tag, receipt


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=bike
        exclude = []
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=EndUser
        exclude= ['password']
        
        
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