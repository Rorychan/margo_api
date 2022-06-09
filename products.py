import json
import random

products = []
with open("./products.json") as f:
    products = json.load(f)

for i in range(len(products)):
    products[i].pop("id")
    products[i].pop("currency")
    products[i].pop("product_link")
    products[i].pop("website_link")
    products[i].pop("rating")
    products[i].pop("tag_list")
    products[i].pop("created_at")
    products[i].pop("updated_at")
    products[i].pop("product_api_url")
    products[i].pop("api_featured_image")
    products[i].pop("product_colors")
print(len(products))
products = list(filter(lambda i: i['brand'] != None, products))
products = list(filter(lambda i: i['category'] != "", products))
print(len(products))
for product in products:
    product["brand_name"] = product.pop("brand")
    product["category_name"] = product.pop("category")
    product["product_type_name"] = product.pop("product_type")
    if product["category_name"] == None:
        product["category_name"] = "without_category"
    if product["price"] == None or product["price"] == "":
        product["price"] == str(random.uniform(0.5, 50))
    if product["price_sign"] == None or product["price_sign"]:
        product["price_sign"] = "$"

with open("./products_new.json", "w") as f:
    f.write(json.dumps(products))
