import glob
from os import read
import cv2
import pytesseract as pyt

pyt.pytesseract.tesseract_cmd = r'C:/Users/chenrick/AppData/Local/Programs/Tesseract-OCR/tesseract'
#path = r'C:/Users/chenrick/Desktop/TOIDEL-2018-01-01-2-T.png'

def read_image(path):
    
    img = cv2.imread(path) 
    (h, w) = img.shape[:2]
    img = cv2.resize(img, (w*2, h*2))
    gry = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #erd = cv2.erode(gry, None, iterations=2)
    #thr = cv2.adaptiveThreshold(erd, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, 5)


    text = pyt.image_to_string(gry)
    words = text.lower().split()
    symbols = ['(',')','-','.',',','/']
    for i in range(len(words)):
        for symbol in symbols:
            words[i] = words[i].replace(symbol,'')
    return words

def get_files(root_dir):
    paths = []
    for filename in glob.glob(root_dir+'**/*T.png', recursive=True):
        paths.append(str(filename))
    return paths

#get_files(r'C:/Users/chenrick/Desktop/Python projects/vs_code/practice/TOIDEL-JAN-18/01/')

def load_data(value,dir):
    all_words = []
    files = get_files(dir)
    data = {}
    paper_ID = []
    for i in range(value):
        all_words.append(read_image(files[i]))
    for i in range(value):
        for word in all_words[i]:
            if word not in data:
                data[word] = 1
                paper_ID.append(files[i])
            else: 
                data[word] += 1
    
    return data, paper_ID


print(load_data(1,r'C:/Users/chenrick/Desktop/Python projects/vs_code/practice/TOIDEL-JAN-18/01/'))

def start_up():
    print('Please enter the path of the folder containing images you would like to parse.')
    flag1 = True
    while flag1:
        folder_path = str(input('Enter path: '))
        try:
            get_files(1,folder_path)
            flag  = False
        except:
            print('Please enter a valid folder path.')
    load_data()

    flag2 = True
    print('Please enter the word/phrase you would like search for (no longer than 15 characters):')
    while flag2:
        search_term = str(input('Enter here: '))
        if len(search_term) > 15:
            print('Search term may not be longer than 15 characters.')
        elif search_term == '':
            print('You did not enter a search term!')
        else:
            flag2 = False
    
    flag3 = True
    print('Please indicate whether you want to allow for close matches.')
    print('\n1)Only show exact matches  2)Allow for close matches')
    var1 = int(input('Enter number here: '))
    