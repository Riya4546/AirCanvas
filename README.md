# AirCanvas

AirCanvas is a real-time virtual drawing application built using Python, OpenCV, and MediaPipe.

It allows users to draw in the air using hand gestures captured through a webcam.

---

## Features

- Real-time hand tracking
- Draw using index finger
- Multiple color options
- Eraser tool
- Save drawing as image
- Clear canvas
- One-hand detection for smoother performance
- Simple and interactive UI

---

## Technologies Used

- Python
- OpenCV
- MediaPipe
- NumPy

---

## How It Works

The application uses MediaPipe to detect hand landmarks from the webcam feed.

The position of the index fingertip is tracked and used as a virtual pen to draw on the canvas.

Users can:
- Select colors from the toolbar
- Draw by raising the index finger
- Erase drawings
- Save their artwork

---

## Control 
- c:Clear canvas
- s:Save drawing
- q:Quit application