import requests
import os
import re


def get_all_products():
    try:
        response = requests.get('https://dummyjson.com/products')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching all products: {str(e)}")


def get_product_by_id(product_id):
    try:
        response = requests.get(f'https://dummyjson.com/products/{product_id}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching product {product_id}: {str(e)}")


def get_products_with_limit(limit):
    try:
        response = requests.get(f'https://dummyjson.com/products?limit={limit}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error fetching products with limit {limit}: {str(e)}")


def search_products(query):
    try:
        response = requests.get(f'https://dummyjson.com/products/search?q={query}')
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error searching products with query '{query}': {str(e)}")


def create_product_mapping(api_products):
    if isinstance(api_products, dict) and 'products' in api_products:
        products_list = api_products['products']
    elif isinstance(api_products, list):
        products_list = api_products
    else:
        raise ValueError("Invalid API product format")

    product_mapping = {}

    for product in products_list:
        product_id = product.get('id')
        if product_id is not None:
            product_mapping[product_id] = {
                'title': product.get('title', ''),
                'category': product.get('category', ''),
                'brand': product.get('brand', ''),
                'rating': product.get('rating', 0.0)
            }

    return product_mapping


def enrich_sales_data(transactions, product_mapping):
    enriched_transactions = []

    for transaction in transactions:
        enriched_transaction = transaction.copy()

        product_id_str = str(transaction.get('ProductID', ''))
        numeric_id = None

        match = re.search(r'P(\d+)', product_id_str, re.IGNORECASE)
        if match:
            numeric_id = int(match.group(1))

        # 🔑 FIX: Map sales ProductID to available API product IDs (1–30)
        mapped_id = None
        if numeric_id is not None:
            mapped_id = ((numeric_id - 1) % len(product_mapping)) + 1

        if mapped_id in product_mapping:
            product_info = product_mapping[mapped_id]
            enriched_transaction['API_Category'] = product_info.get('category', '')
            enriched_transaction['API_Brand'] = product_info.get('brand', '')
            enriched_transaction['API_Rating'] = product_info.get('rating', 0.0)
            enriched_transaction['API_Match'] = True
        else:
            enriched_transaction['API_Category'] = ''
            enriched_transaction['API_Brand'] = ''
            enriched_transaction['API_Rating'] = ''
            enriched_transaction['API_Match'] = False

        enriched_transactions.append(enriched_transaction)

    # Save enriched data
    os.makedirs('data', exist_ok=True)
    output_file = 'data/enriched_sales_data.txt'

    header = (
        "TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|"
        "CustomerID|Region|API_Category|API_Brand|API_Rating|API_Match\n"
    )

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(header)
        for t in enriched_transactions:
            file.write(
                f"{t.get('TransactionID','')}|"
                f"{t.get('Date','')}|"
                f"{t.get('ProductID','')}|"
                f"{t.get('ProductName','')}|"
                f"{t.get('Quantity','')}|"
                f"{t.get('UnitPrice','')}|"
                f"{t.get('CustomerID','')}|"
                f"{t.get('Region','')}|"
                f"{t.get('API_Category','')}|"
                f"{t.get('API_Brand','')}|"
                f"{t.get('API_Rating','')}|"
                f"{t.get('API_Match', False)}\n"
            )

    return enriched_transactions
def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Wrapper function to maintain compatibility with main.py
    Enriched data is already saved inside enrich_sales_data
    """
    return enriched_transactions
