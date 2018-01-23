import smtplib
import pandas as pd
import numpy as np

fromaddr = ''
toaddr = ''

username = ''
password = ''

FROM = username
TO = toaddr if type(toaddr) is list else [toaddr]
SUBJECT = 'Group Assignment Test'
TEXT = 'Hi,\nThis is to inform you that the test email worked!\n\nThanks!\nCS267 GSIs'

#Prepare message
msg = """From: %s\nTo: %s\nSubject: %s\n\n%s""" % (FROM, ", ".join(TO), SUBJECT, TEXT)

try:
    server_ssl = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server_ssl.ehlo()
    server_ssl.login(username, password)
    server_ssl.sendmail(FROM, TO, msg)
    server_ssl.close()
    print('successfully sent the mail')
except:
    print('SSL send failed. Trying without SSL')
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(username, password)
        server.sendmail(FROM, TO, msg)
        server.close()
        print('successfully sent the mail')
    except:
        print('failed to send mail')
