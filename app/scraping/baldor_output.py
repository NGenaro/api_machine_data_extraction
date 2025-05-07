import json
from pathlib import Path
from utils.base64_converter import encode_base64
from utils.pre_process import clean_bom 

##########################################################################################################
# Funcrion to format baldor website output ###############################################################
##########################################################################################################

def output_formater(products):
    """
    Creates JSON output files for each product, including base64-encoded documents.

    Parameters:
        products (list) - List of product categories, each with subcategories and products.

    Returns:
        A dictionary containing the paths to the generated JSON files and the enriched product data.
        - "output_paths": List of paths to the generated JSON files.
        - "products_enriched": List of products with additional data.

    Example use:
        output_paths = output_formater(products)
    """

    clean_bom(products)

    base_folder = Path("output/assets")     
    json_out_dir = Path("output")           
    json_out_dir.mkdir(parents=True, exist_ok=True)

    output_paths = []

    for category in products:
        for subcat in category.get("subcategories", []):
            for subsub in subcat.get("sub_subcategory", []):
                products_list = subsub.setdefault("product", [])

                for product in products_list:
                    code = product.get("code")
                    if not code:
                        continue

                    folder      = base_folder / code
                    manual_path = folder / "manual.pdf"
                    cad_path    = folder / "cad.dwg"
                    img_path    = folder / "img.jpg"
                    json_path   = json_out_dir / f"{code}.json"   # agora é Path

                    docs_base64 = {
                        "manual": encode_base64(manual_path, ".pdf") if manual_path.exists() else None,
                        "cad"   : encode_base64(cad_path,  ".dwg") if cad_path.exists() else None,
                        "image" : encode_base64(img_path,  ".jpg") if img_path.exists() else None,
                    }

                    output_data = {
                        "product_id": code,
                        "name": "Motor AC Trifásico",
                        "description": product.get("description"),
                        "upc": product.get("upc"),
                        "USD": product.get("USD"),
                        "specs": {
                            "hp": product.get("output_at_frequency"),
                            "voltage": product.get("voltage_at_frequency"),
                            "rpm": product.get("synchronous_speed_at_freq"),
                            "frame": product.get("frame"),
                        },
                        "bom": product.get("bom", []),
                        "assets": {
                            "manual": f"assets/{code}/manual.pdf" if manual_path.exists() else None,
                            "cad": f"assets/{code}/cad.dwg" if cad_path.exists() else None,
                            "image": f"assets/{code}/img.jpg" if img_path.exists() else None,
                        },
                        "docs_base64": docs_base64,
                    }

                    json_path.write_text(
                        json.dumps(output_data, ensure_ascii=False, indent=2),
                        encoding="utf-8",
                    )
                    output_paths.append(json_path.as_posix())

                    product.update(output_data)

    return {"output_paths": output_paths, "products_enriched": products,}
