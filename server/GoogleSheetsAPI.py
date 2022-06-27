from threading import Thread
from gspread import service_account
from datetime import datetime as dt
import re
import time
from Bot import bot


class GoogleSheetsAPI:
    
    def __init__(self, orders: object, google_sheet_url: str, users: object):
        # Orders DB methods
        self.orders = orders
        # Users DB methods
        self.users = users
        # Url to Google Sheet
        self.GOOGLE_SHEET_URL = google_sheet_url


    # Check order actuality
    def isOrderActual(self, delivery_date: str):
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
    def updateDBfromGoogleSheets(self):
        # Authorize and get table from google sheets by url
        google_api = service_account(filename='./credentials.json')
        google_sheet = google_api.open_by_url(self.GOOGLE_SHEET_URL)
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
            db_order = self.orders.getOrderByNumber(number=table_order[1])
            # Add new order to DB
            if not db_order:
                self.orders.addOrder(
                    _id=table_order[0],
                    number=table_order[1],
                    amount_in_usd=table_order[2],
                    delivery_date=table_order[3]
                )
            else:
                # Update id in DB
                if db_order[0] != table_order[0]:
                    self.orders.setIdByNumber(number=table_order[1], _id=table_order[0])
                # Update usd amount in DB
                if db_order[2] != table_order[2]:
                    self.orders.setUSDAmountByNumber(number=table_order[1], usd_amount=table_order[2])
                # Update delivery date in DB
                if db_order[3] != table_order[3]:
                    self.orders.setDeliveryDateByNumber(number=table_order[1], delivery_date=table_order[3])
                    
                # Notify in Telegram if delivery date is not actual
                for user in self.users.getAllUsers():
                    # print(user)
                    if not self.isOrderActual(table_order[3]) and self.orders.isActualByNumber(number=table_order[1]):
                        self.orders.setActualByNumber(number=table_order[1], is_actual=False)
                        ### Text is shifted to the left so that
                        ### Telegram doesnt read extra spaces at the beginning of lines
                        bot.send_message(
                            user[1],
                            f"""
Delivery date of order with number {table_order[1]} has passed
About order:
Id: {table_order[0]}
Number: {table_order[1]}
USD amount: {table_order[2]}
Delivery date: {table_order[3]}
RUB amount: {self.orders.getRUBAmountByNumber(table_order[1])}
""")
                    
        # Remove order from DB if it was removed in google sheets
        for order in self.orders.getAllOrders():
            # Convert order info from DB to google sheets format
            order_info = {'№': order[0], 'заказ №': order[1], 'стоимость,$': order[2], 'срок поставки': order[3]}
            # Check order from DB in google sheets
            if order_info not in sheet_list1:
                self.orders.removeByNumber(order[1])


    # Loop for updating DB with google sheets every <update_time> seconds
    def run(self, update_time: int):
        # Run telegram bot for notifications
        thr = Thread(target=bot.infinity_polling, daemon=True)
        thr.start()
        
        while True:
            self.updateDBfromGoogleSheets()
            
            # Wait time to repeat update
            time.sleep(update_time)

