import os
from flask import url_for
# builds urls within blueprints in common way

def blp_url(url):
    """
    Function gets blueprint name from the folder name
    :param url:
        usual flask-classy url like AppView:login
    :return:
        returns an endpoint to a view function e.g. "/login"
    """
    blp_name = os.path.dirname(os.path.abspath(__file__)).split("/")[-1]
    endpoint = url_for(".".join([blp_name, url]))
    return endpoint


def emit(self, record):
    """
    Adjusted version of logging.handlers.SMTP
    where SMTP is replaced with SMTP_SSL
    :param self: instance name
    :param record: log message
    """
    import smtplib
    from email.utils import formatdate
    port = self.mailport
    if not port:
        port = smtplib.SMTP_PORT
    smtp = smtplib.SMTP_SSL(self.mailhost, port, timeout=self.timeout)
    msg = self.format(record)
    msg = "From: %s\r\nTo: %s\r\nSubject: %s\r\nDate: %s\r\n\r\n%s" % (
                    self.fromaddr,
                    ",".join(self.toaddrs),
                    self.getSubject(record),
                    formatdate(), msg)
    if self.username:
        if self.secure is not None:
            # print("jere")
            # smtp.ehlo()
            # smtp.starttls()
            # smtp.ehlo()
            smtp.set_debuglevel(1)
        smtp.login(self.username, self.password)
    smtp.sendmail(self.fromaddr, self.toaddrs, msg)
    smtp.quit()