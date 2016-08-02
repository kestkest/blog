from datetime import datetime
import bcrypt
from sqlalchemy import Column, Integer, Boolean, ForeignKey, Unicode, String, DateTime, UnicodeText, Table
from sqlalchemy.orm import relationship, scoped_session, sessionmaker, backref, Query
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin


Base = declarative_base()


association_table = Table("association", Base.metadata,
                          Column("post_id", Integer, ForeignKey("post.id")),
                          Column("tag_id", Integer, ForeignKey("tag.id"))
                          )
post_tag_table = Table('post_tag_table', Base.metadata,
                       Column("post_id", Integer, ForeignKey("post.id")),
                       Column("tag_id", Integer, ForeignKey("tag.id"))
                       )


class Avatar(Base):
    __tablename__ = "avatar"

    id = Column("id", Integer, primary_key=True)
    path = Column("path", String, default=None)
    user_id = Column("user_id", Integer, ForeignKey("user.id"))
    user = relationship("User", backref=backref("avatar", uselist=False))


class Image(Base):
    __tablename__ = "image"

    id = Column("id", Integer, primary_key=True)
    path = Column("path", String)
    user_id = Column("user_id", Integer, ForeignKey("user.id"))
    user = relationship("User", backref=backref("images"))


class User(Base):
    __tablename__ = "user"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", Unicode(20), nullable=False, unique=True)
    password = Column("password", String, nullable=False)
    email = Column("email", Unicode, nullable=False, unique=True)
    reg_date = Column("reg_date", DateTime(timezone=True), default=datetime.now)
    confirmed = Column("confirmed", Boolean, default=False, nullable=False)
    confirmed_on = Column("confirmed_on", DateTime(timezone=True))
    # country = Column("country", Unicode, nullable=True)
    # city = Column("city", Unicode, nullable=True)
    # birth_date = Column("birth_date", DateTime)

    def __init__(self, name, password, email):
        self.name = name
        self.password = password
        self.email = email
        # self.country = country
        # self.city = city
        # self.birth_date = birth_date

    def is_authenticated(self):
        return True

    def is_active(self):
        if self.confirmed:
            return True
        else:
            return False

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def check_password(self, value):
        password = self.password.encode()
        return password == bcrypt.hashpw(value.encode(), password)

    @staticmethod
    def hash_pw(value):
        password = bcrypt.hashpw(value.encode(), bcrypt.gensalt(12)).decode("utf-8")
        return password


class Post(Base):
    __tablename__ = "post"

    id = Column("id", Integer, primary_key=True)
    user_id = Column("user_id", Integer, ForeignKey("user.id"))
    user = relationship("User", backref=backref("posts"))
    body = Column("body", UnicodeText, nullable=False)
    created = Column("created", DateTime(timezone=True), default=datetime.now)
    updated = Column("updated", DateTime(timezone=True), default=datetime.now, onupdate=datetime.now)
    rating = Column("rating", Integer, default=0)
    tag_id = Column(Integer, ForeignKey("tag.id"))

    def __init__(self, body):
        self.body = body


class Tag(Base):
    __tablename__ = "tag"

    id = Column("id", Integer, primary_key=True)
    name = Column("name", Unicode, nullable=True)
    posts = relationship("Post", secondary=association_table,
                         backref=backref("tags", order_by="Post.id"))

    def __init__(self, name):
        self.name = name


class Category(Base):
    __tablename__ = "category"

    id = Column("id", Integer, primary_key=True)
    name = Column('name', Unicode, nullable=False)



