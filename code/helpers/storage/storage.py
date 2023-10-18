import random
import time
import os
from base64 import b64encode

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

    gb_size = Size / 1_000_000_000

    # Log Attempt
    logging.debug(f"Creating file: {file_name} - {gb_size} GB in size")

    try:
        # Create file      
        with open(file_name, 'wb') as file:
            file.write(os.urandom(Size))
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
    
# Read the contents of the file
def ReadFile(Path: str) -> list:
    """ 
        This function reads a file and returns the contents as a list of strings

        Takes Parameters:
        - Path : Str - Path to file to be read

        Returns:
        - List : List of strings read from the file
    """

    # Log Attempt
    logging.info(f"Attempting To Read file: {Path}")

     # Check file exists
    if os.path.isfile(Path):
        # File exists try to delete
        try:
            data_read = []
            with open(Path, 'rb') as file_data:
                # Split by new line into a list
                for line in file_data:
                    data_read.append(b64encode(line).decode("utf-8").split())

        except Exception as ex:
            logging.exception(f"Unable to Read file: {Path}")
            logging.exception(str(ex))
            return []
    else:
        logging.error(f"File Not Found: {Path}")
        return []

# Storage Test Handler
def StorageTestHandler(Folder_Path: str, SmallFileCount: int, FileSize: int, SmallFileSize: int ) -> list:
    """ 
        This function handles the tests for the storage component
        Will return a list of test names, time, and testing methods.
        The tests run are:
         - Time To Create a single large file, size of X GB Size (sub task delete file)
         - Time To Create Y number of small files, each Z KB in Size (sub task to delete files when complete)
         - Time To Read all the files created above
        Take Paremeter:
        - Folder_Path: Str - Path on which to create and delete files (test #1&2)
        - SmallFileCount: Int - Number of files to create (test #2)
        - FileSize: Int - Large File Creation Size (test #1)
        - SmallFileSize: Int - Small file creation size (test #2)
        Returns:
        - list: list of lists, each one contains a test name, time taken, and parameters used
    """
    logging.info("Running Storage Tests")
    result_set = []

    # Do the first test
    # Start the timer and do the test
    st = time.time()
    large_file_path = CreateFile(Path = Folder_Path, Size = FileSize)
    et = time.time()
    # Log Time taken
    result_set.append(et - st)
    

    # Second Test
    # Start the timer and do the test
    small_files_path = []
    count = 0
    st = time.time()
    # Itterate file creation
    while count < SmallFileCount:
        # Create new file
        small_files_path.append(CreateFile(Path = Folder_Path, Size = SmallFileSize, Name= f"file-{count}"))
        count += 1
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Third Test
    read_file_results = []
    st = time.time()
    # Itterate over files
    for aFile in small_files_path:
        read_file_results.append(ReadFile( Path=aFile ))
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Final test
    count = 0
    st = time.time()
    # Delete large file
    if DeleteFile(Path=large_file_path):
        count += 1
    #Delete Small Files:
    for aFile in small_files_path:
        if DeleteFile(Path=aFile):
            count += 1
    et = time.time()
    # Log Time taken
    result_set.append(et - st)

    # Return Results
    return result_set