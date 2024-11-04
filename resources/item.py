import uuid
from flask import  request
from flask_smorest import abort, Blueprint
from flask.views import MethodView
from db import items, stores

blp = Blueprint("Items", __name__, description="Operations on stores")

@blp.route("/item")
class Item(MethodView):
    def create_item(self):
        item_data = request.get_json()
        if "price" not in item_data or "store_id" not in item_data or "name" not in item_data:
            abort(404, message="Bad request. Ensure 'price', 'store_id' and 'name' are included in the JSON payload")
        for item in items.values():
            if item_data["name"] == item["name"] and item_data["store_id"] == item["store_id"]:
                abort(400, message=f"Store not found")
        if item_data["store_id"] not in stores:
            abort(404, message="Store not found")
        item_id = uuid.uuid4().hex
        item = {**item_data, "id": item_id}
        items[item_id] = item
        return item, 201

    def get_item(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found")


    def delete_item(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found")


    def update_item(self, item_id):
        item_data = request.get_json()
        if "price" not in item_data or "name" not in item_data:
            abort(400, message="Bad request. Ensure 'price, 'name' are included in the JSON payload")
        try:
            item = items[item_id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found")

@blp.route("/item")
class ItemList(MethodView):
    def get_all_items(self):
        return {"items": list(items.values())}