import sendgrid
from sendgrid.helpers.mail import *
from django.core.mail import send_mail
import os 
import config

# SENDGRID_API_KEY='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'

sg = sendgrid.SendGridAPIClient(config.SENDGRID_API_KEY)
from_email = Email("singla.uday2000@gmail.com")
to_email = ["singla.uday2000@gmail.com",]
subject = "Subject here"
content = Content("text/plain", "Check out this new post")
mail = Mail(from_email, to_email, subject, content)
response = sg.send(mail)
print(response.status_code)
print(response.body)
print(response.headers)
print(to_email)