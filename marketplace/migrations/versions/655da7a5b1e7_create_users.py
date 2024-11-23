"""'create_users'

Revision ID: 655da7a5b1e7
Revises: 6edeba9920c9
Create Date: 2024-11-23 02:28:50.376390

"""
from alembic import op
from sqlalchemy.orm import Session

from marketplace.models import User, UserRole
from marketplace.models.users import UserState


# revision identifiers, used by Alembic.
revision = '655da7a5b1e7'
down_revision = '6edeba9920c9'
branch_labels = None
depends_on = None


def upgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    if not session.query(User).filter(User.username == "admin").first():
        default_admin = User(username="admin", role=UserRole.admin)
        default_admin.set_password('admin')
        session.add(default_admin)

    if not session.query(User).filter(User.username == "partner").first():
        default_partner = User(username="partner", role=UserRole.partner)
        default_partner.set_password('partner')
        session.add(default_partner)

    if not session.query(User).filter(User.username == "user").first():
        default_user = User(username="user", role=UserRole.user)
        default_user.set_password('user')
        session.add(default_user)

    if not session.query(User).filter(User.username == "inactive").first():
        default_inactive = User(username="inactive", role=UserRole.user, state=UserState.inactive)
        default_inactive.set_password('inactive')
        session.add(default_inactive)

    session.commit()


def downgrade():
    bind = op.get_bind()
    session = Session(bind=bind)

    default_admin = session.query(User).filter(User.username == "admin").first()
    if default_admin:
        session.delete(default_admin)

    default_partner = session.query(User).filter(User.username == "partner").first()
    if default_partner:
     session.delete(default_partner)

    default_user = session.query(User).filter(User.username == "user").first()
    if default_user:
        session.delete(default_user)

    default_inactive = session.query(User).filter(User.username == "inactive").first()
    if default_inactive:
        session.delete(default_inactive)

    session.commit()
