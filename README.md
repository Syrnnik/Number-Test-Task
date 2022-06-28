# Installation

**Make sure you have installed:**
- PostgreSQL

## Install Python 3 and pip
```
$ sudo apt update
$ sudo apt install python3 python3-pip
```


## Install Python 3 requirements
To install requirements, go to the **applications** folder, then the `server` folder and run the installation of packages from the file `requirements.txt`:
```
$ git clone https://github.com/Syrnnik/Number-Test-Task.git
$ cd Number-Test-Task/server/
$ pip3 install -r requirements.txt
...
```

## Configure PostgreSQL connection
To configure the PostgreSQL connection, go to the **applications** folder, then to the `server` folder and edit the `googleConf.ini` file:
```
$ nano googleConf.ini
...
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


## Run app
To run, go to the **applications** folder, then to the `server` folder and run `WebServer.py` script:
```
$ python3 WebServer.py
...
```
