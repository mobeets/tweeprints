import os
import pygsheets # https://github.com/nithinmurali/pygsheets

try:
    from dotenv import load_dotenv
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(dotenv_path)
except:
    pass

SHEET_KEY = '1MxRwVLjm2ZAb8MYYUa3M-v29wcRlgRx6WEhMl1I1dB8'
SERVICE_ACCOUNT = 'tweeprints@tweeprints-243816.iam.gserviceaccount.com'
GOOGLE_APPLICATION_CREDENTIALS = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
open('tmp_credentials.json', 'w').write(GOOGLE_APPLICATION_CREDENTIALS)

"""
To make this work, you need to create a Google sheet in your normal account,
 then share it with the SERVICE_ACCOUNT listed above.
The google sheets api I'm using here has credentials associated with this service account, so it must have access.

Also, need to run:
    $ heroku config:set GOOGLE_APPLICATION_CREDENTIALS="$(< credentials.json)"
This passes the contents of the credentials.json file to heroku

User: william.langeford@gmail.com
https://console.developers.google.com/iam-admin/serviceaccounts?authuser=2&project=tweeprints-243816
"""

# SHEET_NAME = 'tweeprints'
# HEADER_ROW = ['Date', 'ID', 'User', 'URL', 'Text']
# def init_sheet(sheet_name=SHEET_NAME, header_row=HEADER_ROW):
#     """
#     create sheet, share it, and write header row
#     """
#     gc = pygsheets.authorize(service_file='credentials.json')
#     gc.create(sheet_name)
#     sh = gc.open(sheet_name)
#     # sh.share("mobeets@gmail.com")
#     wks = sh[0]
#     wks.clear()
#     wks.insert_rows(row=0, number=1, values=header_row)

def get_rows_in_sheet(sheet_key=SHEET_KEY):
    """
    return non-empty rows
    """
    # authorization
    gc = pygsheets.authorize(service_file='tmp_credentials.json')
    # gc = pygsheets.authorize(service_account_env_var='GOOGLE_APPLICATION_CREDENTIALS')

    # open the google spreadsheet
    sh = gc.open_by_key(sheet_key)

    # select the first sheet
    wks = sh[0]

    # get non-empty rows
    rows = wks.get_all_values(returnas='matrix')
    return [row for row in rows if ''.join(row)]

def add_rows_to_sheets(rows, sheet_key=SHEET_KEY):
    # authorization
    gc = pygsheets.authorize(service_file='tmp_credentials.json')
    # gc = pygsheets.authorize(service_account_env_var='GOOGLE_APPLICATION_CREDENTIALS')

    # open the google spreadsheet
    sh = gc.open_by_key(sheet_key)

    # select the first sheet
    wks = sh[0]

    # Insert rows after 1st row and fill with values
    wks.insert_rows(row=1, number=len(rows), values=rows)

if __name__ == '__main__':
    # init_sheet(SHEET_NAME)
    rows = [[1,2],[3,4]]
    add_rows_to_sheets(rows)
