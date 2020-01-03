import requests
from datetime import datetime

URL_TOKEN = 'https://auth.veezi.com/token'
API_URL = 'https://api/'

def giftcard_query(start, end):
    '''
    :param start: start barcode range
    :param end:   end barcode range
    :return: query string for vista API
    '''
    url = API_URL + 'giftcardsearch?'
    query_string_parameters = '$count=true&$top=50&$skip=0&$orderby=voucherCode,' \
                              'vouchernumber&barcodeStart={0}&barcodeEnd={1}&stockLocationId=-1'.format(start, end)
    return url + query_string_parameters


def get_token(url):
    username = 'MyUSername'
    password = 'passssPASSSSwOrD'
    login_query = 'grant_type=password&username={0}&password={1}&client_id=vista_id1'.format(username, password)

    request = requests.get(url, data=login_query)

    return request.text

def authorization(token_str):
    token_dic = eval(token_str)
    access_token = token_dic['access_token']
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Authorization': 'bearer ' + access_token,
        'content-type': 'text/plain',
        'Origin': 'https://vgc.eu.veezi.com',
        'Referer': 'https://vgc.eu.veezi.com/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0(Windows NT 10.0; Win64; x64) '
                      'AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 77.0 .3865 .120 Safari / 537.36'
    }

    return headers

def get_giftcards_info(start, end):
    null = None  #  В словаре возвращается обьект null
    query = giftcard_query(start, end)
    headers = authorization(get_token(URL_TOKEN))
    request = requests.get(query, headers=headers)
    return eval(request.text)


def get_card_value(card_num):
    cards = get_giftcards_info(card_num, card_num)
    if cards['count'] > 0:
        for i in cards['items']:
            if i['voucherBarcode'] == card_num:
                value = i['currentValue']
                voucher_num = i['stockIdSet']['voucherNumber']
                voucher_id = i['stockIdSet']['voucherTypeId']
                return value, voucher_id, voucher_num
    return 0, 0, 0


def edit_value(new_value, barcode):
    value, voucher_id, voucher_num = get_card_value(barcode)
    request_payload = {
                          "stockIdSets": [
                            {
                              "voucherTypeId": voucher_id,
                              "voucherNumber": voucher_num,
                              "voucherDuplicateNo": 0
                            }
                          ],
                          "selectedOption": "CurrentPage",
                          "adjustmentType": "NewValue",
                          "comment": "",
                          "isVisible": 'false',
                          "valueLabel": "New Value",
                          "selectedRowCount": 0,
                          "pageRowCount": 1,
                          "allRowCount": 1,
                          "currentSearchViewModel": {
                            "stockType": "GiftCards",
                            "searchMethod": "SearchByBarcode",
                            "searchBy": "Stock",
                            "usageSearch": "T",
                            "stockSearch": "T",
                            "locationId": -1,
                            "barcodeStart": barcode,
                            "barcodeEnd": barcode
                          },
                          "selectionBlurb": "You currently have 0 selected from a total of 1 results.",
                          "selectionOptions": [
                            {
                              "key": "OnlySelected",
                              "displayText": "Only the vouchers I have selected (0)",
                              "isSelected": 'true',
                              "value": "Selected"
                            },
                            {
                              "key": "CurrentPage",
                              "displayText": "All vouchers on the current page view (1)",
                              "isSelected": 'false',
                              "value": "CurrentPage"
                            },
                            {
                              "key": "All",
                              "displayText": "All vouchers in the search results (1)",
                              "isSelected": 'false',
                              "value": "All"
                            }
                          ],
                          "giftCardValueOptions": [
                            {
                              "key": "NewValue",
                              "displayText": "New"
                            },
                            {
                              "key": "DecreaseValue",
                              "displayText": "Decrease"
                            },
                            {
                              "key": "IncreaseValue",
                              "displayText": "Increase"
                            }
                          ],
                          "newValue": new_value,
                          "currentSearchParams": 'null'
                        }
    query = API_URL + 'GiftCardSearchEditValue'
    headers = authorization(get_token(URL_TOKEN))
    headers['content-type'] = 'application/json'
    request = requests.post(query, headers=headers, json=request_payload)

def main(start, end):

    for voucher in range(int(start), int(end) + 1):
        if int(start[0]) == 0:
            value, _, _ = get_card_value('0' + str(voucher))
        else:
            value, _, _ = get_card_value(str(voucher))

        if value:
            whole = value - int(value)
            if whole != 0:
                value = int(value)
                print('Voucher number: ', voucher, 'Set value: ', value, 'Time: ', datetime.now())
                edit_value(value, str(voucher))
            else:
                print('Voucher number: ', voucher, 'Skiped: ', datetime.now())

if __name__ == '__main__':
    start = input('Start of range: ')
    end = input('End of range: ')
    main(start, end)

