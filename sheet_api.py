from googleapiclient.discovery import build
from google.oauth2 import service_account
from dotenv import load_dotenv
import os

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'keys.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")

service = build('sheets', 'v4', credentials=credentials)

sheet = service.spreadsheets()

result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Topi").execute()
values = result.get('values', [])

# request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range="Topi"
#                                 , valueInputOption="USER_ENTERED", body={"values":})


def request_of_data(list_of_data, count):
    request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=f"Topi!A{count}"
                                , valueInputOption="USER_ENTERED", body={"values":list_of_data}).execute()
    return request