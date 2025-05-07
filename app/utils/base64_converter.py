from pathlib import Path
import base64
import mimetypes
import re
from datetime import datetime

##########################################################################################################
# Function to encode to base64 ###########################################################################
##########################################################################################################

def encode_base64(file_path, type_path):
    """
    Function to encode a file to Base64 format.

    Parameters:
        file_path (str): Path to the file to be encoded.
        type_path (str): File extension including dot (e.g., '.pdf', '.dwg').

    Returns:
        str: Base64 encoded string in 'data:<mime>;base64,...' format.

    Example use:
        encoded_file = encode_base64("path/to/file.pdf", ".pdf")
    """
    path = Path(file_path)
    if not path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")

    mime_map = {
        ".pdf": "application/pdf",
        ".dwg": "image/vnd.dwg",
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg"
    }

    mime_type = mime_map.get(type_path.lower()) or mimetypes.guess_type(str(path))[0]
    if not mime_type:
        raise ValueError(f"Unsupported or unknown file type: {type_path}")

    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")

    return encoded

##########################################################################################################
# Function to decode to base64  ##########################################################################
##########################################################################################################

def decode_base64(data_b64, output_path=None, default_name="decoded_file"):
    """
    Function to decode a Base64 string back to a file.

    Parameters:
        data_b64 (str): Base64 encoded string (with or without MIME prefix).
        output_path (str, optional): Path to save the decoded file. If None, auto-generates name.
        default_name (str, optional): Base name used if output_path is not provided.

    Returns:
        Path: Path to the saved file.

    Example use:
        decode_base64(encoded_file, "output/file.pdf")
    """

    match = re.match(r"data:(.+?);base64,(.*)", data_b64, flags=re.I | re.S)

    if match:
        mime_type, base64_content = match.groups()
        extension_map = {
            "application/pdf": ".pdf",
            "image/vnd.dwg": ".dwg",
            "image/png": ".png",
            "image/jpeg": ".jpg"
        }
        file_ext = extension_map.get(mime_type, "")
    else:
        base64_content = data_b64
        file_ext = ""

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"{default_name}_{timestamp}{file_ext}"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(base64.b64decode(base64_content))

    return output_path
