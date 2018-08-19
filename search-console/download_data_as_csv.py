import pandas as pd

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
KEY_FILE_LOCATION = '<REPLACE_WITH_JSON_FILE>'

credentials = ServiceAccountCredentials.from_json_keyfile_name(KEY_FILE_LOCATION, SCOPES)
webmasters = build('webmasters', 'v3', credentials=credentials)

url = '<REPLACE_WITH_SITE_URL>'
d_list = ['query', 'page']
start_date = '2018-07-01'
end_date = '2018-07-01'
row_limit = 25000

body = {
    'startDate': start_date,
    'endDate': end_date,
    'dimensions': d_list,
    'rowLimit': row_limit
}

response = webmasters.searchanalytics().query(siteUrl=url, body=body).execute()

df = pd.io.json.json_normalize(response['rows'])

for i, d in enumerate(d_list):
    df[d] = df['keys'].apply(lambda x: x[i])

df.drop(columns='keys', inplace=True)

df.to_csv('{}.csv'.format(start_date), index=False)
