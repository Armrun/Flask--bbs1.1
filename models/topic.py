import time

from sqlalchemy import String, Integer, Column, Text, UnicodeText, Unicode

from models import Model
from models.base_model import SQLMixin, db
from models.user import User
from models.reply import Reply
from utils import log


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)

    @classmethod
    def add(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    def user(self):
        u = User.one(id=self.user_id)
        return u

    def replies(self):
        ms = Reply.all(topic_id=self.id)
        return ms

    def reply_count(self):
        count = len(self.replies())
        return count

    @classmethod
    def rule_time(cls, arr):
        """
        返回按时间排列的 topic 列表
        """
        arr = sorted(arr, key=lambda t: t.updated_time, reverse=True)
        return arr


    @classmethod
    def all_tapic_of_user(cls, id):
        t = cls.all(user_id=id)
        log('what is time right', cls.rule_time(t))
        # t =  cls.rule_time(t)
        return cls.rule_time(t)

    @classmethod
    def all_tapic_of_user_in(cls, id):
        all_id = Reply.topic_id_of_user_in(id)
        tapices = []
        for key in all_id.keys():
            tapices.append(Topic.one(id=key))
        return cls.rule_time(tapices)

