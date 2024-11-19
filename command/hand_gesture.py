import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

def classify_gesture(landmarks):

    # Tính toán vị trí ngón tay từ landmarks
    finger_tips = [8, 12, 16, 20]  
    thumb_tip = 4  # Đầu ngón cái

    fingers = []
    for tip in finger_tips:
        # Nếu đốt ngón tay đầu tiên cao hơn đốt gốc => ngón tay mở
        fingers.append(landmarks[tip].y < landmarks[tip - 2].y)
    
    # Kiểm tra ngón cái
    thumb_open = landmarks[thumb_tip].x < landmarks[thumb_tip - 2].x

   
    if all(fingers):  # Mở tất cả các ngón
        return "open"
    elif not any(fingers) and not thumb_open:  # Nắm tay
        return "fist"
    return "unknown"

cap = cv2.VideoCapture(0)

print("Listening for gestures...")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1) 
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            
            landmarks = hand_landmarks.landmark
            gesture = classify_gesture(landmarks)
            
            
            if gesture == "open":
                print("Turn on all devices in the current room")
            elif gesture == "fist":
                print("Turn off all devices in the current room")
            else:
                print("Unknown gesture")

    cv2.imshow("Gesture Control", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
