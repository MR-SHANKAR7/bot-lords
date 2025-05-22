import pytesseract
from PIL import ImageGrab
import time
import pyautogui
import cv2
import numpy as np

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

chat_region = (75, 375, 795, 425)

def preprocess_image(image):
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    cl1 = clahe.apply(gray)
    _, thresh = cv2.threshold(cl1, 140, 255, cv2.THRESH_BINARY)
    return thresh

def read_chat_command():
    time.sleep(2)
    screenshot = ImageGrab.grab(bbox=chat_region)
    preprocessed = preprocess_image(screenshot)
    # لإظهار الصورة للتحقق (يمكنك تعطيلها بعد التأكد)
    # cv2.imshow("Processed", preprocessed)
    # cv2.waitKey(500)
    # cv2.destroyAllWindows()
    command = pytesseract.image_to_string(preprocessed, config='--psm 7')
    print(f"Captured Command: {command}")
    return command.strip()

def send_chat_response(response):
    print(f"Sending: {response}")
    pyautogui.write(response)
    pyautogui.press('enter')

def handle_command(command):
    command = command.lower()
    if "/bal" in command:
        send_chat_response("Food: 10M, Wood: 5M, Gold: 1M")
    elif "/food" in command:
        parts = command.split()
        if len(parts) >= 2 and parts[-1].isdigit():
            amount = int(parts[-1])
            send_chat_response(f"🧺 Sending {amount} food to you!")
        else:
            send_chat_response("⚠️ Usage: /food <amount>")
    elif "/stats" in command:
        send_chat_response("Troops: 450K, Shield: Active (22h left), Resources: All stocked")
    elif "/tasks" in command:
        send_chat_response("✅ Daily tasks completed and resources updated.")
    else:
        send_chat_response("❓ Unknown command. Available: /bal, /food <amount>, /stats, /tasks")

if __name__ == "__main__":
    # رسالة الترحيب عند بداية التشغيل
    welcome_message = """
👋 مرحبًا بك في بوت بنك موارد Lords Mobile!

✨ استخدم الأوامر التالية لإدارة مواردك بسهولة:
- /bal: عرض رصيد الموارد الحالي
- /food <amount>: طلب إرسال كمية من الطعام
- /stats: عرض إحصائيات قواتك ودرعك
- /tasks: إتمام المهام اليومية وزيادة الموارد

💡 استمتع باللعب!
"""
    send_chat_response(welcome_message)

    while True:
        command = read_chat_command()
        if command:
            handle_command(command)
        else:
            print("No command detected.")
        time.sleep(5)
