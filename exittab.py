import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
from video_feed import setup_video_feed, capture_frame
import auth  # Import the auth module


def setup_exit_tab(self):
        control_frame = tk.Frame(self.exitTab, bg="#505050")
        control_frame.pack(side=tk.RIGHT, padx=20, pady=20,fill=tk.Y, expand=False)

        self.predicted_plate_label = tk.Label(control_frame, text="Detected License Plate", bg='#505050', fg='white')
        self.predicted_plate_label.pack(pady=5)

        self.predicted_plate_entry = tk.Entry(control_frame)
        self.predicted_plate_entry.pack(pady=10)

        self.actual_plate_label = tk.Label(control_frame, text="Actual License Plate", bg='#505050', fg='white')
        self.actual_plate_label.pack(pady=5)

        self.actual_plate_entry = tk.Entry(control_frame)
        self.actual_plate_entry.pack(pady=10)

        self.time_label = tk.Label(control_frame, text=datetime.now().strftime('%H:%M:%S'), bg='#505050', fg='white')
        self.time_label.pack(pady=10)

        self.capture_button = tk.Button(control_frame, text="Capture Frame", command=lambda: capture_frame(self))
        self.capture_button.pack(pady=10)

        self.update_button = tk.Button(control_frame, text="Update", command=self.send_vehicle_data)
        self.update_button.pack(pady=10)

        setup_video_feed(self, self.exitTab)
        