import time
import requests

# Function to fetch order book data
def fetch_order_book(stock_symbol):
    api_url = f"https://api.broker.com/orderbook/{stock_symbol}"
    response = requests.get(api_url)
    return response.json()

# Function to place order
def place_order(stock_symbol, price, quantity):
    order_payload = {
        "symbol": stock_symbol,
        "price": price,
        "quantity": quantity,
        "order_type": "limit"  # or "market" if you want a market order
    }
    api_url = "https://api.broker.com/place_order"
    response = requests.post(api_url, json=order_payload)
    return response.status_code

# Main function to monitor and place order
def monitor_and_place_order(stock_symbol, target_buy_price, target_sell_price, quantity):
    while True:
        order_book = fetch_order_book(stock_symbol)
        
        # Check if a buyer bought at the target price
        last_trade_price = order_book['last_trade_price']
        
        if last_trade_price == target_buy_price:
            print(f"Buyer purchased at {target_buy_price}, placing sell order at {target_sell_price}")
            
            # Place the sell order at the next price
            status_code = place_order(stock_symbol, target_sell_price, quantity)
            
            if status_code == 200:
                print(f"Order placed successfully at {target_sell_price}")
            else:
                print(f"Failed to place order. Status code: {status_code}")
            
            break  # Exit after placing the order
        else:
            print(f"No trade at {target_buy_price} yet. Last trade was at {last_trade_price}")
        
        time.sleep(1)  # Wait for a second before checking again

# Example usage
stock_symbol = "ABC"
target_buy_price = 102
target_sell_price = 104
quantity = 100

monitor_and_place_order(stock_symbol, target_buy_price, target_sell_price, quantity)
