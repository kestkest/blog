import os

# GENERAL SETTINGS --------------------------------------------------------- #
DEBUG = True
basedir = os.path.dirname(os.path.abspath(__file__))
SECRET_KEY                   # your secret key
SQLALCHEMY_DATABASE_URI      # db URI
# ------------------------------------------------------------------------#
# LOGGER SETTINGS --------------------------------------------------------#

# Mail Logger
LOG_ADMIN_MAIL               # your mail
LOG_SUBJECT                  # error message e.g. "blogapp failure: "
LOG_MAILSERVER               # mail server e.g. "smtp.mail.ru"
LOG_MAILPORT                 # mail port
LOG_MAIL_USERNAME            # full email address e.g. example@gmail.com
LOG_MAIL_PASSWORD            # password

# File Logger

FILE_SIZE                    # size of file in bytes e.g. 1024 * 1024
FILENAME                     # specify a place to store log file
MAX_FILE_COUNT               # number of files within a logging circle
# -------------------------------------------------------------------------#

# DEBUG_TOOLBAR   ---------------------------------------------------------#
DEBUG_TOOLBAR                # True or False
DEBUG_TB_INTERCEPT_REDIRECTS # True or False
# -------------------------------------------------------------------------#

# Flask-Mail SETTINGS -----------------------------------------------------#
MAIL_SERVER                  # mail server e.g. "smtp.mail.ru"
MAIL_PORT                    # mail port
MAIL_USE_TLS                 # True or False
MAIL_USE_SSL                 # True or False
MAIL_DEBUG                   # True or False
MAIL_USERNAME                # full email address e.g. example@gmail.com
MAIL_PASSWORD                # password
MAIL_DEFAULT_SENDER          # sender email e.g. support@atech.com
MAIL_MAX_EMAILS              # max number of emails :)
MAIL_SUPPRESS_SEND           # not sure what it is
MAIL_ASCII_ATTACHMENTS =     # True or False
