import logging
import requests
import json

def fetch_category_data():
    """
    Fetches basic category data from the Baldor API.

    Parameters:
        None

    Returns:
        A list of dictionaries containing:
            - 'id': category ID
            - 'text': category name
            - 'count': number of products in the category
            - 'imageId': category image ID
    
    Example usage:
        data = fetch_category_data()
    """
    url = "https://www.baldor.com/api/products?include=results&language=en-US&include=filters&include=category&pageSize=10"

    try:
        # Define headers to mimic a browser request
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                          "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
            "Accept": "application/json"
        }

        response = requests.get(url, headers=headers)  # <--- agora com headers
        response.raise_for_status()
        data = response.json()

        categories = data.get("category", {}).get("children", [])
        category_data = []

        for category in categories:
            item = {
                "id": category.get("id"),
                "text": category.get("text"),
                "count": category.get("count"),
                "imageId": category.get("imageId")
            }
            category_data.append(item)

            logging.info(
                f"\n - Category ID: {item['id']} \n - Name: {item['text']} \n - Count: {item['count']}"
            )

        return category_data

    except requests.RequestException as e:
        logging.error(f"Error accessing the API: {e}")
        return []

# example usage
# if __name__ == "__main__":
#     data = fetch_category_data()
#     if data:
#         with open("category_data.json", "w") as f:
#             json.dump(data, f, indent=2)
#         print("Category data saved to category_data.json")
#     else:
#         print("No data retrieved.")
