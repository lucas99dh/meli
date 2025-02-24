import requests
import csv
import time
import os

# Define el directorio donde se guarda el archivo csv
output_dir = r""

# Verifica si el directorio existe, si no, lo crea
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# define que productos se va a buscar
search_terms = ["chromecast", "google home", "apple tv", "amazon fire tv"]

# Lista para guardar los  items
items_data = []

# Headers 
headers = {
    "User-Agent": "Mozilla/5.0"
}

def obtener_items_por_busqueda(term, limit=50, pages=3):
    """
    Funcion que obtiene una lista de item_ids para un termino de busqueda.
    Se setea 50 como limite y 3 paginas para llegar a un maximo de 150 items
    """
    item_ids = []
    for page in range(pages):
        offset = page * limit
        url = f"https://api.mercadolibre.com/sites/MLA/search?q={term}&limit={limit}&offset={offset}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for item in data.get("results", []):
                item_ids.append(item["id"])
        else:
            print(f"Error en la busqueda para '{term}' (pagina {page+1}): {response.status_code}")
    return item_ids

# Recopilar item_ids de todos los terminos de busqueda
all_item_ids = set()  # Se usa un set para evitar duplicados
for term in search_terms:
    ids = obtener_items_por_busqueda(term)
    all_item_ids.update(ids)
    print(f"Termino '{term}' obtuvo {len(ids)} items.")

print(f"Total de items obtenidos: {len(all_item_ids)}")

if len(all_item_ids) < 150:
    print("No se alcanzo la cantidad minima de 150 items")
else:
    print("Cantidad minima de items alcanzada")

# Funcion que realiza un GET a la API para obtener los detalles de un item dado su ID.
def obtener_detalles_item(item_id):
    url = f"https://api.mercadolibre.com/items/{item_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error obteniendo detalles del ítem {item_id}: {response.status_code}")
        return None
    
# Funcion para quedarme con los campos del json que quiero
def extraer_campos(item_json):
    return {
        "id": item_json.get("id"),
        "title": item_json.get("title"),
        "category_id": item_json.get("category_id"),
        "price": item_json.get("price"),
        "currency_id": item_json.get("currency_id"),
        "condition": item_json.get("condition"),
        "initial_quantity": item_json.get("initial_quantity"),
        "seller_id": item_json.get("seller_id"),
        "seller_address": item_json.get("seller_address", {}).get("city", {}).get("name"),
        "permalink": item_json.get("permalink")
    }

# Obtener detalles de cada item y guardar la informacion
for count, item_id in enumerate(all_item_ids, start=1):
    item_json = obtener_detalles_item(item_id)
    if item_json:
        datos = extraer_campos(item_json)
        items_data.append(datos)
    if count % 10 == 0:
        print(f"{count} ítems procesados...")

print(f"Total de items procesados: {len(items_data)}")

# Escribir los resultados en un archivo CSV delimitado por comas
csv_file = os.path.join(output_dir, "mercadolibre_items.csv")
fieldnames = [
    "id", "title", "category_id", "price", "currency_id", "condition",
    "initial_quantity", "seller_id", "seller_address", "permalink"
]

with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    for item in items_data:
        writer.writerow(item)

print(f"Archivo generado en: {csv_file}")