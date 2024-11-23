from flask_restx import Namespace, fields, Resource
from pydantic import ValidationError

from marketplace.api.auth.rbac import auth_required
from marketplace.api.auth.validation import LoginSchema
from marketplace.models import User as UserModel

from flask import session

namespace = Namespace('auth', description='Authentication')

login_model = namespace.model('Login', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
})

@namespace.route('/login')
class Login(Resource):
    @namespace.expect(login_model)
    def post(self):
        """Login a user"""
        try:
            data = LoginSchema.model_validate(namespace.payload)
        except ValidationError as e:
            return {'Validation error': e.errors()}, 400

        user = UserModel.query.filter_by(username=data.username).first()
        if user and user.check_password(data.password) and user.is_active:
            session['user_id'] = user.id
            session['is_user'] = user.is_user
            session['is_admin'] = user.is_admin
            session['is_partner'] = user.is_partner
            session['is_active'] = user.is_active
            return {'message': 'Login successful'}, 200

        return {'message': 'Invalid username or password'}, 401


@namespace.route('/logout')
class Logout(Resource):
    def post(self):
        """Logout a user"""
        session.pop('user_id', None)
        return {'message': 'Logged out'}, 200

@namespace.route('/current')
class CurrentUser(Resource):
    @auth_required
    def get(self):
        """Current user"""
        user_id = session.get('user_id')
        user = UserModel.query.filter_by(id=user_id).first()
        if user:
            return user.to_dict(), 200
