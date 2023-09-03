import requests
import time
import os

from .constants import ocrURl

def processRequest(image_data: bytes):
    params = {'mode' : 'Handwritten'}

    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = os.getenv('CVKey') or ""
    headers['Content-Type'] = 'application/octet-stream'

    retries = 0
    result = None

    while True:
        response = requests.post(ocrURl, json = None, data = image_data, headers = headers, params = params )

        if response.status_code == 429:
            print( "Message: %s" % ( response.json() ) )
            if retries <= 10:
                time.sleep(1) 
                retries += 1
                continue
            else: 
                print( 'Error: failed after retrying!' )
                break
        elif response.status_code == 202:
            result = response.headers['Operation-Location']
        else:
            print( "Error code: %d" % ( response.status_code ) )
            print( "Message: %s" % ( response.json() ) )
        break
        
    return result


def getOCRTextResult(operationLocation):
    headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = os.getenv('CVKey') or ""

    retries = 0
    result = None

    while True:
        response = requests.get(operationLocation, json=None, data=None, headers=headers, params=None)
        if response.status_code == 429:
            print("Message: %s" % (response.json()))
            if retries <= 10:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break
        elif response.status_code == 200:
            result = response.json()
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()))
        break

    return result


def getOcrText(image_data: bytes):
    operationLocation = processRequest(image_data=image_data)

    result = None
    if (operationLocation != None):
        while True:
            time.sleep(1)
            result = getOCRTextResult(operationLocation)
            if result is not None and (result['status'] == 'Succeeded' or result['status'] == 'Failed'):
                break
    
    return result