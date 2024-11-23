"""'create_tickets'

Revision ID: 1d2440bf7df4
Revises: f488c5e345ed
Create Date: 2024-11-23 03:49:52.457827

"""
from alembic import op
from sqlalchemy.orm import Session

from marketplace.models import Ticket


# revision identifiers, used by Alembic.
revision = '1d2440bf7df4'
down_revision = 'f488c5e345ed'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    if not session.query(Ticket).filter(Ticket.name == 'beer_event_ticket').first():
        beer_event_ticket = Ticket(name='beer_event_ticket', event_id=1, price=100, quantity=3)
        session.add(beer_event_ticket)

    if not session.query(Ticket).filter(Ticket.name == 'dance_event_ticket').first():
        dance_event_ticket = Ticket(name='dance_event_ticket', event_id=2, price=150, quantity=3)
        session.add(dance_event_ticket)

    if not session.query(Ticket).filter(Ticket.name == 'sport_event_ticket').first():
        sport_event_ticket = Ticket(name='sport_event_ticket', event_id=3, price=300, quantity=3)
        session.add(sport_event_ticket)

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    beer_event_ticket = session.query(Ticket).filter(Ticket.name == 'beer_event_ticket').first()
    if beer_event_ticket:
        session.delete(beer_event_ticket)

    dance_event_ticket = session.query(Ticket).filter(Ticket.name == 'dance_event_ticket').first()
    if dance_event_ticket:
        session.delete(dance_event_ticket)

    sport_event_ticket = session.query(Ticket).filter(Ticket.name == 'sport_event_ticket').first()
    if beer_event_ticket:
        session.delete(sport_event_ticket)

    session.commit()
