
from rest_framework import serializers
from .models import Prize, Receipt
from smbportal.vehicles.models import Vehicle, Tag
from smbportal.profiles.models import EndUserProfile

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vehicle
        exclude = []
        
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=EndUserProfile
        exclude= []
        
        
class PrizeSerializer(serializers.ModelSerializer):
    class Meta:
        model= Prize
        exclude = []
        

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = []
        
        
class ReceiptSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Receipt
        exclude = []