from django.shortcuts import render

# Create your views here.

# from .products import products // from hardcoded file
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAdminUser

from base.models import (Product, User)
from base.serializers import *

from rest_framework import status

@api_view(['GET'])
def getProducts(request):
	products = Product.objects.all()
	serializer = ProductSerializer(products, many=True)
	return Response(serializer.data)

@api_view(['GET'])
def getProduct(request, pk):
	product = Product.objects.get(_id=pk)
	print('product', product)
	serializer = ProductSerializer(product, many=False)
	print('serializer', serializer)
	return Response(serializer.data)