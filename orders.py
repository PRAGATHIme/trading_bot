from bot.client import BinanceTestnetClient
from bot import validators

class OrderManager:
    def __init__(self, api_key: str, api_secret: str):
        self.client = BinanceTestnetClient(api_key, api_secret)

    def execute_order(self, raw_symbol, raw_side, raw_type, raw_qty, raw_price):
        # 1. Validate inputs
        symbol = validators.validate_symbol(raw_symbol)
        side = validators.validate_side(raw_side)
        order_type = validators.validate_order_type(raw_type)
        quantity = validators.validate_quantity(raw_qty)
        price = validators.validate_price(raw_price, order_type)

        # 2. Print Request Summary (CLI UX)
        print("\n--- ORDER REQUEST SUMMARY ---")
        print(f"Symbol:   {symbol}")
        print(f"Side:     {side}")
        print(f"Type:     {order_type}")
        print(f"Quantity: {quantity}")
        if order_type == 'LIMIT':
            print(f"Price:    {price}")
        print("-----------------------------\n")

        # 3. Execute
        print("Placing order...")
        response = self.client.place_order(symbol, side, order_type, quantity, price)
        
        return response