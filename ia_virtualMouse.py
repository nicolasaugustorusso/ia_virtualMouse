import cv2
import mediapipe as mp
import pyautogui


#capturar video
cap = cv2.VideoCapture(0)
#Detectar mãos
hand_detector = mp.solutions.hands.Hands()
#Desenhando os pontos
drawing_utils = mp.solutions.drawing_utils
#interligar o frame com as dimensôes da tela
screen_width, screen_height = pyautogui.size()
thumb1_y = 0

#criar loop contínuo
while True:
    #capturar o frame
    _, frame = cap.read()
    #inverter o frame para obter coordenadas corretas
    frame = cv2.flip(frame, 1)
    #obter altura e largura do quadro para posterior multiplicação
    frame_height, frame_width, _ = frame.shape
    #conversor de cor
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    #identificação dos pontos nas mãos
    hands = output.multi_hand_landmarks
    
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(frame, hand)
            #obtendo o id e index de cada ponto da mão
            #conversão dos pontos para números
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)

                #DEDO INDEX
                if id == 12:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    #relação Frame x Screen
                    index_x = screen_width / frame_width * (x) #largura
                    index_y = screen_height / frame_height * (y * 2) #altura
                    #Relacionando código com sistema mouse
                    pyautogui.moveTo(index_x, index_y)
                #DEDO 1 CLIQUE
                if id == 8:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    #relação Frame x Screen
                    thumb1_x = screen_width / frame_width * x
                    thumb1_y = screen_height / frame_height * y
                #DEDO 2 CLIQUE
                if id == 6:
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255))
                    #relação Frame x Screen
                    thumb2_x = screen_width / frame_width * x
                    thumb2_y = screen_height / frame_height * y
                    print('outside', abs(thumb1_y - thumb2_y))

                    if abs(thumb1_y - thumb2_y) < 30: #quanto maior o número maior o raio de aceitação
                        pyautogui.click()
                        pyautogui.sleep(0.2) #Quanto menos segundos, menor o tempo de resposta da ação
                        
    print(hands)
    #mostrar o que foi capturado(img)q
    cv2.imshow('Mouse Virtual', frame)
    key = cv2.waitKey(1)
    #parar código
    if key == ord('q'):
        break
