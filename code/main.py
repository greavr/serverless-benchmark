from flask import Flask, render_template
import logging
from helpers.logging import logs, apm   
from helpers.storage import storage
from helpers.sql import mysql
from helpers.redis import redis

import os
import json

app = Flask(__name__)
app.config.from_pyfile('./cloudrun.cfg')

@app.route("/")
def index():
    return render_template("index.html", storageLocations=app.config['STORAGE_LOCATIONS'],fileTest=[app.config['LARGE_FILE_SIZE'],app.config['SMALL_FILE_COUNT'],app.config['SMALL_FILE_SIZE']], mysqlLocations=app.config['MYSQL_LOCATIONS'],mysqlTest=[app.config['MYSQL_ROWS']],redisLocations=app.config['REDIS_LOCATIONS'], redisTest=[app.config['REDIS_ENTRIES'],app.config['REDIS_RANDOM']]  )

@app.route("/storage")
def storage_tests():
    storage_results = {}
    for aFolder in app.config['STORAGE_LOCATIONS']:
        storage_results[aFolder] = storage.StorageTestHandler(Folder_Path=aFolder, SmallFileCount=app.config['SMALL_FILE_COUNT'], FileSize=app.config['LARGE_FILE_SIZE'], SmallFileSize=app.config['SMALL_FILE_SIZE'])
    
    return json.dumps(storage_results)

@app.route("/sql")
def sql_tests():
    sql_results = {}
    for aServer in app.config['MYSQL_LOCATIONS']:
        sql_results[aServer] = mysql.SQLTestHandler(Host=aServer, User=app.config['MYSQL_USER'], Password=app.config['MYSQL_PWD'], Rows_To_Create=app.config['MYSQL_ROWS'])

    return json.dumps(sql_results)

@app.route("/redis")
def redis_tests():
    redis_results = {}
    for aServer in app.config['REDIS_LOCATIONS']:
        redis_results[aServer] = redis.RedisTestHandler(Host=aServer, Create_Entries=app.config['REDIS_ENTRIES'], Random_Searches=app.config['REDIS_RANDOM'])

    return json.dumps(redis_results)


if __name__ == "__main__":
    """ Main Entry point """

    ## Itterate over all environmental variables:
    for key, value in os.environ.items():
        logging.info(key, value)

    try:
        # Check if should enable Logging
        enable_logging = bool(os.environ.get("ENABLE_LOGGING", True))
        # Enable logging
        if enable_logging:
            logs.cloud_logging()

        # Check to see if OpenTelemetary should be opened
        enable_apm = bool(os.environ.get("ENABLE_APM", True))

        #Enable APM
        if enable_apm:
                apm.cloud_profiler()
        
        
    except Exception as ex:
        logging.exception(f"Unable to cast bool: {os.getenv('ENABLE_LOGGING')}")
        logging.exception(str(ex))
    
    # Finally run app
    app.run()
