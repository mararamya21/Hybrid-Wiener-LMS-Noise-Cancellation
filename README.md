Design and Implementation of Python-Based Hybrid Adaptive Wiener–LMS Filtering for Intelligent Noise Cancellation in Smart Devices

Overview

This project implements a Hybrid Adaptive Wiener–LMS Filtering technique for intelligent noise cancellation in speech signals. The system records speech, introduces synthetic noise, and applies LMS adaptive filtering followed by Wiener filtering to improve speech quality.

Features

* Voice recording using Python
* Synthetic noise generation
* LMS Adaptive Filter implementation
* Wiener Filter for enhanced noise reduction
* Signal-to-Noise Ratio (SNR) evaluation
* Speech Intelligibility (STOI) calculation
* Approximate PESQ score calculation
* Waveform visualization using Matplotlib

Technologies Used

* Python
* NumPy
* SciPy
* Matplotlib
* SoundDevice
* SoundFile
* PySTOI

Performance

* SNR Improved: -5.36 dB → 12.99 dB
* STOI: Approximately 67.45%
* PESQ Improved: 2.74 → 3.77

Project Structure

Noise-Reduction-System/

* noise_reduction_full.py
* Project_Report.pdf
* Project_Presentation.pptx
* requirements.txt
* README.md

Installation

Install the required libraries:

pip install -r requirements.txt

Applications

* Smart Devices
* Speech Enhancement
* Mobile Communication
* Hearing Assistance Systems
* IoT Devices

Future Scope

* AI and Deep Learning integration
* Real-time implementation
* Embedded systems optimization
* Multi-speaker noise cancellation

