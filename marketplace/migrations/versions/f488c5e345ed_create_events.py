"""'create_events'

Revision ID: f488c5e345ed
Revises: 655da7a5b1e7
Create Date: 2024-11-23 02:43:45.075737

"""
from datetime import datetime, timedelta

from alembic import op
from sqlalchemy.orm import Session

from marketplace.models import Event

# revision identifiers, used by Alembic.
revision = 'f488c5e345ed'
down_revision = '655da7a5b1e7'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    now = datetime.now()
    delta = timedelta(days=30)

    if not session.query(Event).filter(Event.name == 'beer_event').first():
        beer_event = Event(name='beer_event', user_id=2, date=now+delta, description='Beer event')
        session.add(beer_event)

    if not session.query(Event).filter(Event.name == 'dance_event').first():
        dance_event = Event(name='dance_event', user_id=2, date=now+delta, description='Dance event')
        session.add(dance_event)

    if not session.query(Event).filter(Event.name == 'sport_event').first():
        sport_event = Event(name='sport_event', user_id=2, date=now-delta, description='Sport event')
        session.add(sport_event)

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    beer_event = session.query(Event).filter(Event.name == 'beer_event').first()
    if beer_event:
        session.delete(beer_event)

    dance_event = session.query(Event).filter(Event.name == 'dance_event').first()
    if dance_event:
        session.delete(dance_event)

    sport_event = session.query(Event).filter(Event.name == 'sport_event').first()
    if beer_event:
        session.delete(sport_event)

    session.commit()
