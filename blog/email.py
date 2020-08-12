from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings

def mail_message(cleaned_form_data, post, post_url):
    sender_email = settings.SENDGRID_MAIL_USERNAME
    SENDGRID_API_KEY = settings.SENDGRID_API_KEY

    subject = '{} ({}) recommends you reading "{}"'.format(cleaned_form_data['name'], cleaned_form_data['email'], post.title)
    message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cleaned_form_data['name'], cleaned_form_data['comments'])
    message = Mail(
        from_email=sender_email,
        to_emails=cleaned_form_data['to'],
        subject=subject,
        html_content=message
    )
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    return response