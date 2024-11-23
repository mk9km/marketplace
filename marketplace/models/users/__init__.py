from flask_login import UserMixin
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash, generate_password_hash

from marketplace.models import db
from marketplace.models.base import EnumBase


class UserRole(EnumBase):
    admin = 'admin'
    partner = 'partner'
    user = 'user'


class UserState(EnumBase):
    active = 'active'
    inactive = 'inactive'
    deleted = 'deleted'


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum(UserRole), default=UserRole.user, nullable=False)
    state = db.Column(db.Enum(UserState), default=UserState.active, nullable=False)

    purchases = relationship('Purchase', back_populates='user')

    def __repr__(self):
        return f'<User {self.username!r}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_user(self):
        return self.role == UserRole.user

    @property
    def is_admin(self):
        return self.role == UserRole.admin

    @property
    def is_partner(self):
        return self.role == UserRole.partner

    @property
    def is_active(self):
        return self.state == UserState.active

    @property
    def is_inactive(self):
        return self.state == UserState.inactive

    @property
    def is_deleted(self):
        return self.state == UserState.deleted

    def to_dict(self):
        rv = {
            'id': self.id,
            'username': self.username,
            'role': self.role.value,
            'state': self.state.value
        }
        return rv
