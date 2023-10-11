import random
import time
import os

import logging

# Create a random file of set size at location, optional file Name
def CreateFile(Path: str, Size: int, Name: str = "random") -> str:
    """ 
    This function creates a random content file.
    Path: Linux path to folder to create new file in
    Size: Int for file size in GB
    Name: If left blank random file name choosen, else use set
    
    Returns:
    - File Path (As string)
    """

    # Check if randomized name
    if Name == "random":
        Name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=10))

    file_name = f"{Path}/{Name}"

    # Log Attempt
    logging.info(f"Creating file: {file_name} - {Size} GB in size")

    try:
        # Create file
        gig_byte = 1_000_000_000
        
        with open(file_name, 'wb') as file:
            file.write(os.urandom(Size*gig_byte))
        # Done

    except Exception as ex:
        logging.exception(f"Unable to create file: {file_name}")
        logging.exception(str(ex))

    return file_name

# Delete the file
def DeleteFile(Path: str) -> bool:
    """"
    This function removes a file, based on the path provided
    Path: Str - Linux path to file to be removed

    Returns:
    - Bool, if success
    """
    # Log Attempt
    logging.info(f"Deleting file: {Path}")

    # Check file exists
    if os.path.isfile(Path):
        # File exists try to delete
        try:
            os.remove(Path)
            return True

        except Exception as ex:
            logging.exception(f"Unable to delete file: {Path}")
            logging.exception(str(ex))
            return False

    else:
        logging.error(f"File Not Found: {Path}")
        return False
    
