import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import cv2
import threading
import os
import csv
import time
from PIL import Image, ImageTk
import numpy as np
import easyocr
import matplotlib.pyplot as plt
import pyttsx3
import pygame

# Paths
CAR_CASCADE_PATH = r"C:\Users\siddartha\OneDrive\Documents\2025\robot\cars.xml"
SOUND_PATH = r"C:\Users\siddartha\OneDrive\Documents\2025\robot\notification-alert-269289.mp3"
SNAPSHOT_DIR = "snapshots"
LOG_DIR = "logs"
CHART_DIR = "chart"

for d in [SNAPSHOT_DIR, LOG_DIR, CHART_DIR]:
    os.makedirs(d, exist_ok=True)

# Settings
PIXELS_PER_METER = 8  # Calibrate based on video
FRAME_INTERVAL = 5  # Frame gap to estimate speed
OVERSPEED_LIMIT = 60  # km/h

reader = easyocr.Reader(['en'])
pygame.mixer.init()

class SpeedDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🚗 Vehicle Speed Detection System")
        self.root.geometry("800x550")
        self.root.configure(bg="#1e1e2f")
        self.video_path = None
        self.stop_flag = False
        self.frame_count = 0
        self.car_cascade = cv2.CascadeClassifier(CAR_CASCADE_PATH)
        self.tracker_data = {}

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", background="#1e88e5", foreground="white",
                             font=("Segoe UI", 12, "bold"), padding=10)
        self.style.map("TButton", background=[("active", "#1565c0")])

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="Vehicle Speed Detection", font=("Segoe UI", 20, "bold"),
                         fg="#ffffff", bg="#1e1e2f")
        title.pack(pady=20)

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack(pady=10)

        ttk.Button(frame, text="🎥 Select Video", command=self.select_video).grid(row=0, column=0, padx=10)
        ttk.Button(frame, text="🚀 Start Detection", command=self.start_detection).grid(row=0, column=1, padx=10)
        ttk.Button(frame, text="🛑 Stop", command=self.stop_detection).grid(row=0, column=2, padx=10)

        self.status_label = tk.Label(self.root, text="No video selected.", font=("Segoe UI", 12),
                                     fg="#dcdcdc", bg="#1e1e2f")
        self.status_label.pack(pady=10)

        self.canvas = tk.Canvas(self.root, width=640, height=360, bg="#2a2a40", highlightthickness=0)
        self.canvas.pack(pady=10)

    def select_video(self):
        path = filedialog.askopenfilename(title="Select video file", filetypes=[("MP4 files", "*.mp4")])
        if path:
            self.video_path = path
            self.status_label.config(text=f"Selected: {os.path.basename(path)}", fg="#90caf9")

    def start_detection(self):
        if not self.video_path:
            messagebox.showwarning("No video", "Please select a video file.")
            return
        self.status_label.config(text="Running detection...", fg="#a5d6a7")
        self.stop_flag = False
        threading.Thread(target=self.process_video, daemon=True).start()

    def stop_detection(self):
        self.stop_flag = True
        self.status_label.config(text="Detection stopped.", fg="#ff7043")

    def process_video(self):
        cap = cv2.VideoCapture(self.video_path)
        self.tracker_data.clear()
        frame_number = 0
        vehicle_speeds = []

        while cap.isOpened() and not self.stop_flag:
            ret, frame = cap.read()
            if not ret:
                break
            frame_number += 1
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cars = self.car_cascade.detectMultiScale(gray, 1.2, 3)

            new_tracker_data = {}
            for (x, y, w, h) in cars:
                center = (x + w // 2, y + h // 2)
                matched_id = None

                for obj_id, data in self.tracker_data.items():
                    old_center = data['center']
                    if np.linalg.norm(np.array(center) - np.array(old_center)) < 50:
                        matched_id = obj_id
                        break

                if matched_id is None:
                    matched_id = str(time.time())

                new_tracker_data[matched_id] = {'center': center, 'frame': frame_number}

                if matched_id in self.tracker_data:
                    prev_data = self.tracker_data[matched_id]
                    distance_px = np.linalg.norm(np.array(center) - np.array(prev_data['center']))
                    time_diff = (frame_number - prev_data['frame']) / cap.get(cv2.CAP_PROP_FPS)
                    speed_mps = (distance_px / PIXELS_PER_METER) / time_diff
                    speed_kmph = speed_mps * 3.6

                    # Draw box
                    color = (0, 255, 0)
                    if speed_kmph > OVERSPEED_LIMIT:
                        color = (0, 0, 255)
                        self.alert_sound()
                        self.save_snapshot(frame, matched_id)
                        self.log_violation(matched_id, speed_kmph)
                        self.detect_plate(frame, x, y, w, h)

                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                    cv2.putText(frame, f"{int(speed_kmph)} km/h", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.6, color, 2)
                    vehicle_speeds.append(speed_kmph)

            self.tracker_data = new_tracker_data

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(rgb).resize((640, 360))
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=imgtk)
            self.canvas.image = imgtk
            time.sleep(0.03)

        cap.release()
        self.generate_chart(vehicle_speeds)
        self.status_label.config(text="Detection completed.", fg="#ffee58")

    def alert_sound(self):
        pygame.mixer.Sound(SOUND_PATH).play()

    def save_snapshot(self, frame, obj_id):
        path = os.path.join(SNAPSHOT_DIR, f"{obj_id}.jpg")
        cv2.imwrite(path, frame)

    def log_violation(self, obj_id, speed):
        log_path = os.path.join(LOG_DIR, "violations.csv")
        with open(log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([obj_id, f"{speed:.2f}", time.strftime("%Y-%m-%d %H:%M:%S")])

    def detect_plate(self, frame, x, y, w, h):
        plate_img = frame[y:y+h, x:x+w]
        result = reader.readtext(plate_img)
        if result:
            print("License Plate Detected:", result[0][-2])

    def generate_chart(self, speeds):
        if not speeds:
            return
        plt.figure(figsize=(10, 5))
        plt.plot(speeds, marker='o')
        plt.axhline(y=OVERSPEED_LIMIT, color='r', linestyle='--', label='Overspeed Limit')
        plt.title("Vehicle Speed Chart")
        plt.xlabel("Detection Count")
        plt.ylabel("Speed (km/h)")
        plt.legend()
        chart_path = os.path.join(CHART_DIR, "speed_chart.png")
        plt.savefig(chart_path)
        print("Speed chart saved to", chart_path)


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeedDetectionApp(root)
    root.mainloop()
