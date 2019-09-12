import json

import requests
import slack
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import *


def send_slack_alert(wekbook_url, web_api_token, dest_channel, query, job_id, user_email, cost, gigabytes_billed,
                     customize_details):
    try:
        message_blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "The following query has processed large amount of data:"
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Query Syntax ```" + str(query) + "```"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "Job ID *" + str(job_id) + "*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "Query User *" + str(user_email) + "*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "Gigabytes Billed *" + str(truncate(gigabytes_billed, 2)) + "*"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "Query Cost *$" + str(truncate(cost, 2)) + "*"
                    }
                ]
            }
        ]

        if wekbook_url:
            send_slack_alert_webhook(wekbook_url, message_blocks)

        if web_api_token:
            send_slack_alert_web_api(web_api_token, dest_channel, message_blocks)
    except Exception as e:
        print("Failed to send slack alert. \n" + e.message)


def send_slack_alert_webhook(wekbook_url, blocks):
    print("sending slack webhook alert")
    try:
        data = {"blocks": blocks}

        requests.post(wekbook_url, data=json.dumps(
            data), headers={'Content-Type': 'application/json'})
    except Exception as e:
        print("Failed to send slack alert. \n" + e.message)


def send_slack_alert_web_api(web_api_token, dest_channel, message_blocks):
    print("sending slack web api alert")
    client = slack.WebClient(web_api_token)
    try:

        client.chat_postMessage(channel=dest_channel, blocks=message_blocks)

    except Exception as e:
        print("Failed to send slack alert. \n" + e.message)


def send_email_alert(sendgrid_api_key, sender, user_email, cc_list, details):
    email_body = "Hey, <br> Job crossed the cost limit. Following is the job details:<br><strong>" + details + "</strong>"
    message = Mail(
        from_email=sender,
        to_emails=user_email,
        subject='BigQuery job crossed threshold',
        html_content='<strong>' + email_body + '</strong>')
    for cc_email in cc_list:
        message.personalizations[0].add_cc(Email(cc_email))
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        sg.send(message)
    except Exception as e:
        print("Failed to send email alert. \n" + e.message)


def truncate(f, n):
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d + '0' * n)[:n]])
