import logging
import random
import time
 
import mysql.connector

# Create DB Connection
def CreateConnection(Host: str, User: str, Password: str, Port: str = "3306", Database_name: str = "") -> mysql.connector:
    """
    This function creates a connection to the host with provided creds
    Host: Str - (IP Address) to connect to DB
    User: Str - DB Username
    Password: Str - DB Password
    """

     # Log Attempt
    logging.debug(f"Connecting to DB via IP: {Host}, with the Username {User}")

    mydb = ""

    try:
        mydb = mysql.connector.connect(
            host=Host,
            user=User,
            password=Password,
            port=Port,
            database=Database_name
        )

        return mydb
    except Exception as ex:
        logging.exception(f"Unable to connect to the DB: {Host}")
        logging.exception(str(ex))
        return mydb
    
# Create Datbase
def CreateDB(Connection: mysql.connector, DB_NAME: str = "random") -> str:
    """
    This function creates a new database and returns the Database Name
    Connection: mysql.connector - Connection to target DB
    DB_NAME: str - DB Name
    """

    # Check if random name and if so generate
    if DB_NAME == "random":
        DB_NAME = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

    logging.debug(f"Creating database: {DB_NAME}")
    try:
        mycursor = Connection.cursor()
        mycursor.execute(f"CREATE DATABASE {DB_NAME}")
        Connection.commit()
        return DB_NAME
    except Exception as ex:
        logging.exception(f"Unable to Create the DB: {DB_NAME}")
        logging.exception(str(ex))
        return ""

# Create Testing Table
def CreateTable(Connection: mysql.connector, Rows: int, TABLE_NAME: str = "random") -> str:
    """
    This function creates a random table name, with these set columns:
    ID = Primary Key Int (auto increment)
    NAME = VARCHAR(255)
    ADDRESS = VARCHAR(255)
    ACTIVE= BOOL
    
    Returns
    - TABLE_NAME: Str - Newly created table name
    """

    # Check if random name and if so generate
    if TABLE_NAME == "random":
        TABLE_NAME = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))

    logging.debug(f"Creating table: {TABLE_NAME}, with {Rows} rows inside")

    try:
        mycursor = Connection.cursor()
        # Create the table
        mycursor.execute(f"CREATE TABLE {TABLE_NAME} (ID INT(11) NOT NULL AUTO_INCREMENT, name VARCHAR(255), address VARCHAR(255), active BOOLEAN, PRIMARY KEY (`ID`))")
        Connection.commit()
        # Now create rows
        i = 0
        while i<= Rows:
            i += 1
            fname = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=5))
            address = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=15))
            active = random.choice([True, False])
            sql = f"INSERT INTO {TABLE_NAME} (name, address, active) VALUES (%s, %s, %s)"
            val = (fname,address, active)
            mycursor.execute(sql, val)

        Connection.commit()
        logging.debug(f"{mycursor.rowcount}, record inserted.")
        return TABLE_NAME

    except Exception as ex:
        logging.exception(f"Unable to Create the table: {TABLE_NAME}")
        logging.exception(str(ex))
        return ""   

# Read Tables
def ReadTable(Connection: mysql.connector, TABLE_NAME: str) -> list:
    """
    This function reads each row in the table and appends value to list
    """
    logging.debug(f"Reading table: {TABLE_NAME}")
    results = []
    try:
        mycursor = Connection.cursor()
        # Read the table
        mycursor.execute(f"SELECT * FROM {TABLE_NAME}")
        myresult = mycursor.fetchall()

        for x in myresult:
            results.append(x)

        return results

    except Exception as ex:
        logging.exception(f"Unable to Read the table: {TABLE_NAME}")
        logging.exception(str(ex))
        return results 

# Drop Table
def DropDatabase(Connection: mysql.connector, DATABASE_NAME: str) -> bool:
    """
    This function drops the table created
    """
    logging.debug(f"Dropping table: {DATABASE_NAME}")

    try:
        mycursor = Connection.cursor()
        # Drop the table
        sql = f"DROP DATABASE IF EXISTS {DATABASE_NAME}"
        mycursor.execute(sql)

        Connection.commit()
        return True
    except Exception as ex:
        logging.exception(f"Unable to Drop the table: {DATABASE_NAME}")
        logging.exception(str(ex))
        return False 

# SQL Test Handler
def SQLTestHandler(Host: str, User: str, Password: str, Rows_To_Create: int, Port: int = 3306) -> list:
    """ 
        This function handles the tests for the SQL component
        Will return a list of test names, time, and testing methods.
        The tests run are:
         - Time To Create X Number of Rows 
         - Time To Read X Number of Rows 
        Take Paremeter:
        - Host: Str - IP Address of the MySQL Target
        - User: Str - Username for MySQL
        - Password: Str - Password for MySQL
        - Rows_To_Create: Int - Number of rows to create / read
        - Port: Int - Default to 3306 but support in case that needs changing
        Returns:
        - list: list of lists, each one contains a test name, time taken, and parameters used
    """
    logging.info("Running MySQL Tests")
    result_set = []

    thisConnection = CreateConnection(Host=Host, User=User, Password=Password)
    # Validate DB Exists
    if thisConnection == "" :
        return ""
    DatabaseName = CreateDB(Connection=thisConnection)
    thisConnection = CreateConnection(Host=Host, User=User, Password=Password, Database_name=DatabaseName)

    # Do the first test
    # Start the timer and do the test
    st = time.time()
    CreatedTable = CreateTable(Connection=thisConnection,Rows=Rows_To_Create)
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Do the Second Test
    # Start the timer and do the test
    st = time.time()
    ReadRows = ReadTable(Connection=thisConnection,TABLE_NAME=CreatedTable)
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Final Cleanup
    DropDatabase(Connection=thisConnection,DATABASE_NAME=DatabaseName)

    # Return Results
    return result_set