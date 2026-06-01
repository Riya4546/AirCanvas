import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Create blank canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)

prev_x, prev_y = 0, 0

while True:
    success, frame = cap.read()

    if not success:
        break

    # Flip webcam horizontally
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hand tracking
    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            # Index fingertip
            index_tip = hand_landmarks.landmark[8]

            # Lower joint of index finger
            index_base = hand_landmarks.landmark[6]

            h, w, _ = frame.shape

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw fingertip marker
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

            # Draw only when index finger is up
            if index_tip.y < index_base.y:

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                cv2.line(
                    canvas,
                    (prev_x, prev_y),
                    (x, y),
                    (255, 0, 0),
                    5
                )

                prev_x, prev_y = x, y

            else:
                prev_x, prev_y = 0, 0

    else:
        prev_x, prev_y = 0, 0

    # Merge canvas with webcam
    frame = cv2.add(frame, canvas)

    # Display window
    cv2.imshow("AirCanvas", frame)

    key = cv2.waitKey(1)

    # Clear canvas
    if key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    # Quit program
    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()