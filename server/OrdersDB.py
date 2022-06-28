import requests
from xml.etree.ElementTree import fromstring
import psycopg2


# Convert USD amount to RUB amount with actual rate
def convert_usd_to_rub(amount_in_usd: float) -> float:
    response = requests.get("https://www.cbr.ru/scripts/XML_daily.asp")
    # Convert str to xml
    all_valutes = fromstring(response.text)
    # Get USD rate in RUBs
    for valute in all_valutes:
        if valute.attrib.get('ID') == "R01235":
            for param in valute:
                if param.tag == "Value":
                    amount_in_rub = amount_in_usd * float(param.text.replace(',', '.'))
    return amount_in_rub


class OrdersDB:
    # Initializing table and connection info
    def __init__(self, password: str, username: str="postgres", host: str="localhost",
                dbname: str="postgres", port: int="5432") -> None:
        # Save connection info
        self.dbname = dbname
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        
        # DB cols names
        self.col_id = "_id"
        self.col_number = "number"
        self.col_amount_in_usd = "amount_in_usd"
        self.col_delivery_date = "delivery_date"
        self.col_amount_in_rub = "amount_in_rub"
        self.col_is_actual = "is_actual"
        
        # Create table with orders if not exist
        self.table_name = "orders"
        self.cur = self.connect()
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            {self.col_id} INTEGER NOT NULL,
            {self.col_number} INTEGER NOT NULL PRIMARY KEY,
            {self.col_amount_in_usd} REAL NOT NULL,
            {self.col_delivery_date} TEXT NOT NULL,
            {self.col_amount_in_rub} REAL NOT NULL,
            {self.col_is_actual} BOOLEAN NOT NULL
        );""")
        self.save()
        self.close()
        
    # Open connection
    def connect(self) -> None:
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.username,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.cur = self.conn.cursor()
        return self.cur
    
    # Close connection
    def close(self) -> None:
        if self.conn and self.cur:
            self.cur.close()
            self.conn.close()

    # Save changes
    def save(self) -> None:
        self.conn.commit()


    # Add new order
    def addOrder(self, _id: int, number: int, amount_in_usd: float, delivery_date: str, is_actual: bool=True) -> None:
        # Convert amount from USD to RUB
        amout_in_rub = convert_usd_to_rub(amount_in_usd)
        
        self.cur = self.connect()
        self.cur.execute(f"""INSERT INTO {self.table_name} (
                        {self.col_id},
                        {self.col_number},
                        {self.col_amount_in_usd},
                        {self.col_delivery_date},
                        {self.col_amount_in_rub},
                        {self.col_is_actual}
                    ) VALUES (
                        {_id},
                        {number},
                        {amount_in_usd},
                        '{delivery_date}',
                        {amout_in_rub},
                        {is_actual}
                    );""")
        self.save()
        self.close()


    # Get all orders
    def getAllOrders(self) -> list:
        self.cur = self.connect()
        self.cur.execute(f"SELECT * FROM {self.table_name};")
        orders = self.cur.fetchall()
        self.close()
        return orders

    # Get order by number
    def getOrderByNumber(self, number: int) -> tuple:
        self.cur = self.connect()
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE number={number};")
        order = self.cur.fetchone()
        self.close()
        return order
    
    # 
    def getRUBAmountByNumber(self, number: int) -> float:
        self.cur = self.connect()
        self.cur.execute(f"SELECT {self.col_amount_in_rub} FROM {self.table_name} WHERE number={number};")
        rub_amount = self.cur.fetchone()[0]
        self.close()
        return rub_amount

    # Check order actualite by number
    def isActualByNumber(self, number: int) -> bool:
        self.cur = self.connect()
        self.cur.execute(f"SELECT {self.col_is_actual} FROM {self.table_name} WHERE number={number};")
        is_actual = self.cur.fetchone()[0]
        self.close()
        return is_actual


    # Change order id by number
    def setIdByNumber(self, number: int, _id: int) -> None:
        self.cur = self.connect()
        self.cur.execute(f"UPDATE {self.table_name} SET {self.col_id}={_id} WHERE {self.col_number}={number};")
        self.save()
        self.close()
    
    # Change order usd amount by number
    def setUSDAmountByNumber(self, number: int, usd_amount: float) -> None:
        self.cur = self.connect()
        self.cur.execute(f"UPDATE {self.table_name} SET {self.col_amount_in_usd}={usd_amount} WHERE {self.col_number}={number};")
        self.save()
        self.close()
        # Change rub amount with actual rate
        rub_amount = convert_usd_to_rub(usd_amount)
        self.setRUBAmountByNumber(number, rub_amount)
    
    # Change order delivery date by number
    def setDeliveryDateByNumber(self, number: int, delivery_date: str) -> None:
        self.cur = self.connect()
        self.cur.execute(f"UPDATE {self.table_name} SET {self.col_delivery_date}='{delivery_date}' WHERE {self.col_number}={number};")
        self.save()
        self.close()
    
    # Change order actuality by number
    def setActualByNumber(self, number: int, is_actual: bool) -> None:
        self.cur = self.connect()
        self.cur.execute(f"UPDATE {self.table_name} SET {self.col_is_actual}={is_actual} WHERE {self.col_number}={number};")
        self.save()
        self.close()
    
    # Change order rub amount by number
    def setRUBAmountByNumber(self, number: int, rub_amount: float) -> None:
        self.cur = self.connect()
        self.cur.execute(f"UPDATE {self.table_name} SET {self.col_amount_in_rub}={rub_amount} WHERE {self.col_number}={number};")
        self.save()
        self.close()


    # Remove order by number
    def removeByNumber(self, number: int) -> None:
        self.cur = self.connect()
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE {self.col_number}={number};")
        self.save()
        self.close()
