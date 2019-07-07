import os
import uuid

from sqlalchemy import Column, String, Unicode

import config
from models import Model
from models.base_model import SQLMixin, db
from utils import log


class User(SQLMixin, db.Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """

    username = Column(String(50), nullable=False)
    password = Column(String(256), nullable=False)
    signature = Column(Unicode(50), nullable=False, default='这家伙很懒，什么个性签名都没有留下。')
    image = Column(String(100), nullable=False, default='/static/img/default.gif')
    email = Column(String(50), nullable=False, default=config.test_mail)

    @classmethod
    def salted_password(cls, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        print('sha256', len(hash2))
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form['username']
        password = form['password']
        if len(name) > 2 and User.one(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(password)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        user = User.one(username=form['username'])
        print('validate_login <{}> who <{}> pass_eql <{}>'.format(
            form,
            user,
            user.password == User.salted_password(form['password'])
        ))
        if user is not None and user.password == User.salted_password(form['password']):
            return user
        else:
            return None

    @classmethod
    def update_user_data(cls, id, **kwargs):
        log('update_user_data form: {}'.format(kwargs))

        n = kwargs['name']
        s = kwargs['signature']
        e = kwargs['email']
        if n != '':
            if n.find(' ') == -1:
                cls.update(id=id, username=n)
        if s != '':
            cls.update(id=id, signature=s)
        if e != '':
            cls.update(id=id, email=e)

    @classmethod
    def reset_password(cls, id, **kwargs):
        log('reset password form: {}'.format(kwargs))
        username = User.one(id=id).username
        old_pass = kwargs['old_pass']
        new_pass = kwargs['new_pass']

        form = dict(
            username=username,
            password=old_pass,
        )
        if cls.validate_login(form) is not None:
            cls.update(id=id, password=cls.salted_password(new_pass))

    @classmethod
    def change_img(cls, id, file):
        filename = str(uuid.uuid4())
        # flask 框架默认做好了 static 文件的静态资源动态路由，其他文件夹的文件路由需要自己加
        path = os.path.join('images', filename)
        file.save(path)

        User.update(id, image='/images/{}'.format(filename))
