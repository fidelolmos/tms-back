from rest_framework import serializers
from .models import Direction, Order, Route, TMS

class DirectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Direction
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

class TMSSerializer(serializers.ModelSerializer):
    class Meta:
        model = TMS
        fields = '__all__'
