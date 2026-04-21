import argparse
import os
import sys
from dotenv import load_dotenv
from bot.orders import OrderManager

def main():
    # Load environment variables securely
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        print(" Error: API credentials not found. Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.")
        sys.exit(1)

    parser = argparse.ArgumentParser(description="Binance Futures Testnet Trading Bot")
    parser.add_argument("--symbol", required=True, help="Trading pair symbol (e.g., BTCUSDT)")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"], help="Order side (BUY/SELL)")
    parser.add_argument("--type", required=True, choices=["MARKET", "LIMIT", "market", "limit"], help="Order type (MARKET/LIMIT)")
    parser.add_argument("--qty", required=True, help="Order quantity")
    parser.add_argument("--price", help="Order price (Required if type is LIMIT)")

    args = parser.parse_args()

    try:
        manager = OrderManager(api_key, api_secret)
        result = manager.execute_order(args.symbol, args.side, args.type, args.qty, args.price)

        data = result.get("data", {})
        
        if result["status_code"] == 200:
            print(" SUCCESS: Order Placed Successfully!\n")
            print("--- ORDER RESPONSE DETAILS ---")
            print(f"Order ID:     {data.get('orderId')}")
            print(f"Status:       {data.get('status')}")
            print(f"Executed Qty: {data.get('executedQty')}")
            # MARKET orders use avgPrice, LIMIT orders use price
            avg_price = data.get('avgPrice')
            if avg_price and float(avg_price) > 0:
                print(f"Avg Price:    {avg_price}")
           
        else:
            print(" FAILURE: Order Failed.\n")
            print(f"API Error Code: {data.get('code')}")
            print(f"Message:        {data.get('msg')}")
            print("Check trading_bot.log for detailed API request/response traces.")

    except ValueError as ve:
        print(f"\n INPUT ERROR: {str(ve)}")
    except ConnectionError as ce:
        print(f"\n NETWORK ERROR: {str(ce)}")
    except Exception as e:
        print(f"\n UNEXPECTED ERROR: {str(e)}")

if __name__ == "__main__":
    main()