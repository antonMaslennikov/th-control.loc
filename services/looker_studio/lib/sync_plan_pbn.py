from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Load the access token from file
credentials = Credentials.from_authorized_user_file('token.json')

# Check if the access token has expired and refresh if necessary
if credentials.expired and credentials.refresh_token:
    credentials.refresh(Request())

# Build the service
service = build('sheets', 'v4', credentials=credentials)

# Read the spreadsheet data
spreadsheet_id = '1lr605ApFV2Mdoevc4HZxi1qiPmuuLfIV-ccb2wfg4H4'
range_ = '!A1:Z'
response = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
values = response.get('values', [])

# Extract the column names
column_names = values[0]

# Convert the remaining rows to a list of dictionaries
data = []
for row in values[1:]:
    row_dict = {column_names[i]: value for i, value in enumerate(row)}
    data.append(row_dict)

# Print the data
for item in data:
    print(item)
