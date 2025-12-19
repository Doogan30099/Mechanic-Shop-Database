from .mechanicSchemas import inventory_schema, inventories_schema
from flask import request, jsonify 
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import Inventory, db
from . import inventory_bp


#CREATE NEW INVENTORY ITEM
@inventory_bp.route("/", methods=['POST'])
def create_item():
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    


    query = select(Inventory).where(Inventory.item_name == inventory_data['item_name'])
    existing_item = db.session.execute(query).scalars().all()
    if existing_item:
        inventory_data.quantity += existing_item[0].quantity
        existing_item[0].quantity = inventory_data.quantity
    
    new_inventory = Inventory(**inventory_data)
    db.session.add(new_inventory)
    db.session.commit()
    return inventory_schema.jsonify(new_inventory), 201


#GET ALL INVENTORY ITEMS
@inventory_bp.route("/", methods=['GET'])
def get_inventory_items():
    query = select(Inventory)
    inventories = db.session.execute(query).scalars().all()
    return inventories_schema.jsonify(inventories)

#GET SPECIFIC INVENTORY ITEM
@inventory_bp.route("/<int:inventory_id>", methods=['GET'])
def get_inventory_item(inventory_id):
    inventory_item = db.session.get(Inventory, inventory_id)

    if inventory_item:
        return inventory_schema.jsonify(inventory_item), 200
    return jsonify({"error": "Inventory item not found."}), 404

#UPDATE SPECIFIC INVENTORY ITEM
@inventory_bp.route("/<int:inventory_id>", methods=['PUT'])
def update_inventory_item(inventory_id):
    inventory_item = db.session.get(Inventory, inventory_id)

    if not inventory_item:
        return jsonify({"error": "Inventory item not found."}), 404
    
    try:
        inventory_data = inventory_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in inventory_data.items():
        setattr(inventory_item, key, value)

    db.session.commit()
    return inventory_schema.jsonify(inventory_item), 200

#DELETE SPECIFIC INVENTORY ITEM
@inventory_bp.route("/<int:inventory_id>", methods=['DELETE'])
def delete_inventory_item(inventory_id):
    inventory_item = db.session.get(Inventory, inventory_id)

    if not inventory_item:
        return jsonify({"error": "Inventory item not found."}), 404
    
    db.session.delete(inventory_item)
    db.session.commit()
    return jsonify({"message": f'Inventory item id: {inventory_id}, successfully deleted.'}), 200