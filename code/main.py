from flask import Flask, render_template
import logging
from helpers.logging import logs, apm   
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html", storageLocations=["a","b","c"],fileTest=[10,100,1], mysqlLocations=["a","b","c"],mysqlTest=1000,redisLocations=["a","b","c"], redisTest=[1000,700]  )

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
