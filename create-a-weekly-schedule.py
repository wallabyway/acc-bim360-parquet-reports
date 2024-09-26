import json
import requests
import os
from datetime import datetime

def lambda_handler(event, context):
    """
    PURPOSE:
    Call this URL endpoint, to schedule a Data Connector API dump of CSV files on a once off basis.
    Remember to configure the callback to point to the 'handler-callback.py'
    """

    access_token = event.get('access_token')
    accountId = event.get('accountId')
    projectId = event.get('projectId')
    callback_url = os.getenv('CALLBACK_URL')
    
    url = f'https://developer.api.autodesk.com/data-connector/v1/accounts/{accountId}/requests'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    
    effective_from = datetime.utcnow().isoformat() + 'Z'

    payload = {
        "projectId": projectId,
        "serviceGroups": ["admin", "activities"],
        "startDate": None,
        "endDate": None,
        "description": f"Insight Data Extraction for Account: {accountId}, Project: {projectId}.",
        "scheduleInterval": "ONE_TIME",
        "effectiveFrom": effective_from,
        "callbackUrl": callback_url
    }
    
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    
    return {
        'statusCode': response.status_code,
        'body': response.json()
    }