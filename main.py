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
    total_cost = total_tera_bytes_billed * tera_bytes_cost
    print("Total cost: " + str(total_cost))
    if total_cost >= alert_threshold:
        print("Job violated cost threshold limit")
        giga_bytes_billed = total_tera_bytes_billed * 1000
        fields_to_retrieve = config['FIELDS_TO_RETRIEVE']
        customize_details = ""
        for field in fields_to_retrieve:
            customize_details = customize_details + field + "=" + str(getattr(job, field, "Non")) + ", "

        print("Job details: \n" + customize_details)
        slack_alert = config['SLACK_ALERT']
        if slack_alert:
            print("Sending slack alert")
            wekbook_url = config['SLACK_WEBHOOK_URL']
            web_api_token = config['SLACK_WEB_API_TOKEN']
            dest_channel = config['SLACK_WEB_API_DESTINATION_CHANNEL']

            alert_channels.send_slack_alert(wekbook_url, web_api_token, dest_channel, job.query, job_id, job.user_email,
                                            total_cost,
                                            giga_bytes_billed, customize_details)

        email_alert = config['EMAIL_ALERT']
        if email_alert:
            print("Sending email alert")
            sender = config['EMAIL_SENDER']
            cc_list = config['EMAIL_CC']
            sendgrid_api_key = config['SENDGRID_API_KEY']
            alert_channels.send_email_alert(sendgrid_api_key, sender, job.query, job_id, job.user_email, cc_list,
                                            total_cost, giga_bytes_billed, customize_details)
    else:
        print("Job didn't violate cost threshold limit")
