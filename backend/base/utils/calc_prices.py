def add_decimals(num):
    return format(round(num, 2), '.2f')

def calc_prices(order_items):
    # Calculate the items price
    items_price = add_decimals(
        sum(0.83 * item['price'] * item['qty'] for item in order_items)
    )
    # Calculate the shipping price
    shipping_price = add_decimals(0 if float(items_price) > 100 else 10)
    # Calculate the tax price
    tax_price = add_decimals(float(0.17 * (float(items_price) / 0.83)))
    # Calculate the total price
    total_price = add_decimals(
        float(items_price) + float(shipping_price) + float(tax_price)
    )
    return {
        'itemsPrice': items_price,
        'shippingPrice': shipping_price,
        'taxPrice': tax_price,
        'taxPrice': tax_price,
        'totalPrice': total_price,
    }
