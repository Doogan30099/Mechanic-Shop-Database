from .ServiceTicketSchema import service_ticket_schema, service_tickets_schema
from flask import request, jsonify 
from marshmallow import ValidationError
from sqlalchemy import select
from application.models import ServiceTicket, db
from . import service_ticket_bp
from application.models import Mechanic


@service_ticket_bp.route("/", methods=['POST'])
def create_service_ticket():
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages),400
    


    query = select(ServiceTicket).where(ServiceTicket.customer == service_ticket_data['customer'])
    existing_service_ticket = db.session.execute(query).scalars().all()
    if existing_service_ticket:
        return jsonify({"error": "Service Ticket already associated with an account."}), 400
    
    new_service_ticket = ServiceTicket(**service_ticket_data)
    db.session.add(new_service_ticket)
    db.session.commit()
    return service_ticket_schema.jsonify(new_service_ticket), 201


#GET ALL SERVICE TICKETS
@service_ticket_bp.route("/", methods=['GET'])
def get_service_tickets():
    query = select(ServiceTicket)
    service_tickets = db.session.execute(query).scalars().all()
    return service_tickets_schema.jsonify(service_tickets)

#GET SPECIFIC SERVICE TICKET
@service_ticket_bp.route("/<int:service_ticket_id>", methods=['GET'])
def get_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if service_ticket:
        return service_ticket_schema.jsonify(service_ticket), 200
    return jsonify({"error": "Service Ticket not found."}), 404

#UPDATE SPECIFIC SERVICE TICKET
@service_ticket_bp.route("/<int:service_ticket_id>/edit", methods=['PUT'])
def update_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)
    mechanic_id = db.session.get(Mechanic.id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found."}), 404
    
    add_ids = request.json.get('add_ids', [])
    remove_ids = request.json.get('remove_ids', [])

    if add_ids is None:
        query = select(Mechanic).where(Mechanic.id.in_(add_ids))
        mechanics_to_add = db.session.execute(query).scalars().all()
        for mechanic in mechanics_to_add:
            service_ticket.mechanics.append(mechanic)
    
    if remove_ids is None:
        query = select(Mechanic).where(Mechanic.id.in_(remove_ids))
        mechanics_to_remove = db.session.execute(query).scalars().all()
        for mechanic in mechanics_to_remove:
            service_ticket.mechanics.remove(mechanic)
    
    try:
        service_ticket_data = service_ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    
    for key, value in service_ticket_data.items():
        setattr(service_ticket, key, value)

    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

#UPDATE add mechanic id to SERVICE TICKET
@service_ticket_bp.route("/<int:service_ticket_id>/assign_mechanic/<int:mechanic_id>", methods=['PUT'])
def assign_mechanic_to_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found."}), 404
    # Assign only the mechanic_id; don't require or process a request body
    service_ticket.mechanic_id = mechanic_id
    service_ticket.assigned_mechanic = db.session.get(Mechanic, mechanic_id).name
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200


#UPDATE remove mechanic id from SERVICE TICKET
@service_ticket_bp.route("/<int:service_ticket_id>/remove_mechanic/<int:mechanic_id>", methods=['PUT'])
def remove_mechanic_from_service_ticket(service_ticket_id, mechanic_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found."}), 404
    # Ensure the mechanic being removed matches the currently assigned mechanic (optional safety check)
    if service_ticket.mechanic_id is not None and service_ticket.mechanic_id != mechanic_id:
        return jsonify({"error": "Mechanic id does not match the assigned mechanic for this ticket."}), 400

    # Clear both the foreign key and the stored assigned_mechanic name
    service_ticket.mechanic_id = None
    service_ticket.assigned_mechanic = None
    db.session.commit()
    return service_ticket_schema.jsonify(service_ticket), 200

#DELETE SPECIFIC SERVICE TICKET
@service_ticket_bp.route("/<int:service_ticket_id>", methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    service_ticket = db.session.get(ServiceTicket, service_ticket_id)

    if not service_ticket:
        return jsonify({"error": "Service Ticket not found."}), 404
    
    db.session.delete(service_ticket)
    db.session.commit()
    return jsonify({"message": f'Service Ticket id: {service_ticket_id}, successfully deleted.'}), 200