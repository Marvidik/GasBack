from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *



#  user serializer
class SalesSerializer(serializers.ModelSerializer):
    referral_name = serializers.CharField(required=False, allow_blank=True)
    class Meta(object):
        model = Sales
        fields = "__all__"


#  user serializer
class ProductSerializer(serializers.ModelSerializer):
    referral_name = serializers.CharField(required=False, allow_blank=True)
    class Meta(object):
        model = Product
        fields = "__all__"


#  user serializer
class ExpensesSerializer(serializers.ModelSerializer):
    referral_name = serializers.CharField(required=False, allow_blank=True)
    class Meta(object):
        model = Expenses
        fields = "__all__"