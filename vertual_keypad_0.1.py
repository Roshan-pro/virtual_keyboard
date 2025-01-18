import cv2
import mediapipe as mp
from time import sleep
from pynput.keyboard import Controller

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'],
        ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']]

finaltext = ""
keyboard = Controller()

class Button:
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text

def draw_all(img, button_list):
    for button in button_list:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

button_list = []
for i in range(len(keys)):
    for j, key in enumerate(keys[i]):
        button_list.append(Button([100 * j + 50, 100 * i + 50], key))

while True:
    success, img = cap.read()
    
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    results = hands.process(img_rgb)

    img = draw_all(img, button_list)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(img, landmarks, mp_hands.HAND_CONNECTIONS)
            
            x1, y1 = int(landmarks.landmark[8].x * img.shape[1]), int(landmarks.landmark[8].y * img.shape[0])
            
            for button in button_list:
                x, y = button.pos
                w, h = button.size
                if x < x1 < x + w and y < y1 < y + h:
                    cv2.rectangle(img, button.pos, (x + w, y + h), (174, 0, 174), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
                    
                    x2, y2 = int(landmarks.landmark[4].x * img.shape[1]), int(landmarks.landmark[4].y * img.shape[0])
                    distance = ((x1 - x2)**2 + (y1 - y2)**2)**0.5
                    if distance < 30:
                        keyboard.press(button.text)
                        finaltext += button.text
                        sleep(0.15)
                        break

    cv2.rectangle(img, (50, 350), (700, 450), (175, 0, 175), cv2.FILLED)
    cv2.putText(img, finaltext, (60, 430), cv2.FONT_HERSHEY_PLAIN, 5, (255, 255, 255), 5)

    cv2.imshow("Virtual Keyboard", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
