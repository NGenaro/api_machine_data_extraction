import json
from pathlib import Path
from utils.base64_converter import encode_base64
from utils.pre_process import clean_bom  # Certifique-se de que esse caminho está correto

def output_formater(products):
    """
    Creates JSON output files for each product, including base64-encoded documents.

    Parameters:
        products (list) - List of product categories, each with subcategories and products.

    Returns:
        List of paths to the generated JSON files.

    Example use:
        output_paths = output_formater(products)
    """
    clean_bom(products)  # pré-processa os dados

    output_paths = []
    base_folder = Path("output/assets")

    for category in products:
        for subcat in category.get("subcategories", []):
            for subsub in subcat.get("sub_subcategory", []):
                for product in subsub.get("product", []):
                    code = product.get("code")
                    if not code:
                        continue

                    folder = base_folder / code
                    if not folder.exists():
                        continue

                    manual_path = folder / "manual.pdf"
                    cad_path = folder / "cad.dwg"
                    img_path = folder / "img.jpg"

                    docs_base64 = {
                        "manual": encode_base64(manual_path, ".pdf") if manual_path.exists() else None,
                        "cad": encode_base64(cad_path, ".dwg") if cad_path.exists() else None,
                        "image": encode_base64(img_path, ".jpg") if img_path.exists() else None
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
                            "frame": product.get("frame")
                        },
                        "bom": product.get("bom", []),
                        "assets": {
                            "manual": f"assets/{code}/manual.pdf" if manual_path.exists() else None,
                            "cad": f"assets/{code}/cad.dwg" if cad_path.exists() else None,
                            "image": f"assets/{code}/img.jpg" if img_path.exists() else None
                        },
                        "docs_base64": docs_base64
                    }

                    output_file = base_folder / f"{code}.json"
                    with open(output_file, "w", encoding="utf-8") as f:
                        json.dump(output_data, f, ensure_ascii=False, indent=2)

                    output_paths.append(str(output_file))

    return output_paths


# if __name__ == "__main__":
#     with open("data/products.json", "r", encoding="utf-8") as f:
#         raw_data = json.load(f)  # carrega como dict
#         products = list(raw_data) if isinstance(raw_data, list) else [raw_data]  # garante lista de dict

#     output_paths = output_formater(products)
#     print(f"Generated {len(output_paths)} JSON files.")
