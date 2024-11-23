from datetime import datetime

from flask import session
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from marketplace.api.auth.rbac import auth_required, user_required, user_id_required
from marketplace.api.purchases.validation import PurchaseCreateSchema

from marketplace.models import db
from marketplace.models import Event as EventModel
from marketplace.models import Ticket as TicketModel
from marketplace.models import Purchase as PurchaseModel

namespace = Namespace('purchases', description='Purchases')

purchase_create_model = namespace.model('PurchaseCreate', {
    'ticket_id': fields.Integer(required=True, description='DateTime'),
    'quantity': fields.Integer(required=True, description='Description')
})

@namespace.route('/')
class PurchaseList(Resource):
    @namespace.doc('list_purchases')
    @auth_required
    @user_id_required
    def get(self):
        """List all purchases"""
        rv = [purchase.to_dict() for purchase in PurchaseModel.query.all()]
        return rv, 200

    @namespace.expect(purchase_create_model)
    @namespace.doc('create_purchase')
    @auth_required
    @user_required
    def post(self):
        """Create a new purchase"""
        try:
            data = PurchaseCreateSchema.model_validate(namespace.payload)
        except ValidationError as e:
            return {'Validation error': e.errors()}, 400

        ticket = TicketModel.query.get(data.ticket_id)
        if not ticket:
            return {'message': 'Ticket not found'}, 404

        event = EventModel.query.get(ticket.event_id)
        if not event:
            return {'message': f'Event for ticket {ticket.id} not found'}, 404

        if event.date < datetime.now():
            return {'message': 'Event is over'}, 404

        if ticket.quantity < data.quantity:
            return {'message': f'Only {ticket.quantity} left'}, 400

        user_id = session.get('user_id')
        purchase = PurchaseModel(
            user_id=user_id,
            ticket_id=data.ticket_id,
            quantity=data.quantity
        )
        ticket.quantity -= data.quantity

        db.session.add(purchase)
        db.session.commit()
        return {"message": "Purchase created successfully"}, 201

@namespace.route('/<int:purchase_id>')
@namespace.doc(params={'purchase_id': 'Purchase ID'})
class Purchase(Resource):
    @namespace.doc('get_purchase')
    @auth_required
    @user_id_required
    def get(self, purchase_id):
        """Get purchase by ID"""
        purchase = PurchaseModel.query.get(purchase_id)
        if not purchase:
            return {'message': 'Purchase not found'}, 404

        return purchase.to_dict(), 200
