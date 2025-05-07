import requests
from pathlib import Path

def download_with_retry(url, retries=3, delay=5):
    """
    Function to download a file from a URL with retries.

    Parameters:
        url (str) - URL of the file to download.
        retries (int) - Number of retry attempts.
        delay (int) - Delay between retries in seconds.

    Returns:
        None if download fails.
        The content of the file if download is successful.

    Example use:
        content = download_with_retry(URL, retries=5, delay=10)
    """

    headers = {"User-Agent": "Mozilla/5.0"}

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            
            if response.status_code == 200:
                return response.content
            
            else:
                logging.info(f"Try {attempt}/{retries} - failed to download {url} (status {response.status_code})")

        except Exception as e:
            logging.info(f"Try {attempt}/{retries} - error downloading {url}: {e}")
        time.sleep(delay)

    return None


def download_product_files(data):
    """
    Downloads product-related files (manual, CAD, image) for each product in the data.

    Parameters:
        data (list) - List of product categories, each with subcategories and products.

    Returns:
        list: Paths to successfully saved files.
    """

    saved_files = []
    base_path = Path("output/assets")
    base_path.mkdir(parents=True, exist_ok=True)

    for category in data:
        for subcategory in category.get("subcategories", []):
            for sub_subcategory in subcategory.get("sub_subcategory", []):
                for product in sub_subcategory.get("product", []):
                    code = product.get("code")
                    if not code:
                        continue

                    product_folder = base_path / code
                    product_folder.mkdir(parents=True, exist_ok=True)

                    files = {
                        "manual.pdf": product.get("pdf"),
                        "cad.dwg": product.get("dwg"),
                        "img.jpg": product.get("img")
                    }

                    for filename, url in files.items():
                        if not url:
                            continue

                        dest_path = product_folder / filename
                        content = download_with_retry(url, retries=5, delay=10)

                        if content:
                            try:
                                with open(dest_path, "wb") as f:
                                    f.write(content)
                                saved_files.append(str(dest_path))
                                logging.info(f"File saved: {dest_path}")

                            except Exception as e:
                                logging.info(f"Error saving file {dest_path}: {e}")

                        else:
                            logging.info(f"Failed to download after retries: {url}")

    return saved_files
