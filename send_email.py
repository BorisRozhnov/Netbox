"""
Send email
"""
import smtplib

host_default = '10.2.1.45'
to_default = 'nextox_readers@domain.ru'
from_default = "netbox@domain.ru"
subject_default = "Message from Netbox"

def send_email(host=host_default, subject=subject_default, TO=to_default, FROM=from_default, data1='test'):

    BODY = "\r\n".join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % subject,
        "",
        data1
    ))

    server = smtplib.SMTP(host)
    server.sendmail(FROM, [TO], BODY)
    server.quit()
send_email(data1='Hello from the python')
