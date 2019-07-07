import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)
from werkzeug.datastructures import FileStorage

from models.reply import Reply
from models.user import User
from models.topic import Topic
from routes import current_user, new_csrf_token, csrf_required

from utils import log

main = Blueprint('set', __name__)

@main.route('/')
def set_view():
    u = current_user()
    token = new_csrf_token()

    return render_template('set_information.html', user=u, token=token)

@main.route('/update', methods=["POST"])
@csrf_required
def setting():
    u = current_user()
    form = request.form.to_dict()
    log('get the set update {}'.format(form))
    User.update_user_data(u.id, **form)

    return redirect(url_for('set.set_view'))

@main.route('/reset_pass', methods=["POST"])
@csrf_required
def reset():
    u = current_user()
    form = request.form.to_dict()
    log('get the set update {}'.format(form))
    User.reset_password(u.id, **form)

    return redirect(url_for('set.set_view'))

@main.route('/chang_img', methods=["POST"])
@csrf_required
def chang_img():
    u = current_user()
    file = request.files['avatar']
    User.change_img(u.id, file)

    return redirect(url_for('set.set_view'))