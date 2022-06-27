import psycopg2
from uuid import uuid4


class BotUsersDB:
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
        self.col_user_id = "user_id"
        
        # Create table with user ids if not exist
        self.table_name = "users"
        self.cur = self.connect()
        self.cur.execute(f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
            {self.col_id} TEXT NOT NULL PRIMARY KEY,
            {self.col_user_id} INTEGER NOT NULL
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
        
        
     # Add new user for sending
    def addUser(self, user_id: int) -> None:
        self.cur = self.connect()
        self.cur.execute(f"""INSERT INTO {self.table_name} (
                        {self.col_id},
                        {self.col_user_id}
                    ) VALUES (
                        '{uuid4()}',
                        {user_id}
                    );""")
        self.save()
        self.close()
    
    
    # Get all user ids
    def getAllUsers(self) -> list:
        self.cur = self.connect()
        self.cur.execute(f"SELECT * FROM {self.table_name};")
        users = self.cur.fetchall()
        self.close()
        return users
    
    
    # Get user by telegram id
    def getUserByUserId(self, user_id: int) -> tuple:
        self.cur = self.connect()
        self.cur.execute(f"SELECT * FROM {self.table_name} WHERE {self.col_user_id}={user_id};")
        user = self.cur.fetchone()
        self.close()
        return user
    
    
    # Remove user by telegram id
    def removeUserByUserId(self, user_id: int) -> None:
        self.cur = self.connect()
        self.cur.execute(f"DELETE FROM {self.table_name} WHERE {self.col_user_id}={user_id};")
        self.save()
        self.close()
