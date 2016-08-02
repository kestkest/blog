import os

# GENERAL SETTINGS --------------------------------------------------------- #
DEBUG = True
basedir = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY = "OIdflhfldsh*#^*$(^#03fj43jf4f43jf43dfsh"
SQLALCHEMY_DATABASE_URI = 'postgresql://blogadmin:realpython@localhost/blog'
# ------------------------------------------------------------------------- #
# LOGGER SETTINGS --------------------------------------------------------- #

# Mail Logger
LOG_ADMIN_MAIL = ["rivazx@mail.ru"]
LOG_SUBJECT = "blogapp failure: "
LOG_MAILSERVER = "smtp.mail.ru"
LOG_MAILPORT = "465"
LOG_MAIL_USERNAME = "rivazx@mail.ru"
LOG_MAIL_PASSWORD = "zx"

# File Logger

FILE_SIZE = 1024 * 1024
FILENAME = basedir + ".out"
MAX_FILE_COUNT = 10
# ------------------------------------------------------------------------- #

# DEBUG_TOOLBAR   --------------------------------------------------------- #
DEBUG_TOOLBAR = False
DEBUG_TB_INTERCEPT_REDIRECTS = False

# ------------------------------------------------------------------------- #

# Flask-Mail SETTINGS --------------------------------------------------------- #
MAIL_SERVER = "smtp.mail.ru"
MAIL_PORT = 465
MAIL_USE_TLS = False
MAIL_USE_SSL = True
MAIL_DEBUG = False
MAIL_USERNAME = "rivazx@mail.ru"
MAIL_PASSWORD = "zx"
MAIL_DEFAULT_SENDER = "rivazx@mail.ru"
MAIL_MAX_EMAILS = None
MAIL_SUPPRESS_SEND = None
MAIL_ASCII_ATTACHMENTS = False