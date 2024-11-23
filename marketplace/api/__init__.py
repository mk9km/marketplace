from flask import Blueprint
from flask_restx import Api

from .auth import namespace as auth_namespace
from .events import namespace as events_namespace
from .purchases import namespace as purchases_namespace
from .tickets import namespace as tickets_namespace
from .users import namespace as users_namespace

blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(blueprint)
api.add_namespace(auth_namespace)
api.add_namespace(events_namespace)
api.add_namespace(purchases_namespace)
api.add_namespace(tickets_namespace)
api.add_namespace(users_namespace)
