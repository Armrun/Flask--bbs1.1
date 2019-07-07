from time import sleep

from marrow.mailer import Mailer
from sqlalchemy import Column, Unicode, UnicodeText, Integer

from config import admin_mail
import secret
from models.base_model import SQLMixin, db
from models.user import User
# from tasks import send_async, mailer
from routes import reset_pass_token
from utils import log


def configured_mailer():
    config = {
        # 'manager.use': 'futures',
        'transport.debug': True,
        'transport.timeout': 1,
        'transport.use': 'smtp',
        'transport.host': 'smtp.exmail.qq.com',
        'transport.port': 465,
        'transport.tls': 'ssl',
        'transport.username': admin_mail,
        'transport.password': secret.mail_password,
    }
    log('transport.username={},transport.password={}'.format(admin_mail, secret.mail_password))
    log('transport.username={},transport.password={}'.format(1, 2))
    m = Mailer(config)
    m.start()
    return m





def send_mail(subject, author, to, content):
    m = mailer.new(
        subject=subject,
        author=author,
        to=to,
    )
    m.plain = content

    log('e-mail like? {}'.format(m))
    mailer.send(m)
    # sleep(30)

mailer = configured_mailer()
# send_mail('test', 'wudewei@skyroom.cn', '1005851786@qq.com', 'test')
# send_mail(
#             subject='重置密码邮件',
#             author=admin_mail,
#             to='1005851786@qq.com',
#             content='通过这个链接重置你的密码：\n {}'.format('http://localhost:3000/reset/view?token=1'),
#         )


class Messages(SQLMixin, db.Model):
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer, nullable=False)

    @staticmethod
    def send(title: str, content: str, sender_id: int, receiver_id: int):
        form = dict(
            title=title,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id
        )
        Messages.new(form)

        receiver: User = User.one(id=receiver_id)

        log('before send e-mail:to={}'.format(receiver.email))
        send_mail(
            subject=title,
            author=admin_mail,
            to=receiver.email,
            content='站内信通知：\n {}'.format(content),
        )
        import threading
        # form = dict(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        #     plain=form['content'],
        # )
        # t = threading.Thread(target=_send_mail, kwargs=form)
        # t.start()
        #
        # m = mailer.new(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        # )
        # m.plain = form['content']
        #
        # mailer.send(m)
        # sleep(30)
        # send_async.delay(
        #     subject=form['title'],
        #     author=admin_mail,
        #     to=receiver.email,
        #     plain=form['content']
        # )

    @staticmethod
    def send_reset_mail(username):
        user = User.one(username=username)
        if user is not None:
            token = reset_pass_token(username)
            # http: // ip / reset / view?token = token的值。

            # reset_url = 'http://129.204.10.127/reset/view?token={}'.format(token)
            # send_mail(
            #     subject='重置密码邮件',
            #     author=admin_mail,
            #     to=user.email,
            #     content='通过这个链接重置你的密码：\n {}'.format(reset_url),
            # )

            reset_url = 'http://127.0.0.1:3002/reset/view?token={}'.format(token)
            log('reset step 2', reset_url, user.email)
