import json
from pathlib import Path
import logging

##########################################################################################################
# Funcrion to format final output ########################################################################
##########################################################################################################

def build_final_output(data):
    """
    Merge detailed product JSONs back into the original category hierarchy structure.

    Parameters:
        data (List[dict]) - Hierarchical data with categories → subcategories → sub-subcategories → product codes.

    Returns:
        List[dict] - Complete nested structure with product JSONs fully embedded.

    Example use:
        final_output = build_final_output(data)
    """

    product_jsons = {}
    for file in Path("output").glob("*.json"):
        try:
            with open(file, "r", encoding="utf-8") as f:
                prod_data = json.load(f)
                code = prod_data.get("product_id")
                if code:
                    product_jsons[code] = prod_data
        except Exception as e:
            logging.error(f"  |  |_ Error loading product JSON {file}: {e}")

    final_structure = []

    for category in data:
        cat_entry = {
            "category_id": category.get("id"),
            "name": category.get("text"),
            "count": category.get("count"),
            "subcategories": []
        }

        for subcat in category.get("subcategories", []):
            subcat_entry = {
                "subcategory_id": subcat.get("id"),
                "name": subcat.get("text"),
                "count": subcat.get("count"),
                "sub_subcategory": []
            }

            for subsub in subcat.get("sub_subcategory", []):
                subsub_entry = {
                    "sub_subcategory_id": subsub.get("id"),
                    "name": subsub.get("text"),
                    "count": subsub.get("count"),
                    "product": []
                }

                for product in subsub.get("product", []):
                    code = product.get("code")
                    if code in product_jsons:
                        subsub_entry["product"].append(product_jsons[code])

                subcat_entry["sub_subcategory"].append(subsub_entry)
            cat_entry["subcategories"].append(subcat_entry)

        final_structure.append(cat_entry)

    return final_structure
