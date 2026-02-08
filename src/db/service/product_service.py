from db.mongo_connection import get_db


def get_products():
    db = get_db()
    return list(db["Products"].find())

def get_next_id():
    db = get_db()
    last_product = db["Products"].find_one(sort=[("ID", -1)])
    if last_product and "ID" in last_product:
        return last_product["ID"] + 1
    return 1


def insert_product(product):
    db = get_db()

    product["ID"] = get_next_id()

    try:
        product["UnitPerBox"] = int(product["UnitPerBox"])
    except (ValueError, TypeError):
        raise ValueError("UnitPerBox deve ser um número inteiro.")

    try:
        if isinstance(product["BuyPrice"], str):
            product["BuyPrice"] = product["BuyPrice"].replace(",", ".")
        product["BuyPrice"] = float(product["BuyPrice"])
    except (ValueError, TypeError):
        raise ValueError("BuyPrice deve ser um número decimal válido.")

    result = db["Products"].insert_one(product)
    return result.inserted_id

def update_product(product):
    db = get_db()

    try:
        product["UnitPerBox"] = int(product["UnitPerBox"])
    except (ValueError, TypeError):
        raise ValueError("UnitPerBox deve ser um número inteiro.")

    try:
        if isinstance(product["BuyPrice"], str):
            product["BuyPrice"] = product["BuyPrice"].replace(",", ".")
        product["BuyPrice"] = float(product["BuyPrice"])
    except (ValueError, TypeError):
        raise ValueError("BuyPrice deve ser um número decimal válido.")

    result = db["Products"].update_one(
        {"SKU": product["SKU"]},
        {"$set": {
            "Type": product["Type"],
            "Description": product["Description"],
            "BuyPrice": product["BuyPrice"],
            "UnitPerBox": product["UnitPerBox"]
        }}
    )

    return result.modified_count