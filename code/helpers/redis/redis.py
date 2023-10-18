import logging
import random
import time
 
import redis

# Create Connector
def RedisConnector(Host: str, Port: int = 6379) -> redis.Redis:
    """ This function connects to redis and returns a client"""

    # Log Attempt
    logging.debug(f"Connecting to Redis via IP: {Host}, on the Port {Port}")

    redis_client = ""

    try:
         redis_client = redis.Redis(host=Host, port=Port)
         return redis_client

    except Exception as ex:
        logging.exception(f"Unable to connect to the Redis Host: {Host}")
        logging.exception(str(ex))
        return redis_client
    
# Create Redis values
def RedisPopulate(Connection: redis.Redis, Rows: int) -> int:
    """
    This function creates Rows number of redis entries
    """

    logging.debug(f"Adding {Rows} entries to Redis instance")
    count = 0
    try:
        while count <= Rows:
            some_value = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=250))
            Connection.mset({count:some_value})
            count += 1
    
        return count

    except Exception as ex:
        logging.exception(f"Unable to Add Rows to the Redis Instance: {Connection}")
        logging.exception(str(ex))
        return ""       

# Read Redis values
def RedisRead(Connection: redis.Redis, Max_Rows: int, Rows_To_Read: int) -> list:
    """
    This function reads a random number of rows, between 0 and Max_rows
    Returns a list of all values found
    """
    # Log Attempt
    logging.debug(f"Attempting to read {Rows_To_Read} from Redis")
    return_values = []
    count = 0
    try:
        while count <= Rows_To_Read:
            random_value = random.randint(1, Max_Rows)
            return_values.append(Connection.get(random_value))
            count += 1
        
        return return_values

    except Exception as ex:
        logging.exception(f"Unable to Add Rows to the Redis Instance: {Connection}")
        logging.exception(str(ex))
        return ""       

# Drop Redis values
def RedisDelete(Connection: redis.Redis) -> bool:
    """
    This function simply cleans up the instance
    """

    logging.debug(f"Dropping records in redis: {Connection}")

    try:
        # Drop the table
        Connection.flushdb()

        return True
    except Exception as ex:
        logging.exception(f"Unable to Drop the keys in redis: {Connection}")
        logging.exception(str(ex))
        return False 

# Redis Test Handler
def RedisTestHandler(Host: str, Create_Entries: int, Random_Searches: int, Port: int = 6379) -> list:
    """ 
        This function handles the tests for the Redis component
        Will return a list of test names, time, and testing methods.
        The tests run are:
         - Time To Create X Number of Keys
         - Time To Read X Number of Keys 
        Take Paremeter:
        - Host: Str - IP Address of the Redis Target
        - Create_Entries: Int - Number of redis entries to create
        - Random_Searches: Int - Number of random redis searches to do
        - Port: Int - Default to 6379 but support in case that needs changing
        Returns:
        - list: list of lists, each one contains a test name, time taken, and parameters used
    """
    logging.info("Running Redis Tests")
    result_set = []
    thisConnection = RedisConnector(Host=Host, Port=Port)
    # Validate Redis connector works
    if thisConnection == "":
        return ""
    
    # Do the first test
    # Start the timer and do the test
    st = time.time()
    CreateKeys = RedisPopulate(Connection=thisConnection,Rows=Create_Entries)
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Do the Second Test
    # Start the timer and do the test
    st = time.time()
    ReadRows = RedisRead(Connection=thisConnection,Max_Rows=CreateKeys,Rows_To_Read=Random_Searches)
    et = time.time()
    # Log Time taken
    result_set.append(et - st)


    # Do the Third Test
    # Start the timer and do the test
    st = time.time()
    RedisDelete(Connection=thisConnection)
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Return Results
    return result_set
