import json
import os

import httplib2
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from oauth2client.service_account import ServiceAccountCredentials

import sys

from lookerstudio.models import PbnPlans, LinksAllDomains
from thcontrol.settings import LOOKER_DB_KEY


def fetch_spreadsheet_data():

    with open('services/looker_studio/lib/looker-400413-4cfe6a2df3ad.json', 'r', encoding='utf-8') as f:
        credentials = ServiceAccountCredentials._from_parsed_json_keyfile(json.load(f), scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])

    http = credentials.authorize(httplib2.Http())

    # Build the service
    service = build('sheets', 'v4', credentials=credentials)

    # Read the spreadsheet data
    spreadsheet_id = '1jUP0o3k7CIELL1Kj-4ARzOgYj3nCb47o21c58AMBguE'
    range_ = '!A1:E'  # Adjust the range to match the columns in the spreadsheet
    response = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_).execute()
    values = response.get('values', [])

    # Extract the column names
    column_names = values[0]

    # Convert the remaining rows to a list of dictionaries
    data = []
    for row in values[1:]:
        row_dict = {column_names[i]: value for i, value in enumerate(row)}
        data.append(row_dict)

    return data


def clear_and_save_data():

    spreadsheet_data = fetch_spreadsheet_data()

    if spreadsheet_data and len(spreadsheet_data) > 0:

        PbnPlans.objects.using(LOOKER_DB_KEY).all().delete()

        for row_dict in spreadsheet_data:
            pbn_plan = PbnPlans(
                client=row_dict.get('client'),
                money_site=row_dict.get('money_site'),
                pbn_sites=int(row_dict.get('pbn_sites')) if row_dict.get('pbn_sites') else 0,
                links=int(row_dict.get('links')) if row_dict.get('links') else 0,
                deadline=row_dict.get('deadline')
            )
            pbn_plan.save(using=LOOKER_DB_KEY)
