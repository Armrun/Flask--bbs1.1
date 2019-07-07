import time

from sqlalchemy import String, Column, Integer, UnicodeText

from models import Model
from models.base_model import db, SQLMixin
from models.user import User
from utils import log


class Reply(SQLMixin, db.Model):
    content = Column(UnicodeText, nullable=False)
    topic_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)

    def user(self):
        u = User.one(id=self.user_id)
        return u

    @classmethod
    def add(self, form, user_id):
        log('new reply''s form:{}'.format(form))
        form['user_id'] = user_id

        r = Reply.new(form)
        return r

    @classmethod
    def topic_id_of_user_in(cls, id):
        all_topic = cls.all(user_id=id)
        id = {}
        #将话题列表列表去重
        for t in all_topic:
            id[t.topic_id] = ''

        return id
