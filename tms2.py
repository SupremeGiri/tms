import requests
import time

def get_market_depth(stock_symbol):
    api_url = "https://nepalstock.com.np/marketdepth"
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Check for a successful response
        data = response.json()
        
        # Extract the relevant price data for the specified stock
        for stock in data['data']:
            if stock['symbol'] == stock_symbol:
                return stock['last_price'], stock['last_trade_price']  # Adjust based on actual response structure

    except requests.exceptions.RequestException as e:
        print(f"Error fetching market depth: {e}")
        return None, None

def place_order(stock_symbol, price, quantity):
    api_url = "https://tms40.nepsetms.com.np/tms/me/memberclientorderentry"
    order_data = {
        "symbol": stock_symbol,
        "price": price,
        "quantity": quantity,
        "order_type": "LIMIT"  # Assuming you want to place a limit order
    }
    headers = {
        "Authorization": "Bearer YOUR_API_KEY",  # Replace with your actual API key
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(api_url, json=order_data, headers=headers)
        response.raise_for_status()
        print(f"Order placed successfully at {price} for {quantity} shares.")
    except requests.exceptions.RequestException as e:
        print(f"Failed to place order: {e}")

def monitor_and_place_order(stock_symbol, target_buy_price, quantity):
    attempts = 0  # Counter for attempts
    while attempts < 20:  # Run for 20 attempts
        current_price, last_trade_price = get_market_depth(stock_symbol)
        print(f"Current Price: {current_price}, Last Trade Price: {last_trade_price}")

        if last_trade_price == target_buy_price:
            print(f"Target price reached at {target_buy_price}, placing order.")
            place_order(stock_symbol, target_buy_price, quantity)  # Place order at target buy price
            break  # Exit after placing the order
        
        time.sleep(0.05)  # Sleep for 50 milliseconds
        attempts += 1

# Example usage
stock_symbol = "ABC"  # Replace with the actual stock symbol
target_buy_price = 102  # Your buy target
quantity = 100  # Number of shares to buy

monitor_and_place_order(stock_symbol, target_buy_price, quantity)
