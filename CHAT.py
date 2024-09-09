import pytesseract
from PIL import ImageGrab, Image
import pyautogui
import time
from concurrent.futures import ThreadPoolExecutor
from g4f.client import Client

# Захват области экрана по заданным координатам
def capture_screen(x1, y1, x2, y2):
    return ImageGrab.grab(bbox=(x1, y1, x2, y2))

def recognize_text(image):
    text = pytesseract.image_to_string(image, lang="rus+eng")  
    return text

def click_on_pixel(x, y):
    pyautogui.moveTo(x, y)
    pyautogui.click()

def process_text_comparison(prompt):
    max_attempts = 3  # Количество попыток
    for attempt in range(max_attempts):
        try:
            client = Client()
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            return int(response.choices[0].message.content[:1])
        except Exception as e:
            print(f"Attempt {attempt+1}/{max_attempts} failed: {e}")

    return None

def main():
    EX1 = capture_screen(225, 375, 1300, 425)
    EX2 = capture_screen(225, 490, 1300, 550)
    
    EX1_Text = recognize_text(EX1)
    EX2_Text = recognize_text(EX2).splitlines()[0]

    print(EX1_Text)
    print(EX2_Text)

    prompt = f"Сравни два текста: {EX1_Text} и {EX2_Text}? Варианты ответов: 1) Подходит 2) Подходит частично 3) Совсем не подходит. Ответ предоставить в виде цифры без лишней информации"
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = list(executor.map(lambda _: process_text_comparison(prompt), range(10)))
    
    results = [result for result in results if result is not None]
    
    S = sum(results)
    k = len(results)
    Sr = round(S / k) if k != 0 else "N/A"
    print(S, k, Sr)

    if Sr == 1:
        x, y = 315, 550  
    elif Sr == 2:
        x, y = 315, 600  
    elif Sr == 3:
        x, y = 315, 650 

    click_on_pixel(x, y)
    time.sleep(0.5)
    click_on_pixel(450, 750)
    time.sleep(3)

if __name__ == "__main__":
    main()
