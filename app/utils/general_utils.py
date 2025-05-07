import logging
import requests
from typing import Any
import json
import os


RETRY_STATUS = {429, 500, 502, 503, 504}
CHECKPOINT = "checkpoint.json"


session = requests.Session()
session.headers.update({
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json"
})


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
    if not os.path.exists(log_dir_path):
        os.makedirs(log_dir_path)

    log_file = os.path.join(log_dir_path, "logs.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )

    return logging

def save_checkpoint(data: Any) -> None:
    """
    Function to save the current state of the data to a checkpoint file.
    
    Parameters:
        data (Any) - The data to be saved to the checkpoint file.

    Returns:
        None

    Example use:
        save_checkpoint(data)
    """
    with open(CHECKPOINT, "w") as fp:
        json.dump(data, fp)


def load_checkpoint() -> Any | None:
    """
    Function to load the data from a checkpoint file.
    
    Parameters:
        None

    Returns:
        None

    Example use:
        data = load_checkpoint()
    """
    if os.path.exists(CHECKPOINT):
        with open(CHECKPOINT) as fp:
            return json.load(fp)
    return None


def safe_get(url: str, **kwargs):
    """
    Function to safely make a GET request to a URL, retrying on certain status codes.

    Parameters:
        url (str) - The URL to make the GET request to.
        **kwargs - Additional arguments to pass to the requests.get() function.

    Example use:
        response = safe_get("https://example.com/api/data")    
    """
    try:
        resp = session.get(url, **kwargs)
        if resp.status_code in RETRY_STATUS:
            raise RuntimeError(f"HTTP {resp.status_code}")
        resp.raise_for_status()
        return resp
    except Exception as exc:
        logging.error(f"Interrompido em {url} _ {exc}")
        raise
