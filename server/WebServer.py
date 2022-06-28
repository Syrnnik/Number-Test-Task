from configparser import ConfigParser
from OrdersDB import OrdersDB
from flask import Flask
from flask_cors import CORS, cross_origin
from GoogleSheetsAPI import GoogleSheetsAPI
from threading import Thread
from BotUsersDB import BotUsersDB


# Config file with google sheets and DB params
config = ConfigParser()
config.read("./googleConf.ini")

# Params to connect to DB
db_host = config.get('GoogleSheets', 'db_host')
db_password = config.get('GoogleSheets', 'db_password')
db_username = config.get('GoogleSheets', 'db_username')
db_name = config.get('GoogleSheets', 'db_name')
db_port = int(config.get('GoogleSheets', 'db_port'))

# Url to your Google Sheet
google_sheet_url = config.get('GoogleSheets', 'google_sheet_url')

# Time in seconds to update DB
update_time = int(config.get('GoogleSheets', 'update_time'))

# Class for orders DB
orders = OrdersDB(
    password=db_password,
    username=db_username,
    host=db_host,
    dbname=db_name,
    port=db_port
)

# Class for users DB
users = BotUsersDB(
    password=db_password,
    username=db_username,
    host=db_host,
    dbname=db_name,
    port=db_port
)

web_server = Flask(__name__)
cors = CORS(web_server)
web_server.config['CORS_HEADERS'] = 'Content-Type'
googleAPI = GoogleSheetsAPI(orders, google_sheet_url, users)

# Run script fro google sheets
thr = Thread(target=googleAPI.run, args=(update_time,), daemon=True)
thr.start()


# Route to get data from DB
@web_server.route('/table/', methods=['GET'])
@cross_origin()
def table():
    cols = ["№", "заказ №", "стоимость, $", "срок поставки", "стоимость, руб", "актуальность"]
    ords = orders.getAllOrders()
    for i in range(len(ords)):
        ordr = dict()
        print(ords[i])
        for j in range(len(ords[i])):
            ordr.update({cols[j]: f"{ords[i][j]}"})
        ords[i] = ordr
    ords = str(ords).replace("'", '"')
    return ords, {'Content-Type': 'application/json'}


web_server.run()