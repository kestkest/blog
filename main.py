import random
from datetime import datetime

import dependency_injector as di
import config as cfg
import blog.helpers as helpers
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, g, current_app
from blog import routes as blog_blp
from blog import views as blog
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from blog.models import *
from flask_wtf import CsrfProtect
from flask_login import LoginManager
from logging import Logger, INFO, DEBUG, handlers, ERROR, Formatter
from flask_mail import Mail
from flask_sqlalchemy import _EngineDebuggingSignalEvents
from blog.filters import format_date, show_time_passed


class BlogApp:

    def __init__(self):
        self.app = Flask("blog")
        self._logger = None
        self.engine = create_engine(cfg.SQLALCHEMY_DATABASE_URI)
        self.mail_manager = Mail()
        self.login_manager = LoginManager()
        self.csrf = CsrfProtect()
        self.session = scoped_session(sessionmaker(self.engine))

    def run(self, host=None, port=None, debug=None, **kwargs):
        """Runs application"""
        self.app.run()

    @property
    def logger(self):
        if not self._logger:
            log_handlers = []

            # mail handler initialization and configuration
            handlers.SMTPHandler.emit = helpers.emit
            mail_handler = handlers.SMTPHandler(
                mailhost=(cfg.LOG_MAILSERVER, cfg.LOG_MAILPORT),
                fromaddr=cfg.LOG_MAIL_USERNAME,
                toaddrs=cfg.LOG_ADMIN_MAIL,
                subject=cfg.LOG_SUBJECT,
                credentials=(cfg.LOG_MAIL_USERNAME,
                             cfg.LOG_MAIL_PASSWORD),
                secure=True,
                timeout=1
            )
            mail_handler.setLevel(ERROR)
            mail_fmt = Formatter("""
            Message type:       %(levelname)s
            Location:           %(pathname)s:%(lineno)d
            Module:             %(module)s
            Function:           %(funcName)s
            Time:               %(asctime)s
            Message: %(message)s
            """)
            mail_handler.setFormatter(mail_fmt)
            log_handlers.append(mail_handler)

            # file handler init and configuration
            file_handler = handlers.RotatingFileHandler(filename=cfg.FILENAME,
                                            maxBytes=cfg.FILE_SIZE,
                                            backupCount=cfg.MAX_FILE_COUNT)
            file_fmt = Formatter("%(asctime)s %(levelname)s: %(pathname)s:%(lineno)d %(message)s")
            file_handler.setFormatter(file_fmt)
            file_handler.setLevel(INFO)
            log_handlers.append(file_handler)

            self._logger = di.Singleton(Logger, level=INFO,
                                        *[di.Method("addHandler", handler)
                                            for handler in log_handlers],
                                        name="Logger")

            return self._logger

    def configure_app(self):

        # extensions
        # csrf = CsrfProtect()
        # login_manager = LoginManager()
        mail_manager = Mail()

        # flask app configuration
        self.app.config.from_object(cfg)

        # extensions

        # csrf.init_app(self.app)
        self.login_manager.init_app(self.app)
        self.login_manager.login_view = blog.BlogView.login

        @self.login_manager.user_loader
        def load_user(user_id):
            return self.session.query(User).get(int(user_id))

        # blueprint registering
        self.app.register_blueprint(blog_blp.blog, url_prefix="/blog")

        # setting up filters
        self.app.jinja_env.filters['datetime'] = format_date
        self.app.jinja_env.filters['passed'] = show_time_passed
        # debug toolbar
        if cfg.DEBUG_TOOLBAR:
            debug_toolbar = DebugToolbarExtension()
            _EngineDebuggingSignalEvents(self.engine, self.app.name).register()

            debug_toolbar.init_app(self.app)

        # providers
        session = di.Singleton(scoped_session, session_factory=sessionmaker(self.engine))
        mail = di.Singleton(Mail, di.Method("init_app", self.app))
        login = di.Singleton(LoginManager, di.Method("init_app", self.app))

        # blueprints dependencies
        blog_blp.DICatalog.logger.override(self.logger)
        blog_blp.DICatalog.scoped_session.override(session)
        blog_blp.DICatalog.mail_manager.override(mail)

        # errors, before, after
        self.app.teardown_appcontext = blog.teardown_app_context

        # current_app._get_current_object()

    def fill_db(self):
        self.reset_db()
        name_list = ["Joe", "Chandler", "Foebe", "Ross", "Monica", "Rachel",
                     "Jennis", "Richard", "Mike", "Emma", "Ursula", "Sting",
                     "Brad", "Frank", "Lora", "Emily", "Toby", "Paulo", "Ben",
                     "Harper", "Charlie", "Evelin", "Bertha", "Jake", "Melnick"]
        post_list = ["How are you doing?", "Ive lost it in my tracktor", "First, i moist the mother land",
                     "I know!", "Noooooooooooooo", "OMYGAD", "I love my moustache", "Will you marry me, crazy woman?",
                     "My sister will make me a baby \o/", "You don`t have to put on the red light", "life is too short",
                     "Va fan culo", "With the love in my hearth and the song in my mouth", "This is not a support group",
                     "Typical!", "I want more pizza", "My ass is still in a pretty good shape",
                     "Who the hell is Chandler?"]

        print("filling db with test data...")
        print("-" * 20)
        for name in name_list:
            password = User.hash_pw(name.lower())
            user = User(name.lower(), password, (name+'@example.com').lower())
            user.confirmed = True
            user.confirmed_on = datetime.now()
            for i in range(10):
                body = post_list[random.randint(0, len(post_list) - 1)]
                post = Post(body)
                user.posts.append(post)
            self.session.add(user)
            self.session.commit()
        print("data saved")
        print("end...")
        print("-" * 20)

    def reset_db(self):
        print("dropping tables...")
        Base.metadata.drop_all(self.engine)
        print("done dropping")
        print("-" * 20)
        print("creating tables...")
        Base.metadata.create_all(self.engine)
        print("done creating")
        print("-" * 20)

app = BlogApp()
app.configure_app()
# app.fill_db()
app.run()


