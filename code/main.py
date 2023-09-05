from flask import Flask, render_template
import logging
import helpers.logging
import os

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    """ Main Entry point """

    ## Itterate over all environmental variables:
    for key, value in os.environ.items():
        logging.info(key, value)

    try:
        # Check if should enable Logging
        enable_logging = bool(os.getenv("ENABLE_LOGGING"))
        # Enable logging
        if enable_logging:
            helpers.logging.enable_logging()

        # Check to see if OpenTelemetary should be opened
        enable_apm = bool(os.getenv("ENABLE_APM"))

        #Enable APM
        if enable_apm:
                helpers.logging.cloud_profiler()
        
        
    except Exception as ex:
        logging.exception(f"Unable to cast bool: {os.getenv('ENABLE_LOGGING')}")
        logging.exception(str(ex))
    
    # Finally run app
    app.run()
