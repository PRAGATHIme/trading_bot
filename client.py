import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import setup_logger

logger = setup_logger()

class BinanceTestnetClient:
    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API Key and Secret must be provided.")
        
        self.base_url = "https://testnet.binancefuture.com"
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _generate_signature(self, query_string: str) -> str:
        return hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None) -> dict:
        endpoint = "/fapi/v1/order"
        
        params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
            "timestamp": int(time.time() * 1000)
        }

        if order_type == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC" # Good Till Cancelled is required for LIMIT

        query_string = urlencode(params)
        signature = self._generate_signature(query_string)
        url = f"{self.base_url}{endpoint}?{query_string}&signature={signature}"

        logger.info(f"Sending Order Request -> Endpoint: {endpoint} | Params: {params}")

        try:
            response = self.session.post(url)
            response_data = response.json()
            
            if response.status_code != 200:
                logger.error(f"API Error {response.status_code}: {response_data}")
            else:
                logger.info(f"Order Successful: {response_data}")
                
            return {"status_code": response.status_code, "data": response_data}
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network Failure: {str(e)}")
            raise ConnectionError(f"Failed to connect to Binance Testnet: {str(e)}")