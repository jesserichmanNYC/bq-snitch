# BigQuery Job Informer
Cloud Function triggered by BigQuery job and informing the user who initiated the job with query details (date/time, syntax, amount of scanned data and cost).

# Configuration

Setup properties in config.json:

ALERT_THRESHOLD - Any query reaching this value will trigger an alert

TB_COST - The amount google charges for 1 terabyte of data processed in a query (shouldn't be changed unless google announce on changes in rates)

SLACK_ALERT - Should slack alerts be enabled

SLACK_WEBHOOK_URL - If slack alerts enabled, alerts will be sent to this URL. Using the following link will help you generate the URL:
https://api.slack.com/incoming-webhooks

EMAIL_ALERT - Should email alerts be enabled

SENDGRID_API_KEY - API key of your Sendgrid account. Go to https://app.sendgrid.com -> Settings -> API Keys

EMAIL_SENDER - The email address you want the alert email to be sent from

EMAIL_RECIPIENTS - List of emails you want to receive the alerts
  
FIELDS_TO_RETRIEVE - Define which first level fields you want to retrieve from the job data, in order to send it in an alert message

# Deploy Function

export PROJECT_ID=YOUR-PROJECT-ID

gcloud config set project $PROJECT_ID

gcloud beta functions deploy bq_informer --trigger-event google.cloud.bigquery.job.complete --trigger-resource projects/${PROJECT_ID}/jobs/{jobId} --runtime python37