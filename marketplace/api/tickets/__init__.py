from datetime import datetime

from flask import session, url_for
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from marketplace.api.auth.rbac import auth_required
from marketplace.api.auth.rbac import partner_required
from marketplace.api.tickets.validation import TicketCreateSchema

from marketplace.models import db
from marketplace.models import Ticket as TicketModel
from marketplace.models import Event as EventModel

namespace = Namespace('tickets', description='Tickets')

ticket_create_model = namespace.model('TicketCreate', {
    'name': fields.String(required=True, description='Ticket name'),
    'price': fields.Float(required=True, description='Price'),
    'quantity': fields.String(required=True, description='Quantity'),
    'event_id': fields.Float(required=True, description='Event id'),
})

@namespace.route('/upcoming')
class UpcomingTicketList(Resource):
    @namespace.doc('list_upcoming_tickets')
    @auth_required
    def get(self):
        """List all tickets for upcoming events"""
        upcoming_events = db.session.query(EventModel).filter(EventModel.date > datetime.now()).all()
        upcoming_events_ids = [event.id for event in upcoming_events]
        rv = [ticket.to_dict() for ticket in TicketModel.query.all() if ticket.event_id in upcoming_events_ids]
        return rv, 200


@namespace.route('/')
class TicketList(Resource):
    @namespace.doc('list_tickets')
    @auth_required
    def get(self):
        """List all tickets"""
        rv = [ticket.to_dict() for ticket in TicketModel.query.all()]
        return rv, 200

    @namespace.expect(ticket_create_model)
    @namespace.doc('create_ticket')
    @partner_required
    def post(self):
        """Create a new ticket"""
        try:
            data = TicketCreateSchema.model_validate(namespace.payload)
        except ValidationError as e:
            return {'Validation error': e.errors()}, 400

        user_id = session.get('user_id')
        event = EventModel.query.filter_by(id=data.event_id).first()
        if event.user_id != user_id:
            return {'message': f'Event {data.event_id} for user {user_id} not found'}, 400

        ticket = TicketModel.query.filter_by(name=data.name, event_id=data.event_id).first()
        if not ticket:
            ticket = TicketModel(
                name=data.name,
                event_id=data.event_id,
                price = data.price,
                quantity = data.quantity
            )
            db.session.add(ticket)
            db.session.commit()
            return {"message": "Ticket created successfully"}, 201
        else:
            return {"message": "Ticket already exists"}, 409

@namespace.route('/<int:ticket_id>')
@namespace.doc(params={'ticket_id': 'Ticket ID'})
class Ticket(Resource):
    @namespace.doc('get_ticket')
    @auth_required
    def get(self, ticket_id):
        """Get ticket by ID"""
        ticket = EventModel.query.get(ticket_id)
        if not ticket:
            return {'message': 'Ticket not found'}, 404

        return ticket.to_dict(), 200
