import requests as req
import os
import sys
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
            print(f'ERROR to download file. State: {response.status_code}')

    except Exception as e:
        print(f'[-] ERROR: {e}')

def getExtension(filename):
    _, extension = os.path.splitext(filename)
    return extension

def getWordsFromFile(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()

            words = [word.strip() for line in lines for word in line.split()]

            return words

    except FileNotFoundError:
        print(f"ERROR: File' {file_path}' not found")
        exit()
    except Exception as e:
        print(f"ERROR: {e}")
        exit()

def main():
    load_dotenv('.env')
    URL = os.environ.get('TRANSLATE_URL')
    DIR = os.environ.get('DIR')
    EXT = os.environ.get('EXT')
    filename = os.environ.get('WORDS_FILE')
    if (URL == None or DIR == None or EXT == None):
        print("ERROR can't import environment variables")
        exit()
    if (len(sys.argv) == 2 and filename == None):
        print("Getting word or filename...")
        filename = sys.argv[1]
        extension = getExtension(filename)
        if (extension == ""):
            word = filename 
            using_file = False
        else:
            print(f"Using file {filename}")
            using_file = True
    elif (filename == None):
        print(f"ERROR: File or word aren't specified")
        print(f'Execute as: python3 main.py <word or filename>')
        exit()
    else:
        using_file = True

    workdir = os.getcwd()
    print(f'Working directory: {workdir}')
    if not os.path.exists(DIR):
        os.makedirs(DIR)
        print(f'Directory created: {workdir}/{DIR}')
    print(f'Working URL: {URL}')
    if (URL != None and URL != ''):
        if (using_file):
            words = getWordsFromFile(f'{workdir}/{filename}')
            for word in words:
                word = word.lower()
                getAudio(f'{URL}{word}', f'{DIR}/{word}{EXT}')
                
        else:
            word = word.lower()
            getAudio(f'{URL}{word}', f'{DIR}/{word}{EXT}')
    else:
        printWarning(f'No URL specified')
    print('[+] Done')
main()