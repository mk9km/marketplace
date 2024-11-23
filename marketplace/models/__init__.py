from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migration = Migrate()

from .events import Event
from .purchases import Purchase
from .tickets import Ticket
from .users import User
from .users import UserRole
from .users import UserState
