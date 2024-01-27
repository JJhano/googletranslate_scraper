import requests as req
import os
from dotenv import load_dotenv

def printWarning(message):
    message = f'WARNING: {message}'
    print('=' * len(message))
    print(f'{message}')
    print('=' * len(message))

def getAudio(url, filename):
    if(os.path.exists(filename)):
        printWarning(f'File {filename} already exists')
        exit()
    try:
        print(f'Request HTTP: {url}')
        response = req.get(url)
        if (response.status_code == 200):
            with open(filename, 'wb') as file:
                file.write(response.content)
            print(f'File downloaded as "{filename}"')
        else:
            print(f'Error to download file. State: {response.status_code}')

    except Exception as e:
        print(f'[-] ERROR: {e}')


def main():
    load_dotenv('.env')
    URL = os.environ.get('TRANSLATE_URL')
    DIR = os.environ.get('DIR')
    print(f'Working path: {os.getcwd()}')
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    print(f'Working URL: {URL}')
    if (URL != None and URL != ''):
        word = 'Hi'
        EXT = '.mp3'
        getAudio(f'{URL}{word}', f'{DIR}/{word}{EXT}')
    else:
        printWarning(f'No URL specified')
    print('[+] Done')
main()