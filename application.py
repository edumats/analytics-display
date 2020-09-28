import json
import os

from flask import Flask, render_template
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = os.environ.get('KEY_FILE_LOCATION')
VIEW_ID = os.environ.get('VIEW_ID')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report')
def get_report():
    data = initialize_analyticsreporting().reports().batchGet(
        body={
          'reportRequests': [
          {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
            'metrics': [{'expression': 'ga:sessions'}],
            'dimensions': [{'name': 'ga:country'}]
          }]
        }
    ).execute()
    return json.dumps(data)

def initialize_analyticsreporting():
    # Initializes an Analytics Reporting API V4 service object.
    # An authorized Analytics Reporting API V4 service object.

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics

def print_response(response):
    """Parses and prints the Analytics Reporting API V4 response.

    Args:
    response: An Analytics Reporting API V4 response.
    """
    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
        dimensions = row.get('dimensions', [])
        dateRangeValues = row.get('metrics', [])

        for header, dimension in zip(dimensionHeaders, dimensions):
            print(header + ': ', dimension)

        for i, values in enumerate(dateRangeValues):
            print('Date range:', str(i))
            for metricHeader, value in zip(metricHeaders, values.get('values')):
                print(metricHeader.get('name') + ':', value)
