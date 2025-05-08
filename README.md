# 🎶 Real-Time Audio Visualizer

A sleek desktop application built with Python, Tkinter, and Matplotlib to visualize audio input in real time, showing both the energy and dominant frequency of the audio signal while recording and saving the captured sound.

![Screenshot 2025-05-08 112412](https://github.com/user-attachments/assets/e8123f42-10d6-48c7-a2d1-e6d13d12954c)


## 🚀 Features

- 🎤 Real-time microphone audio input  
- 📈 Live frequency domain visualization using FFT  
- ⚡ Audio energy display  
- 🎯 Dominant frequency detection  
- 💾 Save recordings as `.wav` files  
- 🌈 Modern GUI with `ttkbootstrap`  
- 🧊 Optional custom window/taskbar icon (Windows)

---

## 🧠 Technologies Used

- `Python`  
- `tkinter` via `ttkbootstrap` for a modern themed UI  
- `matplotlib` for real-time plotting  
- `sounddevice` for audio streaming  
- `numpy` for signal processing  
- `wave` for saving audio files

---

## 🛠️ Installation

### Prerequisites

Make sure Python 3.7+ is installed. Then install dependencies:

```bash
pip install -r requirements.txt

▶️ How to Run
#bash
python audio_visualizer.py
If you bundled the app using PyInstaller, just run the .exe as usual.


📁 File Structure:
audio_visualizer/
│
├── audio_visualizer.py       
├── multi_mediaIcon.ico       
└── README.md                 


🪄 Packaging as Executable (Optional)
If you want to distribute your app:
pyinstaller --noconfirm --onefile --windowed --icon=multi_mediaIcon.ico audio_visualizer.py
