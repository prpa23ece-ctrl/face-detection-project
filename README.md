# Human-Following-Robot# Face Detection and Tracking System

A real-time computer vision project that detects human faces, tracks their movement, and calculates the angular position of the detected face.

The system uses OpenCV for face detection and a Kalman Filter for smooth and stable face tracking.

## Project Overview

The Face Detection and Tracking System is designed to detect a human face from a live camera feed and continuously track its position.

A Kalman Filter is used to reduce sudden fluctuations in the detected face coordinates and provide smoother tracking. The system also calculates the horizontal angle of the face relative to the camera frame.

This project can be extended for robotics, autonomous systems, surveillance, and human-following robots.

## Features

* Real-time face detection
* Continuous face tracking
* Kalman Filter-based position estimation
* Smooth tracking of face coordinates
* Horizontal angle calculation
* Live camera processing
* Bounding box visualization
* Face center coordinate tracking

## Face Detection

The system processes frames captured from the camera and detects human faces using OpenCV.

Once a face is detected, a bounding box is drawn around the face and its center coordinates are calculated.

The center position is used as the measurement input for the tracking algorithm.

## Kalman Filter Tracking

A Kalman Filter is implemented to improve tracking stability.

The filter predicts the position of the face and corrects the prediction using the latest detected face coordinates.

This helps reduce:

* Sudden coordinate changes
* Detection noise
* Unstable tracking
* Rapid movement fluctuations

The result is smoother and more reliable face tracking.

## Angle Tracking

The horizontal position of the detected face is converted into an angular value relative to the center of the camera frame.

The angle indicates whether the detected face is positioned:

* Left of the camera
* At the center
* Right of the camera

This feature can be used for servo motor control, robotic head movement, and human-following systems.

## Project Structure

```text
face_detection_project/
│
├── face_detection.py
├── kalman_filter.py
├── angle_tracking.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Technologies Used

* Python
* OpenCV
* NumPy
* Computer Vision
* Kalman Filter
* Real-Time Image Processing

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
```

### 2. Navigate to the project directory

```bash
cd face_detection_project
```

### 3. Install the required dependencies

```bash
pip install -r requirements.txt
```

## How to Run

Run the main Python program:

```bash
python face_detection.py
```

The camera feed will open and the system will start detecting and tracking faces in real time.

Press `q` to stop the program.

## Applications

This project can be used in:

* Human-following robots
* Autonomous assistant robots
* Smart surveillance systems
* Robotic camera tracking
* Human-robot interaction
* Automatic camera positioning systems

## Future Improvements

* Integration with servo motors for physical camera movement
* Deep learning-based face detection
* Multiple face tracking
* Face recognition
* ROS 2 integration
* ESP32-CAM integration
* PID-based motor control
* Improved tracking during temporary face occlusion

## Author

**Priyam Patel**

Electronics and Communication Engineering
Interested in Embedded Systems, Robotics, IoT, and Computer Vision
