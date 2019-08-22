import json

from google.cloud import bigquery

import alert_channels

with open('config.json', 'r') as f:
    data = f.read()
config = json.loads(data)


def bq_informer(data, context):
    alert_threshold = config['ALERT_THRESHOLD']
    tera_bytes_cost = config['TB_COST']
    client = bigquery.Client()
    resource_name = context.resource.get('name')
    slicing_index = resource_name.rfind('/') + 1
    job_id = resource_name[slicing_index:]
    job = client.get_job(job_id)
    total_tera_bytes_billed = job.total_bytes_billed / 1000000000000
    total_cost = total_tera_bytes_billed / tera_bytes_cost
    if total_cost >= alert_threshold:
        print("Job violated cost threshold limit")
        fields_to_retrieve = config['FIELDS_TO_RETRIEVE']
        details = ""
        for field in fields_to_retrieve:
            details = details + field + "=" + str(getattr(job, field, "Non")) + ", "
        details = details + 'cost=' + str(total_cost)

        print("Job details: \n" + details)
        slack_alert = config['SLACK_ALERT']
        if slack_alert:
            print("Sending slack alert")
            wekbook_url = config['SLACK_WEBHOOK_URL']
            alert_channels.send_slack_alert(wekbook_url, details)

        email_alert = config['EMAIL_ALERT']
        if email_alert:
            print("Sending email alert")
            sender = config['EMAIL_SENDER']
            recipients = config['EMAIL_RECIPIENTS']
            alert_channels.send_email_alert(sender, recipients, job, details)
    else:
        print("Job didn't violate cost threshold limit")
