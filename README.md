# BigQuery Snitch
Implemented as Google Cloud Function and triggered by BigQuery `query` job to inform the user/channel on Email/Slack along with query details (date/time, syntax, amount of scanned data and cost).

# Configuration

Before deploying the function, adjust the properties in config.json:

 - **ALERT_THRESHOLD** - Any query reaching this value will trigger an alert, e.g., `1` means $1 USD

 - **TB_COST** - The amount Google charges for 1 Terabyte of data processed by a query ($5 per TB according to https://cloud.google.com/bigquery/pricing#on_demand_pricing)

 - **SLACK_ALERT** - Should Slack alerts be enabled (value can be either `true` or `false`)

 - **SLACK_WEBHOOK_URL** - If Slack alerts are enabled, alerts will be sent to this URL. Using the following link will help you generate the URL:
https://api.slack.com/incoming-webhooks

- **SLACK_WEB_API_TOKEN** - If Slack alerts are enabled, alerts will be sent via Web API using this token. Using the following link will help you generate the token:
https://api.slack.com/web

- **SLACK_WEB_API_DESTINATION_CHANNEL** - If Slack alert is enabled and SLACK_WEB_API_TOKEN is defined, alert will be sent via Web API to said channel

 - **EMAIL_ALERT** - Should email alerts be enabled (value can be either `true` or `false`)

 - **SENDGRID_API_KEY** - API key of your SendGrid account. Go to https://app.sendgrid.com -> Settings -> API Keys to retrieve your key. If you don't have a SendGrid account, you can sign up for a free plan [here](https://console.cloud.google.com/marketplace/details/sendgrid-app/sendgrid-email).

 - **EMAIL_SENDER** - The email address you want the alert email to be sent from (e.g., `bq-notifier@domain.com`).

 - **EMAIL_RECIPIENTS** - List of additional emails to receive the alerts. Alerts will always be sent to the user who has executed the query.
  
 - **FIELDS_TO_RETRIEVE** - Define which first level fields you want to retrieve from the job data, in order to send it in an alert message. Optional fields can be found here:  https://googleapis.github.io/google-cloud-python/latest/bigquery/generated/google.cloud.bigquery.job.QueryJob.html#google.cloud.bigquery.job.QueryJob 

# Deploy Function

To deploy the function, execute the following commands. Replace the `project_number` with the project number where you deploy the function.

```
gcloud projects add-iam-policy-binding <project_name> --role=roles/cloudfunctions.serviceAgent --member=serviceAccount:service-<project_number>@gcf-admin-robot.iam.gserviceaccount.com

export PROJECT_ID=YOUR-PROJECT-ID

gcloud config set project $PROJECT_ID

gcloud beta functions deploy bq_informer --trigger-event google.cloud.bigquery.job.complete --trigger-resource projects/${PROJECT_ID}/jobs/{jobId} --runtime python37
```
