import tkinter as tk
from tkinter import ttk
import sounddevice as sd
import soundfile as sf
import threading

class VoiceRecorderApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Voice Recorder")

        self.record_button = ttk.Button(master, text="Record", command=self.toggle_recording)
        self.record_button.pack(pady=10)

        self.save_button = ttk.Button(master, text="Save", command=self.save_recording, state=tk.DISABLED)
        self.save_button.pack(pady=10)

        self.recording = False
        self.frames = []

    def toggle_recording(self):
        if not self.recording:
            self.recording = True
            self.record_button.configure(text="Stop Recording")
            self.save_button.configure(state=tk.DISABLED)

            self.frames = []  # Clear previous frames
            self.recording_thread = threading.Thread(target=self.record_audio)
            self.recording_thread.start()
        else:
            self.recording = False
            self.record_button.configure(text="Record")
            self.save_button.configure(state=tk.NORMAL)

    def record_audio(self):
        duration = 10  # Set the recording duration (in seconds)
        fs = 44100  # Set the sampling frequency

        with sd.InputStream(channels=2, samplerate=fs) as stream:
            self.frames = stream.read(fs * duration, dtype='int16')

    def save_recording(self):
        file_path = "recorded_audio.wav"
        sf.write(file_path, self.frames, 44100)
        print(f"Recording saved as {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceRecorderApp(root)
    root.mainloop()
