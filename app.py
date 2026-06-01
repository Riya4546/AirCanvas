import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Canvas setup
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Webcam
cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0

while True:
    success, frame = cap.read()
    if not success:
        break

    # Flip frame
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Hand detection
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            # Get index finger tip
            index_tip = hand_landmarks.landmark[8]

            h, w, c = frame.shape
            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw circle on fingertip
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

            # Draw line on canvas
            if prev_x == 0 and prev_y == 0:
                prev_x, prev_y = x, y

            cv2.line(canvas, (prev_x, prev_y), (x, y),
                     (255, 0, 0), 5)

            prev_x, prev_y = x, y

            # Draw hand landmarks
            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

    else:
        prev_x, prev_y = 0, 0

    # Merge canvas and webcam
    frame = cv2.add(frame, canvas)

    cv2.imshow("Air Canvas", frame)

    key = cv2.waitKey(1)

    # Clear canvas
    if key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    # Quit
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()