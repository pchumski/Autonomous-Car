<div align="center">

# 🚗 Autonomous Car — Engineering Thesis

**NVIDIA Jetson JetRacer · YOLOv5 · OpenCV · Flask · ESP32**

*Autonomous lane-following vehicle with road-sign detection and a custom wireless gamepad*

[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://www.python.org/)
[![PyTorch](https://img.shields.io/badge/PyTorch-1.11+-red?logo=pytorch)](https://pytorch.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green?logo=opencv)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-black?logo=flask)](https://flask.palletsprojects.com/)
[![YOLOv5](https://img.shields.io/badge/YOLOv5-custom-orange)](https://github.com/ultralytics/yolov5)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Platform](#-platform)
- [Features](#-features)
- [Repository Structure](#-repository-structure)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Usage](#-usage)
  - [Lane Detection](#1-lane-detection)
  - [YOLOv5 Sign & Light Detection](#2-yolov5-sign--light-detection)
  - [Gamepad Control](#3-gamepad-control)
  - [Traffic Sign Classification (alternative)](#4-traffic-sign-classification-keras-alternative)
  - [Full Autonomous Mode](#5-full-autonomous-mode-lane--detection-combined)
- [Model Performance](#-model-performance)
- [Links](#-links)

---

## 🧭 Overview

This project is an engineering thesis implementing a miniature autonomous vehicle based on the **NVIDIA Jetson Nano** platform running the **JetRacer** framework. The system combines three independently usable modules:

| Module | Technology | Purpose |
|---|---|---|
| Lane Detection | OpenCV + NumPy | Keep the vehicle on the track |
| Sign & Light Detection | YOLOv5 (custom-trained) | Recognise road signs and traffic lights |
| Remote Control | ESP32 + Pygame + Socket | Drive the car wirelessly |

A **Flask-based web server** streams the camera feed so you can monitor everything from a browser.

---

## 🖥️ Platform

<p align="center">
  <img src="Lane_detection/picture/pojazd.png" alt="NVIDIA Jetson JetRacer" width="500"/>
</p>

| Component | Specification |
|---|---|
| SBC | NVIDIA Jetson Nano |
| Car frame | Waveshare JetRacer |
| Camera | IMX219 CSI (224×224 @ 30 fps) |
| Controller | Custom ESP32-based PCB (designed in KiCad) |

---

## ✅ Features

- **Autonomous lane following** using bird's-eye-view perspective warp and pixel histogram analysis
- **Real-time detection** of stop signs, crosswalks, speed-limit signs, and traffic lights with a custom-trained YOLOv5 model
- **Distance estimation** to detected objects using a focal-length formula
- **Custom wireless gamepad** — ESP32 PCB with Bluetooth/Wi-Fi over a TCP socket, built from scratch (schematic in KiCad)
- **Standard gamepad support** via Pygame (any USB/Bluetooth joystick)
- **Live camera stream** served over Flask at any IP on the local network

---

## 📁 Repository Structure

```
Autonomous-Car/
│
├── Lane_detection/              # Lane-following module
│   ├── code/                    # ← Main production scripts
│   │   ├── autko.py             #   Core lane detection + car steering
│   │   ├── autko_server.py      #   Lane detection + Flask camera server
│   │   ├── Lane_detection.py    #   Standalone lane detection pipeline
│   │   ├── my_detect.py         #   YOLOv5 object detection helper
│   │   └── ...                  #   Utility modules (warping, histogram, …)
│   ├── picture/                 # Reference images & visualisations
│   ├── templates/               # Flask HTML template (index.html)
│   └── video/                   # Demo recordings from the car
│
├── Yolov5/
│   ├── Computer/                # ← Run on a PC / Jetson for detection
│   │   ├── detect_server.py     #   Flask server streaming detections
│   │   ├── class_server.py      #   Detection + lane combined server
│   │   ├── my_detect.py         #   Detection core (calls YOLOv5)
│   │   ├── Lane_detection.py    #   Lane detection for PC webcam
│   │   ├── models/              #   YOLOv5 model architecture files
│   │   ├── utils/               #   YOLOv5 utility functions
│   │   ├── modele_yolo/         #   Pretrained YOLOv5n / YOLOv5s weights
│   │   └── moje_modele/         #   Custom-trained weights (best.pt etc.)
│   │
│   └── Jetracer/                # ← Run directly on the JetRacer
│       ├── Yolo_with_Flask.py   #   Detection + Flask stream on Jetson
│       ├── Yolo_with_Flask_with_distance.py  # + distance estimation
│       ├── Yolo_on_camera.py    #   Detection-only (no server)
│       ├── my_detect.py         #   Detection helper
│       ├── camera.py            #   CSI camera initialisation
│       └── wskazniki_jakosci_modelu/  # Training metrics (PR curves etc.)
│
├── Gamepad/
│   ├── jetracer_teleop.py       # Control with any Pygame joystick
│   └── Own gamepad/             # Custom ESP32 gamepad
│       ├── prosty_serwer.py     #   TCP socket server (runs on Jetson)
│       └── csi_cam.py           #   CSI camera helper
│
├── Traffic_sign_clasification/  # Keras-based sign classifier (alternative)
│   ├── main.py                  #   Run classification from webcam
│   └── label_names.csv          #   43-class GTSRB label mapping
│
├── html page/                   # Project website (Bootstrap)
├── presentation/                # Final presentation (PDF)
├── BSc Thesis/                  # Full thesis document (PDF)
│
└── old/                         # Archived / experimental files
```

---

## ⚙️ Requirements

### Hardware

- NVIDIA Jetson Nano with JetRacer kit  
- IMX219 CSI camera  
- A PC on the same local network (optional, for the computer-side server)  
- Custom ESP32 gamepad **or** any Pygame-compatible USB/Bluetooth joystick  

### Software (JetRacer / Jetson Nano)

> These packages must be installed on the Jetson Nano. JetPack 4.6 or newer is recommended.

```
jetracer          # NVIDIA JetRacer Python library
jetcam            # NVIDIA camera interface library
torch >= 1.11     # PyTorch (JetPack wheel)
torchvision
opencv-python
numpy
flask
```

### Software (PC — optional, for computer-side server)

```
torch >= 1.11
torchvision
opencv-python
numpy
flask
pandas
```

Install on PC:

```bash
pip install torch torchvision opencv-python numpy flask pandas
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/pchumski/Autonomous-Car.git
cd Autonomous-Car
```

### 2. Install JetRacer & JetCam on the Jetson (one-time setup)

Follow the official NVIDIA guide:  
- JetRacer: https://github.com/NVIDIA-AI-IOT/jetracer  
- JetCam: https://github.com/NVIDIA-AI-IOT/jetcam

### 3. Install Python dependencies on the Jetson

```bash
pip3 install flask opencv-python numpy
# PyTorch wheel for Jetson: follow https://forums.developer.nvidia.com/t/pytorch-for-jetson
```

### 4. (Optional) Install dependencies on your PC

```bash
pip install torch torchvision opencv-python numpy flask pandas
```

---

## 🎮 Usage

### 1. Lane Detection

Runs the lane-following algorithm on the JetRacer using the CSI camera.

```bash
cd Lane_detection/code
python autko.py          # Lane detection only — car steers automatically
```

- The script reads the CSI camera via GStreamer, applies perspective warp, computes a pixel histogram to find lane centre, and steers the car accordingly.
- Press **Q** to stop and zero the throttle.

**Visualisation example:**

<p align="center">
  <img src="Lane_detection/picture/warp.png" alt="Bird's-eye warp" width="300"/>
  <img src="Lane_detection/picture/pixelsum1.png" alt="Pixel histogram" width="300"/>
</p>

---

### 2. YOLOv5 Sign & Light Detection

#### Option A — Run on the JetRacer (standalone)

```bash
cd Yolov5/Jetracer
python Yolo_with_Flask.py        # detection + browser stream
python Yolo_with_Flask_with_distance.py   # + distance to sign
```

Then open `http://<jetson-ip>:5000` in your browser to watch the live feed.

#### Option B — Run on a PC (webcam or network camera)

```bash
cd Yolov5/Computer
python detect_server.py          # detection only
python class_server.py           # detection + lane tracking
```

Open `http://localhost:5000`.

**Detected classes:** `stop`, `crosswalk`, `speedlimit`, `trafficlight`

**Choosing a model weight:** place `best.pt` (or any `moje_modele/*.pt`) in the working directory and update the model path in the script:

```python
model = torch.hub.load('yolov5', 'custom', 'moje_modele/best3.pt', source='local')
```

---

### 3. Gamepad Control

#### Option A — Standard joystick (via Pygame)

Works with any USB or Bluetooth gamepad recognised by the OS.

```bash
cd Gamepad
python jetracer_teleop.py
```

- Left stick Y → throttle  
- Left stick X → steering  
- Button 11 → exit  

#### Option B — Custom ESP32 gamepad

The custom controller sends 8-byte packets over a TCP socket.  
Start the server on the Jetson:

```bash
cd Gamepad/Own\ gamepad
python prosty_serwer.py          # listens on port 30003
```

Byte layout of each packet:

| Byte | Value |
|------|-------|
| 0 | Steering (0–255, centre = 127) |
| 1 | Throttle (0–255, centre = 127) |
| 2 | Screenshot trigger (0/1) |
| 3 | Potentiometer value (0–255) |
| 7 | Exit flag (0/1) |

---

### 4. Traffic Sign Classification — Keras (alternative)

An earlier Keras-based multi-class classifier trained on **GTSRB** (43 classes).

> **Requires a pre-trained `traffic_sign.h5` model.** Train one from GTSRB or load a compatible checkpoint.

```bash
cd Traffic_sign_clasification
python main.py
```

- Reads the webcam, resizes each frame to 32×32, and prints the sign class and confidence on screen.
- Press **Q** to quit.

---

### 5. Full Autonomous Mode (lane + detection combined)

Runs lane following and YOLOv5 detection simultaneously with a browser-accessible camera stream.

```bash
cd Lane_detection/code
python autko_server.py           # requires custom gamepad connected on port 30003
```

Or from the computer side:

```bash
cd Yolov5/Computer
python class_server.py
```

---

## 📊 Model Performance

The custom YOLOv5 model was trained on manually collected and annotated images of the track environment.

| Metric | Value |
|--------|-------|
| mAP@0.5 (final epoch) | **~0.95** |
| mAP@0.5:0.95 | ~0.78 |
| Precision | ~0.93 |
| Recall | ~0.94 |

Training curves and label distributions are in `Yolov5/Jetracer/wskazniki_jakosci_modelu/`.

<p align="center">
  <img src="Yolov5/Jetracer/wskazniki_jakosci_modelu/PR_curve.png" alt="PR Curve" width="400"/>
  <img src="Yolov5/Jetracer/wskazniki_jakosci_modelu/results.png" alt="Training results" width="400"/>
</p>

---

## 🔗 Links

| Resource | Link |
|---|---|
| 📄 Engineering Thesis (PDF) | [BSc Thesis/BSc_Thesis.pdf](BSc%20Thesis/BSc_Thesis.pdf) |
| 📊 Final Presentation (PDF) | [presentation/Autonomous_car_new.pdf](presentation/Autonomous_car_new.pdf) |
| 📸 Photos & Videos (Google Drive) | [Drive folder](https://drive.google.com/drive/u/1/folders/1PUePPLqRdV5ynQXc28LMWLCpgILiKmpQ) |
| 🚘 JetRacer library | [NVIDIA-AI-IOT/jetracer](https://github.com/NVIDIA-AI-IOT/jetracer) |
| 🔵 YOLOv5 | [ultralytics/yolov5](https://github.com/ultralytics/yolov5) |

---

<div align="center">

*Engineering Thesis — Wrocław University of Science and Technology*  
**Authors: Paweł Chumski, Jędrzej Szczerbal & Konstanty Odważny**  
*Last updated: 02.2023*

</div>
