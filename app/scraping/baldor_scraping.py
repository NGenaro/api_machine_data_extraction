import requests
import logging
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

import time
import os

from utils.general_utils import setup_logging, CHECKPOINT, save_checkpoint, load_checkpoint

##########################################################################################################
# Funcrion to scrape category data #######################################################################
##########################################################################################################

def fetch_category_data():
    """
    Fetches main product category data from the Baldor API.

    Parameters:
        None

    Returns:
        A list of dictionaries containing:
            - id: category ID
            - text: category name
            - count: number of products in the category
            - imageId: image ID for the category
    
    Example use:
        categories = fetch_category_data()
    """

    url = "https://www.baldor.com/api/products?include=results&language=en-US&include=filters&include=category&pageSize=10"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    logging.info(f"_ Fetching main categories from Baldor API")
    logging.info(f"  |_ URL: {url}")

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        categories = data.get("category", {}).get("children", [])
        return [
            {
                "id": cat.get("id"),
                "text": cat.get("text"),
                "count": cat.get("count"),
                "imageId": cat.get("imageId")
            }
            for cat in categories
        ]
    except requests.RequestException as e:
        logging.error(f"Error fetching categories: {e}")

        return []

##########################################################################################################
# Funcrion to scrape subcategory data ####################################################################
##########################################################################################################

