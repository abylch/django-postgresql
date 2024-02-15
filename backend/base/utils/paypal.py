import os
import requests
from decouple import config

# Set up PayPal API credentials
PAYPAL_CLIENT_ID = config("PAYPAL_CLIENT_ID")
PAYPAL_APP_SECRET = config("PAYPAL_APP_SECRET")
PAYPAL_API_URL = config("PAYPAL_API_URL")

def get_paypal_access_token():
    # Authorization header requires base64 encoding
    auth = f"{PAYPAL_CLIENT_ID}:{PAYPAL_APP_SECRET}"
    auth_base64 = b64encode(auth.encode()).decode('utf-8')

    url = f"{PAYPAL_API_URL}/v1/oauth2/token"

    headers = {
        'Accept': 'application/json',
        'Accept-Language': 'en_US',
        'Authorization': f'Basic {auth_base64}',
    }

    body = 'grant_type=client_credentials'
    response = requests.post(url, headers=headers, data=body)

    if not response.ok:
        raise ValueError('Failed to get access token')

    paypal_data = response.json()
    return paypal_data['access_token']

def check_if_new_transaction(order_model, paypal_transaction_id):
    try:
        # Find all documents where Order.paymentResult.id is the same as the id passed paypal_transaction_id
        orders = order_model.find({'paymentResult.id': paypal_transaction_id})

        # If there are no such orders, then it's a new transaction.
        return orders.count() == 0
    except Exception as e:
        print(e)

def verify_paypal_payment(paypal_transaction_id):
    access_token = get_paypal_access_token()
    paypal_response = requests.get(
        f"{PAYPAL_API_URL}/v2/checkout/orders/{paypal_transaction_id}",
        headers={
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {access_token}',
        }
    )

    if not paypal_response.ok:
        raise ValueError('Failed to verify payment')

    paypal_data = paypal_response.json()
    return {
        'verified': paypal_data['status'] == 'COMPLETED',
        'value': paypal_data['purchase_units'][0]['amount']['value'],
    }
