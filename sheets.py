import pygsheets # https://github.com/nithinmurali/pygsheets

SHEET_NAME = 'tweeprints'
SHEET_KEY = '1MxRwVLjm2ZAb8MYYUa3M-v29wcRlgRx6WEhMl1I1dB8'
HEADER_ROW = ['Date', 'ID', 'User', 'URL', 'Text']
SERVICE_ACCOUNT = 'tweeprints@tweeprints-243816.iam.gserviceaccount.com'

"""
To make this work, you need to create a Google sheet in your normal account,
 then share it with the SERVICE_ACCOUNT listed above.
The google sheets api I'm using here has credentials associated with this service account, so it must have access.

User: william.langeford@gmail.com
https://console.developers.google.com/iam-admin/serviceaccounts?authuser=2&project=tweeprints-243816
"""

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

def add_rows(rows, sheet_key=SHEET_KEY, sheet_name=SHEET_NAME):

    # authorization
    gc = pygsheets.authorize(service_file='credentials.json')

    # open the google spreadsheet
    # sh = gc.open(sheet_name)
    sh = gc.open_by_key(sheet_key)

    # select the first sheet
    wks = sh[0]

    # Insert rows after 1st row and fill with values
    wks.insert_rows(row=1, number=len(rows), values=rows)

if __name__ == '__main__':
    # init_sheet(SHEET_NAME)
    rows = [[1,2],[3,4]]
    add_rows(rows)
