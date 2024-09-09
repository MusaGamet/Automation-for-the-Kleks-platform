import pyautogui
import time
from PIL import Image
import pytesseract

def find_word_coordinates(image, keyword, lang='rus'):
    if isinstance(image, str):
        image = Image.open(image)
    
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)

    for i in range(len(data['text'])):
        if keyword.lower() == data['text'][i].lower():
            x = data['left'][i]
            y = data['top'][i]
            return x, y
    return None

pyautogui.moveTo(1150,575)
time.sleep(1)

if coordinates:
    print(f"Найдено слово '{keyword}' на экране!")
    print(f"Координаты: ({coordinates[0]}, {coordinates[1]})")
else:
    print(f"Слово '{keyword}' не найдено на экране.")


