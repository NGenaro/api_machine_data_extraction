##########################################################################################################
# Function to removing invalid items #####################################################################
##########################################################################################################

def clean_bom(data):
    """
    Function to clean the BOM data for each product.

    Parameters:
      data: list of categories, subcategories, and products.

    Returns:
        None
    
    Example to use:
        clean_bom(data)
    """
    def is_valid(item: dict) -> bool:
        pn   = (item.get("part_number") or "").strip()
        desc = (item.get("description")  or "").strip()
        qty  = (item.get("quantity")     or "").strip()
        return pn and len(pn) >= 6 and desc and qty

    for cat in data:
        for sub in cat.get("subcategories", []):
            for subsub in sub.get("sub_subcategory", []):
                for prod in subsub.get("product", []):
                    bom = prod.get("bom", [])
                    prod["bom"] = [item for item in bom if is_valid(item)]
