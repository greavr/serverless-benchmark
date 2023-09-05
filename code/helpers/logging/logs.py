## This module can enables and configures external log storing to Google Cloud
import logging

def cloud_logging():
    """ Function to build logging"""
    import google.cloud.logging
    from google.cloud.logging.handlers import CloudLoggingHandler, setup_logging

    logging.basicConfig(level=logging.INFO)
    client = google.cloud.logging.Client()
    handler = CloudLoggingHandler(client)
    logging.getLogger().setLevel(logging.DEBUG)
    setup_logging(handler)