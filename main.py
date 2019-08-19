import json

from google.cloud import bigquery

import alert_channels

with open('config.json', 'r') as f:
    data = f.read()
config = json.loads(data)


def bq_informer(data, context):
    print(context.resource.get('name'))
    alert_threshold = config['ALERT_THRESHOLD']
    tera_bytes_cost = config['TB_COST']
    wekbook_url = config['SLACK_WEBHOOK_URL']
    slack_alert = config['SLACK_ALERT']
    fields_to_retrieve = config['FIELDS_TO_RETRIEVE']
    client = bigquery.Client()
    resource_name = context.resource.get('name')
    slicing_index = resource_name.rfind('/') + 1
    job_id = resource_name[slicing_index:]
    job = client.get_job(job_id)
    total_tera_bytes_billed = job.total_bytes_billed / 1000000000000
    total_cost = total_tera_bytes_billed / tera_bytes_cost
    if total_cost >= alert_threshold:
        if slack_alert:
            alert_channels.send_slack_alert(wekbook_url, job, fields_to_retrieve, total_cost)
    else:
        print("alert won't be sent")
