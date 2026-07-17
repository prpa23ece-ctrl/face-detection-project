# Human-Following Robot: Real-Time Face Detection, Tracking & Control System

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.x-orange.svg)](https://mediapipe.dev/)

A professional, real-time computer vision-based human detection, recognition, and following robotic system. The software integrates **MediaPipe Face Detection**, **dlib face recognition**, **OpenCV tracking APIs (CSRT)**, and a **Kalman Filter** for smooth, jitter-free position and angle estimation. The system sends control commands over USB Serial to an Arduino/ESP32 microcontroller to actuate a differential-drive chassis and a 2-DOF camera gimbal.

---

## 📸 System Overview

```mermaid
graph LR
    %% Hardware Flow
    Cam[USB Camera] --->|Live Feed| Python[Python Tracking Script]
    Python --->|State Smoothing| KF[Kalman Filter]
    KF --->|Offset & Distance Commands| Serial[USB Serial]
    Serial --->|Serial Packets| MCU[Arduino Uno / ESP32]
    MCU --->|PWM Signals| Motors[L298N Motor Driver + Servos]
```

This system reads frames from a camera, identifies registered users, tracks their face coordinates, applies a Kalman Filter to predict state trajectories, and generates continuous movement vectors.

---

## 🛠️ Key Features

* **High-Speed Face Detection**: Uses Google's MediaPipe Face Detection for low-latency, resource-efficient frame analysis compared to traditional HOG/Haar-cascade models.
* **Biometric Face Recognition**: Uses `face_recognition` (built on dlib's ResNet-34) to perform real-time verification against a database of known faces.
* **Smooth Kalman Tracking**: Integrates a linear Kalman Filter that smooths out coordinates, eliminates sudden frame jitter, and handles short term facial occlusions.
* **Hybrid Tracking (CSRT)**: Uses MediaPipe to identify faces, and transitions to a correlation tracker (CSRT) for steady tracking during fast motion.
* **2-DOF Servo Gimbal Support**: Translates pixel offsets into horizontal (Yaw) and vertical (Pitch) angles to tilt/pan the camera towards the user.
* **Chassis Differential Drive Control**: Calculates bounding box surface areas to determine distance thresholds and drive DC motors for forward, backward, or rotational movements.

---

## 📂 Repository Structure

The project layout conforms to professional standards, separating firmware, detailed documentation, and runtime scripts:

```text
face-detection-project/
│
├── docs/                      # Electrical & Mechanical Architecture
│   ├── circuit_diagram.md     # Wiring schematic, pin tables, and power rails
│   ├── robot_design.md        # Physical chassis layers, weights, and servo gimbal
│   └── workflow_flowchart.md  # Process flowcharts, math equations, and control logic
│
├── firmware/                  # Microcontroller Control Code
│   └── robot_firmware/
│       └── robot_firmware.ino # Arduino sketch for DC motors & pan-tilt servos
│
├── known_faces/               # Target database for face recognition matching
│
├── angle_tracking.py          # Estimates camera-face yaw/pitch offsets
├── fast_face_recognition.py   # High-speed MediaPipe + Face Recognition wrapper
├── final.py                   # Main script: CSRT tracker, Kalman filtering, recognition
├── kalman_face_tracking.py    # Standard tracking with Kalman state estimation
├── track_face.py              # Bounding box displacement controller (forward/backward/turn)
├── requirements.txt           # Python environment dependencies
└── README.md                  # Main overview
```

---

## 🔌 Hardware Architecture

The robot utilizes off-the-shelf maker components for a robust, modular build:
* **Microcontroller**: Arduino Uno / Nano or ESP32.
* **Motor Driver**: L298N or L293D dual H-bridge driver.
* **Motors**: 2x 12V DC Gear Motors + 1x Caster Wheel.
* **Camera Gimbal**: 2-DOF Pan-Tilt Bracket equipped with 2x SG90/MG90S servos.
* **Processing Unit**: Raspberry Pi 4 / 5, Jetson Nano, or a laptop mounted on-board.
* **Power Source**: 12V Li-ion Battery (motors) + 5V USB Power Bank (microcontroller & logic).

> [!NOTE]  
> For the complete wiring layout, pin mappings, and power rail configurations, see the [Circuit Diagram Document](file:///docs/circuit_diagram.md). For structural configurations and physical dimensions, see the [Robot Design Document](file:///docs/robot_design.md).

---

## 💻 Software Setup & Installation

### Prerequisite Libraries
Before installing, ensure you have C++ compiler tools installed on your operating system (needed to compile `dlib`).

### 1. Clone the Repository
```bash
git clone https://github.com/prpa23ece-ctrl/face-detection-project.git
cd face-detection-project
```

### 2. Set Up a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Populate Known Faces
Create a folder named `known_faces` in the root directory and add images of authorized individuals named by their identities:
```text
known_faces/
├── John_Doe.jpg
└── Priyam_Patel.png
```

---

## 🚀 Running the System

### Phase 1: Upload Arduino Firmware
1. Open the [robot_firmware.ino](file:///firmware/robot_firmware/robot_firmware.ino) sketch in the Arduino IDE.
2. Select your board (e.g. Arduino Uno) and Port.
3. Upload the code and verify that the baud rate is set to **115200**.

### Phase 2: Execute Tracking Scripts
Run any of the specialized tracking modules depending on your requirements:

* **General Face Tracking & Recognition (Fast)**:
  ```bash
  python fast_face_recognition.py
  ```
* **Angle Calculation & Offset Estimation**:
  ```bash
  python angle_tracking.py
  ```
* **Smooth Tracking (Kalman Filtered)**:
  ```bash
  python kalman_face_tracking.py
  ```
* **Full Integration (CSRT, Face Recognition, Kalman Filter)**:
  ```bash
  python final.py
  ```

---

## 📈 Software Processing Workflow

The core computer vision pipeline runs in a multithreaded loop. For a detailed flowchart and the control loop mathematics (including the Yaw/Pitch trigonometry and Kalman Filter matrix equations), refer to the [Workflow & Tracking Flowchart](file:///docs/workflow_flowchart.md).

---

## 🔮 Future Enhancements

* [ ] **PID Controller Integration**: Replace the threshold-based movement commands with PID loops for smooth deceleration/acceleration.
* [ ] **Depth-Sensing Integration**: Integrate a stereo depth camera (e.g., Intel RealSense) for precise spatial tracking.
* [ ] **ROS 2 Navigation**: Migrate the control framework to ROS 2 (Robot Operating System) for path planning and obstacle avoidance.
* [ ] **Embedded Edge-AI**: Convert the face recognition network to run on specialized edge accelerators (like Edge TPU or Hailo-8).

---

## 👤 Author

**Priyam Patel**  
*Electronics and Communication Engineering*  
*Specializing in Embedded Systems, Robotics, IoT, and Computer Vision*  
* [GitHub Profile](https://github.com/prpa23ece-ctrl)
