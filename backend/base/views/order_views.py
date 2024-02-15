from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from base.models import Product, Order, OrderItem, ShippingAddress
from base.serializers import ProductSerializer, OrderSerializer

from rest_framework import status
from datetime import datetime

# paypal
from base.utils.calc_prices import calc_prices
from base.utils.paypal import verify_paypal_payment, check_if_new_transaction
from decouple import config
from django.http import JsonResponse

# Set up PayPal API credentials
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID")
PAYPAL_APP_SECRET = config("PAYPAL_APP_SECRET")
PAYPAL_API_URL = config("PAYPAL_API_URL")

def paypal_config(request):
    return JsonResponse({'clientId': PAYPAL_CLIENT_ID})

def update_order_to_paid(request, order_id):
    if request.method == 'POST':
        data = request.POST  # Adjust this if you're receiving JSON data
        payer_type = data.get('payer', '')

        # Dev testing: for production, handle this scenario based on your requirements
        if payer_type == 'test':
            order = get_object_or_404(Order, id=order_id)
            order.is_paid = True
            order.paid_at = timezone.now()
            order.payment_result = {
                'id': data.get('id', ''),
                'status': data.get('status', ''),
                'update_time': data.get('update_time', ''),
                'email_address': data.get('payer.email_address', ''),
            }
            order.save()

            return JsonResponse({'message': 'Order updated for testing'})

        try:
            verified, value = verify_paypal_payment(data.get('id', ''))

            if not verified:
                raise ValueError('Payment not verified')

            # Check if this transaction has been used before
            is_new_transaction = check_if_new_transaction(Order, data.get('id', ''))
            if not is_new_transaction:
                raise ValueError('Transaction has been used before')

            order = get_object_or_404(Order, id=order_id)

            if order:
                # Check if the correct amount was paid
                paid_correct_amount = str(order.total_price) == value
                if not paid_correct_amount:
                    raise ValueError('Incorrect amount paid')

                order.is_paid = True
                order.paid_at = timezone.now()
                order.payment_result = {
                    'id': data.get('id', ''),
                    'status': data.get('status', ''),
                    'update_time': data.get('update_time', ''),
                    'email_address': data.get('payer.email_address', ''),
                }
                order.save()

                return JsonResponse({'message': 'Order updated successfully'})

            else:
                return JsonResponse({'error': 'Order not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addOrderItems(request):
    user = request.user
    # print("addOrderItems user: " + str(user))
    data = request.data
    # print("addOrderItems data: " + str(data))

    orderItems = data['orderItems']
    # print("addOrderItems orderItems: " + str(orderItems))

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:

        # (1) Create order

        order = Order.objects.create(
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )

        # print("addOrderItems order: " + str(order))

        # (2) Create shipping address

        shipping = ShippingAddress.objects.create(
            order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

        # print("addOrderItems shipping: " + str(shipping))

        for i in orderItems:
            try:
                product_id = i['_id']
            except KeyError:
                print("Error: 'product' key is missing in order item:", i)
                return Response({'detail': 'Product ID is missing in order item'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                product = Product.objects.get(_id=product_id)
            except Product.DoesNotExist:
                print(f"Error: Product with _id {product_id} does not exist")
                return Response({'detail': f'Product with _id {product_id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            item = OrderItem.objects.create(
                product=product,
                order=order,
                name=product.name,
                qty=i.get('qty', 1),  # Provide a default value if 'qty' is missing
                price=i.get('price', 0),  # Provide a default value if 'price' is missing
                image=product.image.url,
            )
            print("addOrderItems item: " + str(item))

            # (4) Update stock

            # product.countInStock -= item.qty
            # product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateOrderToPaid(request, pk):
    order = Order.objects.get(_id=pk)

    order.isPaid = True
    order.paidAt = datetime.now()
    order.save()

    return Response('Order was paid')


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateOrderToDelivered(request, pk):
    order = Order.objects.get(_id=pk)

    order.isDelivered = True
    order.deliveredAt = datetime.now()
    order.save()

    return Response('Order was delivered')