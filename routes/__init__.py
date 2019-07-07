import uuid
import redis
from functools import wraps

from flask import session, request, abort, redirect, url_for

from models.user import User
from utils import log

# cache = redis.StrictRedis()
csrf_tokens  = {}


def current_user():
    uid = session.get('user_id', '')
    # session = request.cookies.get('session')
    # uid = cache.get(session)
    log('当前用户sesson值: {}, redis值: {}'.format(session, uid))
    if uid is None:
        return redirect(url_for('index.index'))
    else:
        u = User.one(id=int(uid))
        return u


csrf_tokens = {}


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.to_dict().get('token', None)
        log('get taken: {} \n arg: {}'.format(token, request.args.to_dict()))
        # log('taken 对应的值 {}, redis 有这个值？{}'.format(cache.get(token), cache.exists(token)))
        u = current_user()
        if token is None:
            abort(401)
        elif token in csrf_tokens and csrf_tokens[token] == u.id:
        # elif cache.exists(token) == 1 and int(cache.get(token)) == u.id:
            csrf_tokens.pop(token)
            # cache.delete(token)
            return f(*args, **kwargs)

    return wrapper


def reset_pass_csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.to_dict().get('token', None)

        # log('reset_pass_csrf_required get taken: {} \n arg: {} in？:{}'.format(token, request.args.to_dict(), cache.exists(token)))
        if token is None:
            abort(401)
        elif token in csrf_tokens:
        # elif cache.exists(token) == 1:
            kwargs['token_value'] = csrf_tokens[token]
            # kwargs['token_value'] = cache.get(token)
            csrf_tokens.pop(token)
            # cache.delete(token)
            log('是否返回了函数')
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    # cache.set(token, u.id)
    return token


def reset_pass_token(user_name=None):
    token = str(uuid.uuid4())
    csrf_tokens[token] = user_name
    # cache.set(token, user_name)
    return token
