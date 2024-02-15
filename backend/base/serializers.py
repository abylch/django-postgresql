from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Product, Order, OrderItem, ShippingAddress, Review


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    _id = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin']

    def get__id(self, obj):
        return obj.id

    def get_isAdmin(self, obj):
        return obj.is_staff

    def get_name(self, obj):
        name = obj.first_name
        if name == '':
            name = obj.email

        return name


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', '_id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj):
        print(obj)
        token = RefreshToken.for_user(obj)
        print("from serializers.py get_token token.access_token: " + str(token.access_token))
        return str(token.access_token)


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    shippingAddress = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shippingAddress(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shippingaddress, many=False).data
        except:
            address = False
        return address

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data

# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import *
# from rest_framework_simplejwt.tokens import RefreshToken



# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = '__all__'

# class UserSerializer(serializers.ModelSerializer):
#     name = serializers.SerializerMethodField(read_only=True)
#     _id = serializers.SerializerMethodField(read_only=True)
#     isAdmin = serializers.SerializerMethodField(read_only=True)
    
#     # get name from first_name and last_name, if both are empty, return email
#     # if both are not empty, return first_name + last_name
#     # if first_name is empty, return last_name
#     # if last_name is empty, return email
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin']

#     def get_name(self, obj):
#         name = obj.first_name + ' ' + obj.last_name
#         if name == ' ':
#             return obj.email
#         else:
#             return name
        
#     def get__id(self, obj):
#         return obj.id

#     def get_isAdmin(self, obj):
#         return obj.is_staff

# class UserSerializerWithToken(UserSerializer):
#     token = serializers.SerializerMethodField(read_only=True)
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'name', '_id', 'isAdmin', 'token']
#     def get_token(self, obj):
#         token = RefreshToken.for_user(obj)
#         print(obj)
#         print("from serializers.py get_token token.access_token: " + str(token.access_token))
#         return str(token.access_token)