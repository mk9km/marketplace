from datetime import datetime
from flask import session
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from marketplace.api.auth.rbac import auth_required
from marketplace.api.auth.rbac import partner_required
from marketplace.api.events.validation import EventCreateSchema

from marketplace.models import db
from marketplace.models import Event as EventModel

namespace = Namespace('events', description='Events')

event_create_model = namespace.model('EventCreate', {
    'name': fields.String(required=True, description='Event name'),
    'date': fields.DateTime(required=True, description='DateTime'),
    'description': fields.String(required=True, description='Description')
})

@namespace.route('/upcoming')
class UpcomingEventList(Resource):
    @namespace.doc('list_upcoming_events')
    @auth_required
    def get(self):
        """List all upcoming events"""
        upcoming_events = db.session.query(EventModel).filter(EventModel.date > datetime.now()).all()
        rv = [event.to_dict() for event in upcoming_events]
        return rv, 200


@namespace.route('/')
class EventList(Resource):
    @namespace.doc('list_events')
    @auth_required
    def get(self):
        """List all events"""
        rv = [event.to_dict() for event in EventModel.query.all()]
        return rv, 200

    @namespace.expect(event_create_model)
    @namespace.doc('create_event')
    @auth_required
    @partner_required
    def post(self):
        """Create a new event"""
        try:
            data = EventCreateSchema.model_validate(namespace.payload)
        except ValidationError as e:
            return {'Validation error': e.errors()}, 400

        user_id = session.get('user_id')
        event = EventModel.query.filter_by(user_id=user_id, name=data.name).first()
        if not event:
            event = EventModel(
                user_id=user_id,
                name=data.name,
                date=data.date,
                description=data.description
            )
            db.session.add(event)
            db.session.commit()
            return {'message': 'Event created successfully'}, 201
        else:
            return {'message': 'Event already exists'}, 409

@namespace.route('/<int:event_id>')
@namespace.doc(params={'event_id': 'Event ID'})
class Event(Resource):
    @namespace.doc('get_event')
    @auth_required
    def get(self, user_id):
        """Get event by ID"""
        event = EventModel.query.get(user_id)
        if not event:
            return {'message': 'Event not found'}, 404

        return event.to_dict(), 200
