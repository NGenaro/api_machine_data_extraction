import os
import logging

# Function to set up logging
def setup_logging(log_dir_path):
    """
    Sets up logging to save messages to a log file within the specified directory.

    Parameters:
        log_dir_path (str), path to the directory where the log file should be saved.

    Returns:
        logs file, the configured logging module for use in other parts of the application.

    Exemple use:
        setup_logging("history_log")
    """
    # Create the folder if it doesn't exist
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

    # Full path to the log file
    log_file = os.path.join(log_dir_path, "logs.log")

    # Configure the logging module
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return logging
