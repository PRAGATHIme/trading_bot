def validate_symbol(symbol: str) -> str:
    if not symbol or len(symbol) < 3:
        raise ValueError("Invalid symbol format. Example: BTCUSDT")
    return symbol.upper()

def validate_side(side: str) -> str:
    side = side.upper()
    if side not in ['BUY', 'SELL']:
        raise ValueError("Side must be either 'BUY' or 'SELL'")
    return side

def validate_order_type(order_type: str) -> str:
    order_type = order_type.upper()
    if order_type not in ['MARKET', 'LIMIT']:
        raise ValueError("Order type must be either 'MARKET' or 'LIMIT'")
    return order_type

def validate_quantity(quantity: str) -> float:
    try:
        qty = float(quantity)
        if qty <= 0:
            raise ValueError
        return qty
    except ValueError:
        raise ValueError("Quantity must be a positive number.")

def validate_price(price: str, order_type: str) -> float:
    if order_type == 'LIMIT':
        if not price:
            raise ValueError("Price is required for LIMIT orders.")
        try:
            p = float(price)
            if p <= 0:
                raise ValueError
            return p
        except ValueError:
            raise ValueError("Price must be a positive number.")
    return 0.0