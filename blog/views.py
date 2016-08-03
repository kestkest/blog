import os
from collections import namedtuple

import bcrypt
import json
import logging
import dependency_injector as di
import config as cfg
from sqlalchemy.sql import func
from itsdangerous import URLSafeTimedSerializer, Serializer
from sqlalchemy.orm import scoped_session
from flask_login import current_user, confirm_login, LoginManager, login_user, logout_user, login_required
from flask import redirect, render_template, g, url_for, request, current_app, session, abort, jsonify, Response
from flask_classy import FlaskView, route
from .forms import UserForm, LoginForm
from .helpers import blp_url
from .models import User, Post
from flask_mail import Message, Mail


def teardown_app_context(error):
    if error:
        g.logger.error(error)
    g.scoped_session.remove()


class DICatalog(di.AbstractCatalog):
    scoped_session = di.ExternalDependency(instance_of=scoped_session)
    logger = di.ExternalDependency(instance_of=logging.Logger)
    send = di.Provider()
    mail_manager = di.ExternalDependency(instance_of=Mail)


class BlogView(FlaskView):
    route_base = "/"
    # data = open("questions.json", "r")
    # data = json.load(data)
    # print(data)

    # @route("/serve", methods=["GET"])
    # def serve(self):
    #     resp = Response()
    #     resp.headers['Access-Control-Allow-Origin'] = '*'
    #     data = jsonify(self.data)
    #     print(data)
    #
    #     return data

    def index(self):
        # print(current_user.is_active, current_user.is_active)
        top_rated = g.db_session.query(Post).all()
        form = LoginForm()
        if form.validate_on_submit():
            pass
        title = "Blog homepage"
        posts = g.db_session.query(Post).all()
        login = blp_url("BlogView:login")
        return render_template("index.html", title=title,
                               login=login, form=form,
                               current_user=current_user, posts=posts)

    @route("/<user_name>", methods=["GET"])
    def user_page(self, user_name):
        # print(current_user)
        form = LoginForm()
        login = blp_url("BlogView:login")
        user = g.db_session.query(User).filter(User.name == user_name.lower()).scalar()
        posts = g.db_session.query(Post).filter(Post.user_id == user.id).all()
        pst = sorted(posts, key=lambda post: post.created, reverse=True)
        # print(pst)
        if not user:
            return render_template("404.html")
        return render_template("userpage.html", title=user.name + "`s blog",
                               form=form, posts=pst, user=user)

    @route("/login", methods=["GET", "POST"])
    def login(self):
        title = "Login page for my blog"
        form = LoginForm()
        if form.validate_on_submit():
            print(form.password.data)
            login = form.login.data
            user = g.db_session.query(User).filter_by(name=login).first()
            if user.check_password(form.password.data):
                login_user(user, remember=form["remember_me"])
                next = request.args.get('next')
                return redirect(url_for("blog.BlogView:user_page", user_name=user.name))
            else:
                form.password.errors.append("wrong password")
                return redirect(blp_url("BlogView:login"))
        return render_template("login.html", form=form, title=title)

    @route("/logout", methods=["GET"])
    def logout(self):
        logout_user()
        return redirect(blp_url("BlogView:index"))

    @route("/registration", methods=["GET", "POST"])
    def registration(self):
        form = UserForm()
        if request.method == "GET":
            return render_template("registration.html", form=form)
        if form.validate_on_submit():
            g.current_user = {}
            name = form.name.data
            password = bcrypt.hashpw(form.password.data.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")
            email = form.email.data
            user = User(name, password, email)
            g.db_session.add(user)
            g.db_session.commit()
            serializer = URLSafeTimedSerializer(cfg.SECRET_KEY)
            token = serializer.dumps(user.email, salt="myblogappconfirm")
            msg = Message("Hello, {}".format(name),
                          recipients=[user.email])
            href = url_for("blog.BlogView:confirm_user",
                           _external=True,
                           token=token)
            msg.html = render_template("email_confirm.html", name=name, href=href)

            msg.subject = "Hello, {}. Verify your email please!".format(name)
            g.mail_manager.send(msg)

            return redirect(blp_url("BlogView:index"))
        else:
            return render_template("registration.html", form=form)

    @route("/confirm/<token>", methods=["POST", "GET"])
    def confirm_user(self, token):
        serializer = URLSafeTimedSerializer(cfg.SECRET_KEY)
        try:
            email = serializer.loads(token, salt="myblogappconfirm", max_age=86400)
        except:
            abort(404)
        user = g.db_session.query(User).filter_by(email=email).first()
        user.confirmed = True
        user.confirmed_on = func.now()
        g.db_session.commit()
        print(user.email, user.name)
        login_user(user)
        return redirect(blp_url("BlogView:index"))

    @route("/new_post", methods=["POST"])
    @login_required
    def new_post(self):
        body = request.form.get("data")
        post = Post(body=body)
        user = g.db_session.query(User).filter_by(name=current_user.name).first()
        user.posts.append(post)
        g.db_session.commit()
        response = dict()
        response["user"] = current_user.name
        response["body"] = body
        response["success"] = True
        return jsonify(response)

    @route("/delete_post/<int:post_id>", methods=['POST'])
    def delete_post(self, post_id):
        post = g.db_session.query(Post).get(post_id)
        response = {}
        if not post:
            response['status'] = 'False'
            return jsonify(response)
        g.db.session.delete(post)
        g.db.session.commit()
        response['status'] = 'OK'
        return jsonify(response)

    @route("/edit_post", methods=["PUT"])
    def edit_post(self):
        post_id = request.args.get("id")
        # Should be fine, i guess..
        # Every day is a new day you know :)
        post = g.db.session.query(Post).filter_by(id=post_id).first()
        return None
