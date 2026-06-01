import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# Create blank canvas
canvas = np.zeros((480, 640, 3), dtype=np.uint8)

# Start webcam
cap = cv2.VideoCapture(0)

# Previous coordinates
prev_x, prev_y = 0, 0

# Default drawing color
draw_color = (255, 0, 0)

while True:

    success, frame = cap.read()

    if not success:
        break

    # Flip webcam
    frame = cv2.flip(frame, 1)

    # Convert BGR to RGB
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process hand tracking
    result = hands.process(rgb)

    if result.multi_hand_landmarks:

        for hand_landmarks in result.multi_hand_landmarks:

            # Index fingertip
            index_tip = hand_landmarks.landmark[8]

            # Lower joint
            index_base = hand_landmarks.landmark[6]

            h, w, _ = frame.shape

            x = int(index_tip.x * w)
            y = int(index_tip.y * h)

            # Draw fingertip marker
            cv2.circle(frame, (x, y), 8, (0, 255, 0), -1)

            # Toolbar selection
            if y < 50:

                prev_x, prev_y = 0, 0

                if 0 < x < 100:
                    draw_color = (255, 0, 0)

                elif 100 < x < 200:
                    draw_color = (0, 255, 0)

                elif 200 < x < 300:
                    draw_color = (0, 0, 255)

                elif 300 < x < 400:
                    draw_color = (0, 0, 0)

            # Draw only when finger is up
            elif index_tip.y < index_base.y:

                if prev_x == 0 and prev_y == 0:
                    prev_x, prev_y = x, y

                cv2.line(
                    canvas,
                    (prev_x, prev_y),
                    (x, y),
                    draw_color,
                    5
                )

                prev_x, prev_y = x, y

            else:
                prev_x, prev_y = 0, 0

    else:
        prev_x, prev_y = 0, 0

    # Merge canvas
    frame = cv2.add(frame, canvas)

    # BLUE
    cv2.rectangle(frame, (0, 0), (100, 50), (255, 0, 0), -1)

    # GREEN
    cv2.rectangle(frame, (100, 0), (200, 50), (0, 255, 0), -1)

    # RED
    cv2.rectangle(frame, (200, 0), (300, 50), (0, 0, 255), -1)

    # ERASER
    cv2.rectangle(frame, (300, 0), (400, 50), (0, 0, 0), -1)

    # Toolbar text
    cv2.putText(frame, "BLUE", (15, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.putText(frame, "GREEN", (105, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.putText(frame, "RED", (225, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2)

    cv2.putText(frame, "ERASER", (305, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (255, 255, 255), 2)

    # Show window
    cv2.imshow("AirCanvas", frame)

    key = cv2.waitKey(1)

    # Clear canvas
    if key == ord('c'):
        canvas = np.zeros((480, 640, 3), dtype=np.uint8)

    # Save drawing
    if key == ord('s'):
        cv2.imwrite("drawing.png", canvas)

    # Quit
    if key == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()