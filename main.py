import requests as req
import os
import sys
from dotenv import load_dotenv

example_html_to_add = "<br>[sound:Leverage.mp3]"
BR = "<br>"
html_to_add = '<br>[sound:'
def printWarning(message):
    message = f'WARNING: {message}'
    print('=' * len(message))
    print(f'{message}')
    print('=' * len(message))

def getAudio(url, filename):
    if(os.path.exists(filename)):
        printWarning(f'File {filename} already exists')
        # exit()
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
            words = [line.replace('\n','') for line in lines]
            # print(words)
        return words

    except FileNotFoundError:
        print(f"ERROR: File' {file_path}' not found")
        exit()
    except Exception as e:
        print(f"ERROR: {e}")
        exit()
# ankideck .txt to array format
def transformFile(file_path):
    try:
        array = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            lines = lines[2:]
            for i in range(0, len(lines), 2):
                word, _ = lines[i].split('\t')
                if not word.__contains__(BR):
                    array.append(word)
        return array

    except FileNotFoundError:
        print(f"ERROR: File' {file_path}' not found")
        exit()
    except Exception as e:
        print(f"ERROR: {e}")
        exit()



def createTxtFile(array, nombre_archivo):
    try:
        with open(nombre_archivo, 'w') as archivo:
            for elemento in array:
                archivo.write(str(elemento) + '\n')
        print(f'Se ha creado el archivo "{nombre_archivo}" con éxito.')
    except Exception as e:
        print(f'Ocurrió un error al crear el archivo: {e}')

def endPosSubstring(cadena, substring):
    indice = cadena.rfind(substring)
    if indice != -1:
        end_pos = indice + len(substring) - 1
        return end_pos
    else:
        return -1
    
def addAudioToAnkiTxt(file_path, words):
    global EXT
    try:
        num = len(words)
        cont = 0
        with open(file_path, 'wr') as file:
            lines = file.readlines()
            array = []
            for line in lines:
                if(not line.__contains__(BR)):
                    while (cont < num and not line.__contains__(words[cont])):
                        cont += 1
                    if (cont < num):
                        pos = endPosSubstring(line, words[cont])
                        subs = line[:pos + 1] + html_to_add + words[cont] + EXT + ']'
                        subs += line[pos + 1: len(line) + 1]
                        array.append(subs)
            cont = 0
        print(array)

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
    array = transformFile("English words.txt")
    # # print(endPosSubstring("hola co ", "co"))
    # exit()
    createTxtFile(array, "words.txt")
    # exit()
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
            # addAudioToAnkiTxt('Exglish words.txt', words)
            
        else:
            word = word.lower()
            getAudio(f'{URL}{word}', f'{DIR}/{word}{EXT}')
    else:
        printWarning(f'No URL specified')
    print('[+] Done')
main()