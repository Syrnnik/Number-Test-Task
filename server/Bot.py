from configparser import ConfigParser
from BotUsersDB import BotUsersDB
from telebot import TeleBot


# Config file with google sheets and DB params
config = ConfigParser()
config.read("./googleConf.ini")

# Params to connect to DB
db_host = config.get('GoogleSheets', 'db_host')
db_password = config.get('GoogleSheets', 'db_password')
db_username = config.get('GoogleSheets', 'db_username')
db_name = config.get('GoogleSheets', 'db_name')
db_port = int(config.get('GoogleSheets', 'db_port'))

# Class for users DB
users = BotUsersDB(
    password=db_password,
    username=db_username,
    host=db_host,
    dbname=db_name,
    port=db_port
)

# Config file with bot params
config.read("./botConf.ini")

# Telegram bot token
token = config.get('OrdersBot', 'token')

bot = TeleBot(token)


# if msg text is /start or /help
@bot.message_handler(commands=['start', 'help'])
def start(msg):
    user_id = msg.from_user.id
    bot.send_message(
        user_id,
        """
/help - show this message
/run - start getting notifications about not actual orders
/stop - stop getting notifications about not actual orders
""")


# if msg text is /run
@bot.message_handler(commands=['run'])
def run(msg):
    user_id = msg.from_user.id
    
    # Check if user already getting notifications
    if users.getUserByUserId(user_id):
        bot.send_message(user_id, "You already getting notifications.")
        return

    # Add user for sending notifications
    users.addUser(user_id)
    bot.send_message(user_id, "I will notify you if some new order becomes not actual.")


# if msg text is /stop
@bot.message_handler(commands=['stop'])
def stop(msg):
    user_id = msg.from_user.id
    
    # Check if user already getting notifications
    if not users.getUserByUserId(user_id):
        bot.send_message(user_id, "You're not get notifications yet.")
        return
    
    # Remove user for sending notofications
    users.removeUserByUserId(user_id)
    bot.send_message(user_id, "Okey, if you need information, write me.")

