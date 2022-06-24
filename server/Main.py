from OrdersDB import OrdersDB
from gspread import service_account
import re
from datetime import datetime as dt
from configparser import ConfigParser
import time


# Class for DB
orders = OrdersDB(password="test", host="localhost")

# Url to Google Sheet
GOOGLE_SHEET_URL = "https://docs.google.com/spreadsheets/d/1t_WUuGUNC9MpVdG2y-4tgSo7QYY_vIaDWlehcAuz5L4/edit#gid=0"


# Check order actuality
def isOrderActual(delivery_date: str):
    # Parse order delivery date
    delivery_day, delivery_month, delivery_year = map(int, delivery_date.split('.'))
    now_date = dt.now().date()
    
    # Check if order is actual
    if (delivery_year < now_date.year):
        return False
    elif (delivery_year == now_date.year):
        if (delivery_month < now_date.month):
            return False
        elif (delivery_month == now_date.month):
            if (delivery_day < now_date.day):
                return False
    return True


# Copy orders info from google sheets to DB
def updateDBfromGoogleSheets():
    # Authorize and get table from google sheets by url
    google_api = service_account(filename='./credentials.json')
    google_sheet = google_api.open_by_url(GOOGLE_SHEET_URL)
    sheet_list1 = google_sheet.sheet1.get_all_records()

    for line in sheet_list1:
        #* Order info contains:
        #* _id (int): order id
        #* number (int): number of order
        #* amount_in_usd (float): order amount in USD
        #* delivery_date (str): order delivery date
        table_order = tuple(line.values())
        if '' in table_order or not bool(re.search(r"\d{2}.\d{2}.\d{4}", str(table_order[3]))):
            continue
        db_order = orders.getOrderByNumber(number=table_order[1])
        is_order_actual = isOrderActual(table_order[3])
        # Add new order to DB
        if not db_order:
            orders.addOrder(
                _id=table_order[0],
                number=table_order[1],
                amount_in_usd=table_order[2],
                delivery_date=table_order[3],
                is_actual=is_order_actual
            )
        else:
            # Update usd amount in DB
            if db_order[2] != table_order[2]:
                orders.setUSDAmountByNumber(number=table_order[1], usd_amount=table_order[2])
            # Update delivery date in DB
            if db_order[3] != table_order[3]:
                orders.setDeliveryDateByNumber(number=table_order[1], delivery_date=table_order[3])
                
            # Notify in Telegram if delivery date is not actual
            if not is_order_actual:
                orders.setActualByNumber(number=table_order[1], is_actual=False)
                print("NOTIFY ABOUT NOT ACTUAL ORDER DELIVERY DATE")
                now_date = str(dt.now().date()).split('-')
                now_date.reverse()
                print(f"Now date: {'.'.join(now_date)}")
                print(f"Order delivery date: {table_order[3]}")
                print()
                # TODO: notify about not actual order delivery date in Telegram
                
    # Remove order from DB if it was removed in google sheets
    for order in orders.getAllOrders():
        # Convert order info from DB to google sheets format
        order_info = {'№': order[0], 'заказ №': order[1], 'стоимость,$': order[2], 'срок поставки': order[3]}
        # Check order from DB in google sheets orders
        if order_info not in sheet_list1:
            orders.removeByNumber(order[1])


# Config file with some params
config = ConfigParser()
config.read("./googleConf.ini")

# Time in seconds to update DB
update_time = int(config.get('GoogleSheets', 'update_time'))

# Loop for updating DB with google sheets every <update_time> seconds
while True:
    updateDBfromGoogleSheets()
    
    # Wait time to repeat update
    time.sleep(update_time)
