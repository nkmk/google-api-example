import pandas as pd

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = '<REPLACE_WITH_JSON_FILE>'
VIEW_ID = '<REPLACE_WITH_VIEW_ID>'

credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
analytics = build('analyticsreporting', 'v4', credentials=credentials)

m_list = ['users', 'sessions', 'pageviews', 'bounceRate', 'exitRate', 'avgTimeOnPage',
          'adsenseRevenue', 'adsenseAdsClicks', 'adsenseViewableImpressionPercent']
d_list = ['pagePath', 'date']

metrics = [{'expression': 'ga:' + m} for m in m_list]
dimensions = [{'name': 'ga:' + d} for d in d_list]

start_date = '2018-07-01'
end_date = '2018-07-31'
page_size = 100000
sampling_level = 'LARGE'

body = {
    'reportRequests': [
        {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': start_date, 'endDate': end_date}],
            'metrics': metrics,
            'dimensions': dimensions,
            'pageSize': page_size,
            'samplingLevel': sampling_level
        }
    ]
}

response = analytics.reports().batchGet(body=body).execute()

df = pd.io.json.json_normalize(response['reports'][0]['data']['rows'])

for i, d in enumerate(d_list):
    df[d] = df['dimensions'].apply(lambda x: x[i])

for i, m in enumerate(m_list):
    df[m] = df['metrics'].apply(lambda x: x[0]['values'][i])

df.drop(columns=['dimensions', 'metrics'], inplace=True)

df.to_csv('{}_{}.csv'.format(start_date, end_date), index=False)
