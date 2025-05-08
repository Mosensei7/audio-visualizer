import tkinter as tk
import ttkbootstrap as ttk
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import wave
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
import os
import sys
import ctypes

SAMPLERATE = 44100
CHUNK_SIZE = 1024
MOVING_AVERAGE_WINDOW = 5  # How much smoothing to apply

# Helper function to find the icon path when bundled
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller creates temp folder and stores path here
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class AudioVisualizer:
    def __init__(self, root):
        self.root = root
        self.running = False
        self.frames = []

        # UI Elements
        self.toggle_button = ttk.Button(root, text="🎤 Start Recording", bootstyle="success-outline", command=self.toggle_recording)
        self.toggle_button.pack(pady=10)

        self.energy_label = ttk.Label(root, text="Energy: 0.0", font=('Helvetica', 14))
        self.energy_label.pack(pady=5)

        self.peak_label = ttk.Label(root, text="Dominant Frequency: 0 Hz", font=('Helvetica', 14))
        self.peak_label.pack(pady=5)

        # Matplotlib Figure
        self.fig, self.ax = plt.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_xlim(0, 2000)
        self.ax.set_ylim(0, 1)
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Amplitude')

        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas.get_tk_widget().pack()

    def audio_callback(self, indata, frames, time, status):
        if not self.running:
            return
        audio_data = np.squeeze(indata)
        self.frames.append(audio_data.copy())

        # FFT
        fft_result = np.abs(np.fft.rfft(audio_data))
        freqs = np.fft.rfftfreq(len(audio_data), d=1/SAMPLERATE)

        # Smooth the FFT curve using moving average
        smooth_fft = np.convolve(fft_result, np.ones(MOVING_AVERAGE_WINDOW)/MOVING_AVERAGE_WINDOW, mode='same')

        # Update plot
        self.ax.cla()
        self.ax.plot(freqs, smooth_fft)
        self.ax.set_xlim(0, 2000)
        self.ax.set_ylim(0, np.max(smooth_fft) * 1.1 if np.max(smooth_fft) > 0 else 1)
        self.ax.set_xlabel('Frequency (Hz)')
        self.ax.set_ylabel('Amplitude')
        self.canvas.draw()

        # Energy calculation
        energy = np.sum(audio_data**2)
        self.energy_label.config(text=f"Energy: {energy:.4f}")

        # Dominant frequency
        dominant_freq = freqs[np.argmax(fft_result)]
        self.peak_label.config(text=f"Dominant Frequency: {int(dominant_freq)} Hz")

    def toggle_recording(self):
        if not self.running:
            self.start_recording()
        else:
            self.stop_recording()

    def start_recording(self):
        self.running = True
        self.frames = []
        self.stream = sd.InputStream(callback=self.audio_callback, channels=1, samplerate=SAMPLERATE, blocksize=CHUNK_SIZE)
        self.stream.start()
        self.toggle_button.config(text="🛑 Stop Recording", bootstyle="danger-outline")

    def stop_recording(self):
        self.running = False
        self.stream.stop()
        self.stream.close()
        self.save_wav()
        self.toggle_button.config(text="🎤 Start Recording", bootstyle="success-outline")

    def save_wav(self):
        filename = datetime.now().strftime("recording_%Y%m%d_%H%M%S.wav")
        audio_data = np.concatenate(self.frames)
        audio_data = (audio_data * 32767).astype(np.int16)

        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1) 
            wf.setsampwidth(2)
            wf.setframerate(SAMPLERATE)
            wf.writeframes(audio_data.tobytes())
        print(f"Saved recording to {filename}")

def main():
    # Set taskbar icon (important to set before creating root)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(u"mycompany.real_time_audio_visualizer")

    root = ttk.Window(themename="superhero")
    root.title("🎶 Real-Time Audio Visualizer")

    # Set window icon
    icon_path = resource_path("multi_mediaIcon.ico")
    try:
        root.iconbitmap(icon_path)
    except Exception as e:
        print(f"Could not set icon: {e}")

    app = AudioVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main()
