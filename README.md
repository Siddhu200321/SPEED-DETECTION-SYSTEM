# SPEED-DETECTION-SYSTEM
Vehical Speed Detection 
# 🚗 Vehicle Speed Detection System (Python + OpenCV + Tkinter)

This project is a real-time **Vehicle Speed Detection System** built using **Python**, **OpenCV**, **EasyOCR**, and **Tkinter**. It detects vehicles from a video file, estimates their real-world speed using calibrated pixel-to-meter ratios, and flags over-speeding vehicles with audio alerts and snapshots. License plate recognition is done using EasyOCR, and violations are logged with timestamps.

---

## 🛠 Features

- 🎥 Select and process any `.mp4` video for vehicle detection.
- 📏 Real-world speed estimation using pixel calibration and FPS.
- 🚨 Overspeed alert with notification sound.
- 📸 Automatic snapshots of over-speeding vehicles.
- 📝 CSV logging of violations with speed and timestamp.
- 🔍 License plate detection with EasyOCR.
- 📊 Speed trend graph using Matplotlib.
- 🖥️ Beautiful Tkinter GUI with multithreading for smooth operation.

---

## 📁 Project Structure

.
├── app.py # Main GUI application
├── robot/
│ ├── cars.xml # Haar Cascade for vehicle detection
│ └── notification-alert.mp3 # Alert sound file
├── snapshots/ # Snapshots of over-speeding vehicles
├── logs/
│ └── violations.csv # CSV log file
├── chart/
│ └── speed_chart.png # Line chart of vehicle speeds



---

## 📷 Sample Output

- 💨 Speed displayed on detected vehicles in the video.
- 🚨 Alerts for vehicles going over 60 km/h (default).
- 🖼️ Snapshots saved to `/snapshots` folder.
- 🧾 CSV log saved to `/logs/violations.csv`.
- 📈 Line chart saved to `/chart/speed_chart.png`.

---

## 🧪 Requirements

Install required libraries using pip:

```bash
pip install opencv-python easyocr numpy matplotlib Pillow pygame

PIXELS_PER_METER = 8         # Calibration for real-world distance
OVERSPEED_LIMIT = 60         # km/h speed limit
FRAME_INTERVAL = 5           # Frame gap for tracking

 How It Works
Select a video file using the GUI.

The system detects vehicles using Haar cascade.

Tracks them between frames and calculates their speed.

For vehicles over the speed limit:

Sound alert is played.

Snapshot of the vehicle is saved.

Speed violation is logged.

License plate text is extracted (if detected).

A speed chart is generated and saved at the end.

📌 Notes
System is most accurate with stable, side-angle or overhead road videos.

Ensure you have a visible scale (like lane markers) for distance calibration.

EasyOCR may require internet access on first run to download model weights.

📬 Contact
For questions or contributions, feel free to open an issue or fork the repo!

Developed by [NEERUGANTI SIDDARTHA]

yaml
Copy
Edit

---

Let me know if you'd like:
- The file content as a downloadable `.md` file.
- A license (`MIT`, `Apache`, etc.).
- A sample `.gitignore` or folder upload script.