def fetch_subcategory_data(categories):
    """
    Fetches all main categories and their respective subcategories.

    Parameters:
        categories (list) - List of dictionaries containing category information.

    Returns:
        Updated list with subcategory data included in each category.
            - {here data from category},
            - subcategories:
                - id: subcategory ID
                - text: subcategory name
                - count: number of products in the subcategory
                - imageId: image ID for the subcategory
    
    Example use:
        data = fetch_subcategory_data(categories)
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    all_data = []

    for category in categories:
        category_id = category["id"]
        url = f"https://www.baldor.com/api/products?include=results&language=en-US&include=filters&include=category&pageSize=10&category={category_id}"
        logging.info(f"  |_ Fetching subcategories for category ID: {category_id}")
        logging.info(f"  |  |_ URL: {url}") 

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()

            subcategories = data.get("category", {}).get("children", [])

            category["subcategories"] = [
                {
                    "id": sub.get("id"),
                    "text": sub.get("text"),
                    "count": sub.get("count"),
                    "imageId": sub.get("imageId")
                }
                for sub in subcategories
            ]

        except requests.RequestException as e:
            logging.error(f"\nError fetching subcategories for category {category_id}: {e} \n")
            category["subcategories"] = []

        all_data.append(category)

    return all_data

##########################################################################################################
# Funcrion to scrape sub-subcategory data ################################################################
##########################################################################################################

def fetch_subsubcategory_data(categories_with_subcategories):
    """
    Fetches sub-subcategory data for each subcategory in the provided list.

    Parameters:
        subcategories (list) - List of dictionaries containing subcategory information.

    Returns:
        Updated list with sub-subcategory data included in each subcategory.
            - {here data from category},
                - {here data from subcategory},
                - sub_subcategory:
                    - id: sub-subcategory ID
                    - text: sub-subcategory name
                    - count: number of products in the sub-subcategory
                    - imageId: image ID for the sub-subcategory
    
    Example use:
        data = fetch_subsubcategory_data(subcategories)
    """
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    for category in categories_with_subcategories:
        subcategories = category.get("subcategories", [])
        for subcat in subcategories:
            subcat_id = subcat.get("id")
            url = f"https://www.baldor.com/api/products?include=results&language=en-US&include=filters&include=category&pageSize=10&category={subcat_id}"
            logging.info(f"  |     |_ Fetching sub-subcategories for subcategory ID: {subcat_id}")
            logging.info(f"  |     |  |_ URL: {url}")

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json()

                children = data.get("category", {}).get("children", [])
                subcat["sub_subcategory"] = [
                    {
                        "id": child.get("id"),
                        "text": child.get("text"),
                        "count": child.get("count"),
                        "imageId": child.get("imageId")
                    }
                    for child in children
                ]

            except requests.RequestException as e:
                logging.error(f"Error fetching sub-subcategories for subcategory {subcat_id}: {e}")
                subcat["sub_subcategory"] = []

    return categories_with_subcategories

##########################################################################################################
# Funcrion to scrape product data ########################################################################
##########################################################################################################

def fetch_products_data(data):
    """
    Fetches product data for each sub-subcategory in the provided data.

    Parameters:
        data (list) - List of dictionaries containing category and subcategory information.

    Returns:
        Updated list with product data included in each sub-subcategory.
            - {here data from category},
                - {here data from subcategory},
                    - {here data from sub_subcategory},
                    - "product": 
                        - code: product code
                        - description: product description
                        - imageId: product image ID
                        - upc: product UPC
                        - USD: product price in USD
                        - pdf: link to product PDF
                        - img: link to product image
                        - dwg: link to product drawing
                        - bom: list of BOM items, each with part_number, description, and quantity

    Example use:
        data = fetch_products_data(data)
    """

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    session = requests.Session()
    session.headers.update(headers)

    for category in data:
        for subcat in category.get("subcategories", []):
            for subsubcat in subcat.get("sub_subcategory", []):
                sub_id   = subsubcat.get("id")
                page     = 1
                products = []

                while True:
                    url = (
                        "https://www.baldor.com/api/products"
                        f"?include=results&language=en-US&pageIndex={page}"
                        f"&pageSize=100&category={sub_id}"
                    )
                    logging.info(f"  |     |     |_ sub_subcategory {sub_id} page {page}")

                    try:
                        resp = session.get(url, timeout=30)
                        resp.raise_for_status()
                        payload = resp.json()

                        raw = payload.get("results", {})
                        matches = raw.get("matches", raw if isinstance(raw, list) else [])

                        if not matches:
                            break

                        for prod in matches:
                            code = prod.get("code")
                            imageId = prod.get("imageId") if prod.get("imageId") else None
                            product_data = {
                                "code"       : code,
                                "description": prod.get("description"),
                                "imageId"    : imageId,
                                "upc"        : prod.get("upc"),
                                "USD"        : prod.get("listPrice", {}).get("amount"),
                                "pdf"        : f"https://www.baldor.com/api/products/{code}/infopacket",
                                "img"        : f"https://www.baldor.com/api/images/{imageId}",
                            }                        

                            for attr in prod.get("attributes", []):
                                name   = (attr.get("name") or "").lower()
                                values = attr.get("values") or []
                                if values:
                                    product_data[name] = values[0].get("value")

                            try:
                                dwg_list_url = f"https://www.baldor.com/api/products/{code}/drawings"
                                resp         = session.get(
                                    dwg_list_url,
                                    timeout=20,
                                    headers={"Accept": "application/xml"}        
                                )

                                xml_txt = resp.text.strip()
                                chosen_number = None

                                if resp.ok and xml_txt.startswith("<"):
                                    root = ET.fromstring(xml_txt)                

                                    for drawing in root.findall(".//{*}Drawing"):
                                        kind   = drawing.find("./{*}Kind")
                                        number = drawing.find("./{*}Number")
                                        if number is None:                      
                                            continue

                                        if kind is not None and kind.text == "DimensionSheet":
                                            chosen_number = number.text
                                            break

                                        if chosen_number is None:
                                            chosen_number = number.text

                                product_data["dwg"] = (
                                    f"https://www.baldor.com/api/products/{code}/drawings/{chosen_number}"
                                    if chosen_number else None
                                )

                            except Exception as e:
                                logging.warning(f"  |  |  |_ dwg {code}: {e}")
                                product_data["dwg"] = None

                            try:
                                parts_url = f"https://www.baldor.com/catalog/{code}?tab=%22parts%22"
                                html      = session.get(parts_url, timeout=20).text
                                soup      = BeautifulSoup(html, "html.parser")

                                bom = []
                                rows = soup.select("table tbody tr")
                                for r in rows:
                                    cols = r.find_all("td")
                                    if len(cols) >= 3:
                                        part_number = cols[0].get_text(strip=True)
                                        if not part_number:                    
                                            continue

                                        bom.append(
                                            {
                                                "part_number": part_number,
                                                "description": cols[1].get_text(strip=True),
                                                "quantity"   : cols[2].get_text(strip=True),
                                            }
                                        )

                                product_data["bom"] = bom                     
                            except Exception as e:
                                logging.warning(f"  |  |  |_ bom {code}: {e}")
                                product_data["bom"] = []

                            products.append(product_data)

                            logging.info(f"  |     |     |  |_ code {code}")
                            logging.info(f"  |     |     |  |_ manual {f'https://www.baldor.com/api/products/{code}/infopacket'}")
                            logging.info(f"  |     |     |  |_ drawing {f'https://www.baldor.com/api/products/{code}/drawings/{chosen_number}'}")
                            logging.info(f"  |     |     |  |_ image {f'https://www.baldor.com/api/images/{imageId}'}")
                            logging.info(f"  |     |     |  |_ bom {product_data['bom']}")

                            ########################################################################

                            if len(products) >= 15:
                                logging.info("Limit of 15 products reached. Stopping collection.")
                                subsubcat["product"] = products
                                return data 

                            ########################################################################

                        page += 1  

                    except requests.RequestException as e:
                        logging.error(f" _ erro subSubCat {sub_id} page {page}: {e}")
                        break

                subsubcat["product"] = products or []

    return data
