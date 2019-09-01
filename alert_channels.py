import json

import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_slack_alert(wekbook_url, details):
    try:
        data = {
            'text': 'Job crossed threshold. Job details: ' + details,
            'username': 'moshe'
        }

        requests.post(wekbook_url, data=json.dumps(
            data), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Failed to send slack alert. \n" + e.message)


def send_email_alert(sendgrid_api_key, sender, recipients, details):
    email_body = "Hey, <br> Job crossed the cost limit. Following is the job details:<br><strong>" + details + "</strong>"
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject='BigQuery job crossed threshold',
        html_content='<strong>' + email_body + '</strong>')
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
    except Exception as e:
        print("Failed to send email alert. \n" + e.message)
