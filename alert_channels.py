import json

import requests


def send_slack_alert(wekbook_url, job, fields_to_retrieve, cost):
    details = ""
    for field in fields_to_retrieve:
        details = details + field + "=" + str(getattr(job, field, "Non")) + ", "

    data = {
        'text': 'Job crossed threshold. Job details: ' + details + 'cost=' + str(cost),
        'username': 'moshe'
    }

    response = requests.post(wekbook_url, data=json.dumps(
        data), headers={'Content-Type': 'application/json'})

    return str(response.status_code)
