import google.auth
import requests
#http://localhost:48927/?state=8VosXbX12VuFGywHD65QakhVUVxc5l&code=4/0AZEOvhXlhogg_0HrCBeWWZAratg-M8aC5ne1-KBb1l0uDSnS8-xM0qet5OzKlsmCtoeKEQ&scope=https://www.googleapis.com/auth/spreadsheets.readonly
# Authorization code received from the callback URL
authorization_code = '4/0AZEOvhXlhogg_0HrCBeWWZAratg-M8aC5ne1-KBb1l0uDSnS8-xM0qet5OzKlsmCtoeKEQ'

# Client credentials (from your credentials file)
client_id = '401780502490-qprulvpo8pd8p4ic1uk06q5emopkunkg.apps.googleusercontent.com'
client_secret = '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'

# Redirect URI used in the authorization request
redirect_uri = 'http://localhost'

# Make the token request
token_url = 'https://accounts.google.com/o/oauth2/token'
token_data = {
    'code': authorization_code,
    'client_id': client_id,
    'client_secret': client_secret,
    'redirect_uri': redirect_uri,
    'grant_type': 'authorization_code'
}
response = requests.post(token_url, data=token_data)

# Parse the token response
token_response = response.json()
print(token_response)
access_token = token_response.get('access_token')
refresh_token = token_response.get('refresh_token')

# Use the access token and refresh token for API requests
if access_token and refresh_token:
    # Use the tokens for API requests
    # ...
    print("Access Token:", access_token)
    print("Refresh Token:", refresh_token)
else:
    print("Token retrieval failed.")


# import requests
# import csv
# #pip install google-auth google-auth-oauthlib google-auth-httplib2
# import os
# import pickle
# import google.auth
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
#
# # Define the scope of the Google Sheets API
# SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
#
# # Path to your credentials JSON file
# CREDENTIALS_FILE = './credentials.json'
#
# # Path to store the token (will be generated after authentication)
# TOKEN_FILE = 'token.json'
#
# # Load or generate the token
# creds = None
# if os.path.exists(TOKEN_FILE):
#     with open(TOKEN_FILE, 'rb') as token:
#         creds = pickle.load(token)
# if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             CREDENTIALS_FILE, SCOPES)
#         creds = flow.run_local_server(port=0)
#     with open(TOKEN_FILE, 'wb') as token:
#         pickle.dump(creds, token)
#
# # Create the Google Sheets API service
# service = build('sheets', 'v4', credentials=creds)
#
# # ID of the spreadsheet you want to read from
# spreadsheet_id = '1lr605ApFV2Mdoevc4HZxi1qiPmuuLfIV-ccb2wfg4H4'
#
# # Range of cells to read (e.g., 'Sheet1!A1:B10')
# range_name = 'Sheet1!A1:B10'
#
# # Make the API request to read data from the spreadsheet
# result = service.spreadsheets().values().get(
#     spreadsheetId=spreadsheet_id, range=range_name).execute()
#
# # Extract the values from the response
# values = result.get('values', [])
#
# # Print the values
# if not values:
#     print('No data found.')
# else:
#     for row in values:
#         print(row)
#
