import requests as req
import os
import sys
from dotenv import load_dotenv
import shutil 

example_html_to_add = "<br>[sound:Leverage.mp3]"
BR = "<br>"
html_to_add = '<br>[sound:'

def printWarning(message):
    message = f'WARNING: {message}'
    print('=' * len(message))
    print(f'{message}')
    print('=' * len(message))

#Get audio from google translate tst
def getAudio(url, filename):
    if(os.path.exists(filename)):
        printWarning(f'File {filename} already exists')
        return
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

# gest extension from the route of a file
def getExtension(filename):
    _, extension = os.path.splitext(filename)
    return extension

#Get only the words from txt file
def getWordsFromFile(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            words = [line.replace('\n','') for line in lines]
            
        return words

    except FileNotFoundError:
        print(f"ERROR: File' {file_path}' not found")
        exit()
    except Exception as e:
        print(f"ERROR: {e}")
        exit()

# Function to transform ankideck.txt to array format, also gets lines from txt file
def transformFile(file_path):
    try:
        array = []
        with open(file_path, 'r') as file:
            lines = file.readlines()
            new_lines = lines[2:]
            for i in range(0, len(new_lines), 2):
                word, _ = new_lines[i].split('\t')
                if not word.__contains__(BR):
                    array.append(word)
        return array, lines

    except FileNotFoundError:
        print(f"ERROR: File' {file_path}' not found")
    except Exception as e:
        print(f"ERROR: {e}")

# Function to create a new file 
def createTxtFile(array, nombre_archivo, salto_linea='\n'):
    try:
        with open(nombre_archivo, 'w') as archivo:
            for elemento in array:
                archivo.write(str(elemento) + salto_linea)
        print(f'Se ha creado el archivo "{nombre_archivo}" con éxito.')
    except Exception as e:
        print(f'Ocurrió un error al crear el archivo: {e}')

# Function to find the substring-word in a string
def findSubstring(string, substring):
    i = 0
    while (i < len(string)):
        j = 0
        while(j < len(substring) and string[i] == substring[j]):
            j += 1
            i += 1
        if(j == len(substring)):
            if(i >= len(string)) or (i < len(string) and string[i] == ' ' or string[i] == '\n' or string[i] == None or string[i] == '\t'):
                return i - 1
        i += 1
    return -1

# def endPosSubstring(cadena, substring):
#     indice = cadena.find(substring)
#     if indice != -1:
#         end_pos = indice + len(substring) - 1
#         return end_pos
#     else:
#         return -1

#Fuction to add string to the anki txt file 
def addAudioToAnkiTxt(lines, words, ext):
    num = len(words)
    cont = 0
    array = []
    for line in lines:
        if(not line.__contains__(BR)):
            while (cont < num and not line.__contains__(words[cont])):
                cont += 1
            if (cont < num):
                pos = findSubstring(line, words[cont])
                subs = line[:pos + 1] + html_to_add + words[cont].lower() + ext + ']'
                subs += line[pos + 1: len(line) + 1]
                array.append(subs)
        else:
            array.append(line)
        cont = 0
    return array
#Function to move the audio files to the anki collection location
def moveToCollection(directory_collection, files):
    print(f'Colection directory %s', directory_collection)
    print(f'Files %s', files)
    error_count = 0
    for file in files:
        try:
            shutil.move(file, directory_collection)
            print(f'File {file} moved' )
        except Exception as e:
            error_count += 1
            print(f'ERROR: {file}')
            print(e)
    if(error_count == 0):
        print(f'[+] Files moved')
    else:
        print(f'[-] Error files {error_count}')

def main():
    load_dotenv('.env')
    URL = os.environ.get('TRANSLATE_URL')
    DIR = os.environ.get('DIR')
    EXT = os.environ.get('EXT')
    ANKI_COLLECTION_DIRECTORY = os.environ.get('ANKI_COLLECTION_DIRECTORY')
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
    array, lines = transformFile("English words.txt")
    createTxtFile(array, "words.txt", '\n')
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
    lines = addAudioToAnkiTxt(lines, words, EXT)
    createTxtFile(lines, "new english words.txt", '')
    files =  os.listdir(DIR)
    os.chdir(DIR)
    # moveToCollection(ANKI_COLLECTION_DIRECTORY,files)
    print('[+] Done')

if __name__ == '__main__':
    main()