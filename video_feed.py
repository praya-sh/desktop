import cv2
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk
import nepali_roman as nr
import re


def setup_video_feed(dashboard_app, parent_frame):
    dashboard_app.video_label = tk.Label(parent_frame, bg='white')
    dashboard_app.video_label.pack(side=tk.LEFT, padx=20, pady=20, fill=tk.BOTH, expand=True)

    dashboard_app.cap = cv2.VideoCapture('http://192.168.43.1:8080/video')  # Open webcam or change to your IP camera URL
    dashboard_app.video_feed_active = dashboard_app.cap.isOpened()
    if dashboard_app.video_feed_active:
        update_video_feed(dashboard_app)
    else:
        dashboard_app.video_label.config(text="No video feed available")

def update_video_feed(dashboard_app):
    if dashboard_app.video_feed_active:
        ret, frame = dashboard_app.cap.read()
        if ret:
            dashboard_app.current_frame = frame  # Store the current frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            dashboard_app.video_label.imgtk = imgtk
            dashboard_app.video_label.configure(image=imgtk)
        else:
            dashboard_app.video_feed_active = False
            dashboard_app.video_label.config(text="No video feed available")
    dashboard_app.video_label.after(10, lambda: update_video_feed(dashboard_app))

def capture_frame(dashboard_app):
    if hasattr(dashboard_app, 'current_frame'):
        try:
            image = cv2.imread("3.jpg")

            #plate type and number plate detection
            predictions = dashboard_app.npr_model.predict(dashboard_app.current_frame)  #dashboard_app.current_frame
            detected_plate_number = predictions.get("ocr", "N/A")
            converted_plate = nepali_to_english(detected_plate_number).upper()
            plate_type = predictions.get("cls", "N/A")

            #vehicle type detection
            vehicle_type_idx = dashboard_app.vehicle_classiffier.predict(dashboard_app.current_frame)
            vehicle_types = ["no wheeler", "2 Wheeler", "4 Wheeler"]
            vehicle_type = vehicle_types[vehicle_type_idx]

            # Update GUI elements with detected information
            dashboard_app.plate_number_entry.delete(0, tk.END)
            dashboard_app.plate_number_entry.insert(0, converted_plate)
            dashboard_app.correct_plate_entry.delete(0, tk.END)
            dashboard_app.correct_plate_entry.insert(0, converted_plate)
            dashboard_app.plate_type_box.set(plate_type)
            dashboard_app.vehicle_type_box.set(vehicle_type)

            # Optionally, save the captured frame with timestamp
            filename = datetime.now().strftime("%Y%m%d_%H%M%S") + ".jpg"
            cv2.imwrite(filename, dashboard_app.current_frame)
            print(f"Captured frame and saved as {filename}")

        except Exception as e:
            print(f"Error processing frame: {str(e)}")

 

def nepali_to_english(text):
    if nr.is_devanagari(text):
        return nr.romanize_text(text)
    else:
        return text