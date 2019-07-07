from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
)

from routes import *

from models.message import Messages
main = Blueprint('mail', __name__)


@main.route("/add", methods=["POST"])
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    receiver_id = int(form['receiver_id'])
    # 发邮件
    Messages.send(
        title=form['title'],
        content=form['content'],
        sender_id=u.id,
        receiver_id=receiver_id
    )

    return redirect(url_for('.index'))


@main.route('/')
def index():
    u = current_user()
    token = new_csrf_token()

    send = Messages.all(sender_id=u.id)
    received = Messages.all(receiver_id=u.id)

    t = render_template(
        'mail/index.html',
        send=send,
        received=received,
        user=u,
        token=token,
    )
    return t


@main.route('/view/<int:id>')
def view(id):
    message = Messages.one(id=id)
    u = current_user()
    # if u.id == mail.receiver_id or u.id == mail.sender_id:
    log('what is that message {}'.format(message))
    if message is None:
        return redirect(url_for('.index'))
    elif u.id in [message.receiver_id, message.sender_id]:
        return render_template('mail/detail.html', message=message, user=u)

