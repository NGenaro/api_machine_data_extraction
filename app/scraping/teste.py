# from playwright.sync_api import sync_playwright

# import requests 
# import random
# import json


# def fetch_baldor_products(config: dict, headers: dict, timeout: tuple) -> list:
#     """
#     Fetches products from Baldor's API using pagination.
#     """
#     base_url = "https://www.baldor.com/api/products"
#     total_pages = (config["total_expected"] + config["page_size"] - 1) // config["page_size"]
#     all_products = []

#     for page_index in range(total_pages):
#         params = {
#             "include": "results",
#             "language": "en-US",
#             "category": str(config["category_id"]),
#             "pageSize": config["page_size"],
#             "pageIndex": page_index,
#         }

#         try:
#             response = requests.get(base_url, headers=headers, params=params, timeout=timeout)
#             response.raise_for_status()
#             matches = response.json()["results"].get("matches", [])
#             all_products.extend(matches)
#             print(f"[INFO] Page {page_index + 1}/{total_pages}: {len(matches)} products collected.")
#         except Exception as e:
#             print(f"[ERROR] Page {page_index + 1}: {e}")

#     return all_products


# def save_sampled_products(products: list, k: int, output_path: str) -> None:
#     """
#     Saves a random sample of unique products to JSON.
#     """
#     unique_products = {p["code"]: p for p in products}.values()
#     sampled = random.sample(list(unique_products), min(k, len(unique_products)))

#     with open(output_path, "w") as f:
#         json.dump(sampled, f, indent=2)

#     print(f"[INFO] {len(sampled)} products saved to {output_path}")
    
# def renovar_cookies_baldor():
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)
#         context = browser.new_context()
#         page = context.new_page()
#         page.goto("https://www.baldor.com/products")

#         input("➡️ Faça login ou aguarde o carregamento completo. Pressione ENTER para continuar...")

#         cookies = context.cookies()
#         browser.close()

#         # Gera string de Cookie para requests
#         cookie_header = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
#         return cookie_header

# def montar_headers(cookie_string: str) -> dict:
#     return {
#         "User-Agent": "Mozilla/5.0",
#         "Accept": "application/json",
#         "Cookie": cookie_string
#     }

# if __name__ == "__main__":
#     cookie_string = renovar_cookies_baldor()
#     headers = montar_headers(cookie_string)

#     config = {
#         "category_id": 123,         # ajuste conforme a categoria desejada
#         "page_size": 50,
#         "total_expected": 3000,     # estimativa para calcular o total de páginas
#     }

#     timeout = (5, 15)
#     products = fetch_baldor_products(config, headers, timeout)
#     save_sampled_products(products, k=100, output_path="produtos_amostrados.json")


import requests, bs4, time

url = "https://www.baldor.com/catalog?page={}"
headers = {"User-Agent": "Mozilla/5.0 ..."}
page = 1
skus = set()

while True:
    r = requests.get(url.format(page), headers=headers, timeout=30)
    soup = bs4.BeautifulSoup(r.text, "html.parser")
    items = soup.select("div.catalog-product[data-sku]")
    if not items:
        break
    skus.update(i["data-sku"] for i in items)
    page += 1
    time.sleep(1.5)            # para não ser bloqueado
    print(f"Page {page} done. Found {len(skus)} SKUs.")


