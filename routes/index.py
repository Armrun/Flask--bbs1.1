import uuid

import redis
cache = redis.StrictRedis()

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory,
    make_response,)

from models.message import Messages
from models.reply import Reply
from models.user import User
from models.topic import Topic
from routes import reset_pass_csrf_required, reset_pass_token

from utils import log

main = Blueprint('index', __name__)


# def current_user():
#     # 从 session 中找到 user_id 字段, 找不到就 -1
#     # 然后用 id 找用户
#     # 找不到就返回 None
#     uid = session.get('user_id', -1)
#     u = User.one(id=uid)
#     return u

# def current_user():
#     # uid = session.get('user_id', '')
#     session = request.cookies.get('session')
#     uid = cache.get(session)
#     log('当前用户sesson值: {}, redis值: {}'.format(session, uid))
#     if uid is None:
#         return redirect(url_for('.index'))
#     else:
#         u = User.one(id=uid)
#         return u

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



"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /profile
"""

csrf_tokens = dict()


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/register", methods=['POST'])
def register():
    # form = request.args
    form = request.form
    # 用类函数来判断
    u = User.register(form)
    return redirect(url_for('.index'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    print('login user <{}>'.format(u))
    if u is None:
        # 转到 topic.index 页面
        return redirect(url_for('.index'))
    else:
        # redis 版 session
        # session = str(uuid.uuid4())
        # cache.set(session, u.id)

        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('topic.index'))

        # redis 版 session 增加 set-cookie
        # resp = make_response(redirect(url_for('topic.index')))
        # resp.set_cookie('session', session)
        # return resp


@main.route('/profile')
def profile():
    u = current_user()
    t = Topic.all_tapic_of_user(u.id)
    r = Topic.all_tapic_of_user_in(u.id)
    log('这个用户所有的话题 :{}\n'.format(t), '这个用户参与的话题 :{}'.format(r))
    if u is None:
        return redirect(url_for('.index'))
    else:
        return render_template('profile.html', user=u, topic=t, topic_in=r)


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        t = Topic.all_tapic_of_user(u.id)
        r = Topic.all_tapic_of_user_in(u.id)
        return render_template('profile.html', user=u, topic=t, topic_in=r)


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # http://localhost:2000/images/..%5Capp.py
    # path = os.path.join('images', filename)
    # print('images path', path)
    # return open(path, 'rb').read()
    # if filename in os.listdir('images'):
    #     return
    return send_from_directory('images', filename)


@main.route('/reset/send', methods=['POST'])
def find_password():
    log('reset step 1', request.form.to_dict()['username'])
    username = request.form.to_dict()['username']
    Messages.send_reset_mail(username)
    return redirect(url_for('.index'))


@main.route('/reset/view')
@reset_pass_csrf_required
def find_password_view(**kwargs):
    username = kwargs['token_value']
    token = reset_pass_token('keep')
    log('get the reset username: {}'.format(username))
    return render_template('reset_password.html', token=token, username=username)


@main.route('/reset/update', methods=['POST'])
@reset_pass_csrf_required
def find_password_update(**kwargs):
    form = request.form.to_dict()
    username = form['username']
    new_pass = form['new_pass']
    u = User.one(username=username)
    if u is not None:
        User.update(u.id, password=User.salted_password(new_pass))
        # cls.update(id=id, password=cls.salted_password(new_pass))
    return redirect(url_for('.index'))


def not_found(e):
    return render_template('404.html')
