from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *



#  user serializer
class SalesSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='goods.name', read_only=True)
    class Meta(object):
        model = Sales
        fields = "__all__"



class OtherProductsSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = OtherProducts
        fields = "__all__"


#  user serializer
class ProductSerializer(serializers.ModelSerializer):
  
    class Meta(object):
        model = Product
        fields = "__all__"


#  user serializer
class ExpensesSerializer(serializers.ModelSerializer):
 
    class Meta(object):
        model = Expenses
        fields = "__all__"