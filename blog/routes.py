import dependency_injector as di
from blog import views
from flask import Blueprint, g
from flask_mail import Mail

# blueprint creation
blog = Blueprint("blog", __name__, template_folder="templates", static_folder="static", url_prefix="/blog")


class DICatalog(di.AbstractCatalog):
    scoped_session = di.Provider()
    logger = di.Provider()
    send = di.Provider()
    mail_manager = di.Provider()


def before_request():
    g.scoped_session = DICatalog.scoped_session()
    g.db_session = g.scoped_session()
    g.logger = DICatalog.logger()
    g.mail_manager = DICatalog.mail_manager()


blog.before_request(before_request)


# dependencies
# views.DICatalog.login_manager.override(DICatalog.login_manager)
# views.DICatalog.mail_manager.override(DICatalog.mail_manager)

# blueprint views
views.BlogView.register(blog, route_base="/", route_prefix="/")
