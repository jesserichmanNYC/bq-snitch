import json

import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_slack_alert(wekbook_url, details):


    data = {
        'text': 'Job crossed threshold. Job details: ' + details,
        'username': 'moshe'
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    return str(response.status_code)


def send_email_alert(sender, recipients, details):

    email_body = "Hey, <br> Job crossed the cost limit. Following is the job details:<br><strong>" + details + "</strong>"
    message = Mail(
        from_email=sender,
        to_emails=recipients,
        subject='BigQuery job crossed threshold',
        html_content='<strong>' + email_body + '</strong>')
    try:
        sg = SendGridAPIClient('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')
        sg.send(message)
    except Exception as e:
        print(e.message)
