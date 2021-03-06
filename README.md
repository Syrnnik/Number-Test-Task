# Installation
Url to Google Sheet - https://docs.google.com/spreadsheets/d/1t_WUuGUNC9MpVdG2y-4tgSo7QYY_vIaDWlehcAuz5L4

## Install Python 3 and pip
```
$ sudo apt update
$ sudo apt install python3 python3-pip
```

## Install PostgreSQL
```
$ sudo apt update
$ sudo apt install postgresql
```

## Configure PostgreSQL users
```
$ sudo -i -u postgres psql
$ create database <db_name>;
$ create user <user_name> password '<user_password>';
$ GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;
$ \q
```
**Remember `<db_name>`, `<user_name>` and `<user_password>`.**

## Install Python 3 requirements
```
$ git clone https://github.com/Syrnnik/Number-Test-Task.git
$ cd Number-Test-Task/server/
$ pip3 install -r requirements.txt
```

## Configure PostgreSQL connection
```
$ nano googleConf.ini
```
### **Specify all the parameters for connecting to the database**
> <span style="color: #ff3333">**Don't specify empty values!**</span>

> **If you didn't change these values during PostgreSQL installation, set default values.**

| **parameter** |                         **description**                          | **default value** |
| :-----------: | :--------------------------------------------------------------: | :---------------: |
| `db_password` |  The PostgreSQL password associated with the specified username  |                   |
|   `db_host`   | The network host name or the IP address of the PostgreSQL server |    `localhost`    |
| `db_username` |           The database username you wish to connect as           |    `postgres`     |
|   `db_name`   |       The PostgreSQL database name that you want to access       |    `postgres`     |
|   `db_port`   |    The network port that the PostgreSQL server is running on     |      `5432`       |


### **In the same file, specify the time of updating the database**
> <span style="color: #ff3333">**Don't specify empty values!**</span>

|   **param**   |            **description**             | **default value** |
| :-----------: | :------------------------------------: | :---------------: |
| `update_time` | Time in seconds to update the database |       `30`        |

### **Save changes and exit `nano`**

# Run app
```
$ python3 WebServer.py
```

## Telegram Bot (https://t.me/numbers_orders_bot)
You can subscribe to notifications about not actual orders.
Now, if new orders appear in the database and their deadline expires, the bot will notify you about it.

| **command** |                  **description**                   |
| :---------: | :------------------------------------------------: |
|   `/run`    |          Show message with these commands          |
|   `/stop`   | Stop getting notifications about not actual orders |
|   `/help`   | Stop getting notifications about not actual orders |
