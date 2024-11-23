from flask import session
from flask_restx import Namespace, Resource, fields
from pydantic import ValidationError

from marketplace.api.auth.rbac import auth_required
from marketplace.api.auth.rbac import admin_required, admin_or_user_id_required
from marketplace.api.users.validation import UserCreateSchema, UserModifySchema, UserModifyByAdminSchema

from marketplace.models import db
from marketplace.models import User as UserModel
from marketplace.models import UserRole, UserState

namespace = Namespace('users', description='Users')

user_create_model = namespace.model('UserCreate', {
    'username': fields.String(required=True, description='Username'),
    'password': fields.String(required=True, description='Password'),
    'role': fields.String(
        required=False, description='User role',
        enum=[role.value for role in (UserRole.user, UserRole.partner)]
    ),
})

user_modify_model = namespace.model('UserModify', {
    'password': fields.String(required=True, description='Password'),
    'role': fields.String(
        required=False, description='User role',
        enum=[role.value for role in UserRole]
    ),
    'state': fields.String(
        required=False, description='User states',
        enum=[state.value for state in UserState]
    )
})

@namespace.route('/')
class UserList(Resource):
    @namespace.doc('list_users')
    @auth_required
    @admin_required
    def get(self):
        """List all users"""
        rv = [user.to_dict() for user in UserModel.query.all()]
        return rv, 200

    @namespace.expect(user_create_model)
    @namespace.doc('create_user')
    def post(self):
        """Create a new user"""
        try:
            data = UserCreateSchema.model_validate(namespace.payload)
        except ValidationError as e:
            return {'Validation error': e.errors()}, 400

        user = UserModel.query.filter_by(username=data.username).first()
        if not user:
            user = UserModel(
                username=data.username
            )
            user.set_password(data.password)

            if data.role == UserRole.admin and session.get('is_admin'):
                user.role = data.role
                return {'message': '1'}, 200
            elif data.role == UserRole.admin and not session.get('is_admin'):
                return {'message': 'Forbidden: Insufficient permissions'}, 403
            else:
                user.role = data.role

            db.session.add(user)
            db.session.commit()
            return {'message': 'User created successfully'}, 201
        else:
            return {'message': 'User already exists'}, 409


@namespace.route('/roles')
class UserRoleList(Resource):
    @namespace.doc('list_user_roles')
    @auth_required
    def get(self):
        """List all built-in user roles"""
        rv = [role.value for role in UserRole]
        return rv, 200


@namespace.route('/states')
class UserStateList(Resource):
    @namespace.doc('list_user_states')
    @auth_required
    def get(self):
        """List all built-in user states"""
        rv = [role.value for role in UserState]
        return rv, 200


@namespace.route('/<int:user_id>')
@namespace.doc(params={'user_id': 'User ID'})
class User(Resource):
    @namespace.doc('get_user')
    @auth_required
    @admin_or_user_id_required
    def get(self, user_id):
        """Get user by ID"""
        user = UserModel.query.get(user_id)
        if not user or not user.is_active:
            return {'message': 'User not found'}, 404

        return user.to_dict(), 200

    @namespace.expect(user_modify_model)
    @namespace.doc('modify_user')
    @auth_required
    @admin_or_user_id_required
    def put(self, user_id):
        """Modify a user by ID"""
        user = UserModel.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        if session.get('is_admin'):
            schema = UserModifyByAdminSchema
        else:
            schema = UserModifySchema

        try:
            data = schema.model_validate(namespace.payload)
        except ValidationError as e:
            return {'Validation error': e.errors()}, 400

        user.set_password(data.password)
        if session.get('is_admin'):
            user.role = data.role or user.role
            user.state = data.state or user.role

        db.session.commit()
        return user.to_dict(), 200

    @namespace.doc('delete_user')
    @auth_required
    @admin_required
    def delete(self, user_id):
        """Delete a user by ID"""
        user = UserModel.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user.state = UserState.deleted
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
