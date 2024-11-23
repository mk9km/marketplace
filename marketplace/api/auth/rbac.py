from flask import session
from functools import wraps

def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('user_id'):
            return {'message': 'Unauthorized'}, 401
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_admin'):
            return {'message': 'Forbidden: Insufficient permissions'}, 403
        return func(*args, **kwargs)
    return wrapper

def partner_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_partner'):
            return {'message': 'Forbidden: Insufficient permissions'}, 403
        return func(*args, **kwargs)
    return wrapper

def user_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get('is_user'):
            return {'message': 'Forbidden: Insufficient permissions'}, 403
        return func(*args, **kwargs)
    return wrapper

def user_id_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id') or args[0]
        if session.get('user_id') == user_id:
            return {'message': 'Forbidden: Insufficient permissions'}, 403
        return func(*args, **kwargs)
    return wrapper

def admin_or_user_id_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id') or args[0]
        if session.get('is_admin') or session.get('user_id') == user_id:
            return func(*args, **kwargs)
        return {'message': 'Forbidden: Insufficient permissions'}, 403
    return wrapper
