import pytesseract
from PIL import ImageGrab, Image
import pyautogui
import time
from concurrent.futures import ThreadPoolExecutor
from g4f.client import Client
import numpy as np

# Функция поиска координат слова
def find_word_coordinates(image, keyword, lang='rus'):
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    for i in range(len(data['text'])):
        if keyword.lower() == data['text'][i].lower():
            return (data['left'][i], data['top'][i])
    return None

# Функция захвата экрана
def capture_screen(x1, y1, x2, y2):
    return ImageGrab.grab(bbox=(x1, y1, x2, y2))

# Функция распознавания текста
def recognize_text(image):
    np_image = np.array(image)
    return pytesseract.image_to_string(np_image, lang="rus+eng")

# Функция сравнения текстов
def process_text_comparison(prompt, client):
    max_attempts = 3
    for _ in range(max_attempts):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return int(response.choices[0].message.content[:1])
        except Exception:
            continue
    return None

# Основная функция
def main():
    client = Client()  # Создаем клиента вне цикла

    for Y in range(1000):
        print(Y)
        Start_screen = capture_screen(150, 150, 1500, 850)
        EX_screen = recognize_text(Start_screen).splitlines()[:-4]

        if 'Название товара в чеке' in EX_screen:
            EX1 = capture_screen(225, 375, 1300, 425)
            EX2 = capture_screen(225, 490, 1300, 550)
            
            EX1_Text = recognize_text(EX1)

            try:
                EX2_Text = recognize_text(EX2).splitlines()[0]
            except Exception:
                continue
            
            prompt = f"Сравни два текста: {EX1_Text} и {EX2_Text}? Варианты ответов: 1) Подходит 2) Подходит частично 3) Совсем не подходит. Ответ предоставить в виде цифры без лишней информации"
            
            with ThreadPoolExecutor(max_workers=4) as executor:
                results = list(executor.map(lambda _: process_text_comparison(prompt, client), range(10)))
            
            results = [result for result in results if result is not None]

            if results:
                Sr = round(sum(results) / len(results))
            else:
                Sr = "N/A"

            keyword = {1: "Подходит", 2: "частично", 3: "Совсем"}.get(Sr, "частично")

            screenshot = pyautogui.screenshot()
            image = Image.frombytes('RGB', screenshot.size, screenshot.tobytes())
            coordinates = find_word_coordinates(image, keyword)

            if coordinates:
                pyautogui.moveTo(coordinates)
                pyautogui.click()

            keyword = "Совсем"
            coordinates = find_word_coordinates(image, keyword)
            try:
                x = coordinates[0]
            except Exception:
                continue
            y = coordinates[1] + 100
            pyautogui.moveTo(x, y)
            pyautogui.click()
            time.sleep(3)
        else:
            pyautogui.click(1800, 130)
            time.sleep(0.5)
            pyautogui.click(1150, 575)
            time.sleep(0.5)
            pyautogui.click(1870, 140)
            time.sleep(0.5)
            pyautogui.click(380, 940)
            time.sleep(2)

if __name__ == "__main__":
    main()
