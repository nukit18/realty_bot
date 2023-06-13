import httplib2
import apiclient
from oauth2client.service_account import ServiceAccountCredentials


async def get_list(nameList):
    CREDENTIALS_FILE = 'creds.json'
    spreadsheet_id = '1CmhA0lj57EhS3ZH4audLppWlvfdxwysabkDYl4gtayQ'

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        CREDENTIALS_FILE,
        ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http())
    service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    name = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{nameList}!A1',
        majorDimension='ROWS'
    ).execute()

    values = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=f'{nameList}!A2:B100',
        majorDimension='ROWS'
    ).execute()
    int_values = []
    for e in values['values']:
        var = []
        for e1 in e:
            var.append(int(e1))
        int_values.append(var)
    return name['values'][0][0], int_values


async def get_MJ():
    return await get_list("Marshal_Zhukov")


async def get_PA():
    return await get_list("Avtomatiki")


async def get_KA():
    return await get_list("Krasnoarmeiskaya")
