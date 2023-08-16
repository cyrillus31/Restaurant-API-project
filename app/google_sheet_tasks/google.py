import os.path

import numpy as np
import pandas as pd
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = '1HhPN8TKMyfb8Yy5dZ5S_reSsGHxike4Tv4P8VSz28o8'
CRIDENTIALS_JSON = './app/google_sheet_tasks/token.json'


def get_data_from_google_sheets():
    credentials = None
    if os.path.exists('./app/google_sheet_tasks/token.json'):
        credentials = Credentials.from_authorized_user_file('./app/google_sheet_tasks/token.json', SCOPES)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('./app/google_sheet_tasks/credentials.json', SCOPES)
            credentials = flow.run_local_server(port=0)
        with open('./app/google_sheet_tasks/token.json', 'w') as token:
            token.write(credentials.to_json())

    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheets = service.spreadsheets()

        result = sheets.values().get(spreadsheetId=SPREADSHEET_ID, range='Sheet1!A1:F18').execute()

        values = result.get('values', [])
        return values

    except HttpError as error:
        print(error)


def convert_to_dataframe(values: list):
    for value in values:
        dif = 6 - len(value)
        value = value + [[]] * dif
    df = pd.DataFrame(values)
    return df


def fill_nan(x):
    if x.empty:
        return np.nan
    else:
        return x


def create_excel_from_google_sheets(path):
    values = get_data_from_google_sheets()
    df = convert_to_dataframe(values)
    df = df.apply(fill_nan)
    df.to_excel(path, index=False)
