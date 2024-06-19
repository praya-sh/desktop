import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import requests
from video_feed import setup_video_feed, capture_frame
import auth  
from plate_detector import LicensePlateDetector
from vehicle_classifier_class import VehicleClassifier

vehicle_id= 19

class DashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1000x600")  # Set window size to 1000 by 600
        self.root.configure(bg='#414141')

        self.setup_tabs()
        self.setup_live_feed_tab()
        self.setup_database_tab()
        self.setup_available_spaces_tab()
        self.npr_model = LicensePlateDetector(model_path="plate_model.pt")
        self.vehicle_classiffier = VehicleClassifier(model_path="modelv3_3OP.pth")

        self.update_time()

    def setup_tabs(self):
        self.tabControl = ttk.Notebook(self.root)

        self.liveFeedTab = ttk.Frame(self.tabControl)
        self.databaseTab = ttk.Frame(self.tabControl)
        self.availableSpacesTab = ttk.Frame(self.tabControl)
        self.exitTab= ttk.Frame(self.tabControl)

        self.tabControl.add(self.liveFeedTab, text='Live Feed')
        self.tabControl.add(self.databaseTab, text='Database')
        self.tabControl.add(self.availableSpacesTab, text='Available Spaces')


        self.tabControl.pack(expand=1, fill="both")

    def setup_live_feed_tab(self):
        # Create the control frame and set its background to white
        control_frame = tk.Frame(self.liveFeedTab, bg='white', width=500)
        control_frame.pack(side=tk.RIGHT, padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.title_label = tk.Label(control_frame, text="Superveyes", font=("Arial", 20))
        self.title_label.pack(pady=5, fill =tk.BOTH, expand=True)

        # Create comboboxes for vehicle and plate type
        self.vehicle_type_box = ttk.Combobox(control_frame, values=["2 Wheeler", "4 Wheeler"], state="readonly")
        self.vehicle_type_box.set("Vehicle Type")
        self.vehicle_type_box.pack(pady=10, fill = tk.BOTH, expand=True)

        self.plate_type_box = ttk.Combobox(control_frame, values=["Embossed", "Regional", "Provincial"], state="readonly")
        self.plate_type_box.set("License Plate Type")
        self.plate_type_box.pack(pady=10,fill = tk.BOTH,expand=True)

        # Create labels and entry widgets for license plate info
        self.plate_number_label = tk.Label(control_frame, text="Detected License Plate", bg='white', fg='black')
        self.plate_number_label.pack(pady=5,fill = tk.BOTH,expand=True)

        self.plate_number_entry = tk.Entry(control_frame, bg='white', fg='black')
        self.plate_number_entry.pack(pady=10,fill = tk.BOTH,expand=True)

        self.correct_plate_label = tk.Label(control_frame, text="Actual License Plate", bg='white', fg='black')
        self.correct_plate_label.pack(pady=5,fill = tk.BOTH,expand=True)

        self.correct_plate_entry = tk.Entry(control_frame, bg='white', fg='black')
        self.correct_plate_entry.pack(pady=10,fill = tk.BOTH,expand=True)

        # Create labels for date and time
        self.date_label = tk.Label(control_frame, text=datetime.now().date().strftime('%Y-%m-%d'), bg='white', fg='black', font=("Arial", 15))
        self.date_label.pack(pady=10)

        self.time_label = tk.Label(control_frame, text=datetime.now().strftime('%H:%M:%S'), bg='white', fg='black', font=("Arial", 15))
        self.time_label.pack(pady=10)

        # Create buttons with fixed width to make them the same size
        button_width = 20
        self.capture_button = tk.Button(control_frame, text="Capture Frame", command=lambda: capture_frame(self), bg='black', fg='white', width=button_width)
        self.capture_button.pack(pady=10, fill = tk.BOTH, expand = True)

        self.update_button = tk.Button(control_frame, text="Update", command=self.update_and_assign_slot, bg='black', fg='white', width=button_width)
        self.update_button.pack(pady=10,fill = tk.BOTH, expand=True)

        self.exit_button = tk.Button(control_frame, text="Exit", command=self.update_exit_time, bg='black', fg='white', width=button_width)
        self.exit_button.pack(pady=10,fill = tk.BOTH, expand=True)

        setup_video_feed(self, self.liveFeedTab)  # Call the setup_video_feed function from video_feed.py

    def setup_database_tab(self):
        self.databaseTab.rowconfigure(0, weight=1)
        self.databaseTab.rowconfigure(1, weight=9)
        self.databaseTab.columnconfigure(0, weight=1)

        search_frame = tk.Frame(self.databaseTab, bg='white')
        search_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=20)

        # Configure rows and columns for search_frame to center the entry and button
        search_frame.columnconfigure(0, weight=1)
        search_frame.columnconfigure(1, weight=1)
        search_frame.columnconfigure(2, weight=1)
        search_frame.rowconfigure(0, weight=1)

        self.search_entry = tk.Entry(search_frame, width=50)
        self.search_entry.grid(row=0, column=1, padx=10, pady=10)

        self.search_button = tk.Button(search_frame, text="Search", command=self.search_vehicle)
        self.search_button.grid(row=0, column=2, padx=10, pady=10)

        result_frame = tk.Frame(self.databaseTab, bg='#505050')
        result_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)

        # Configure rows and columns for result_frame to expand
        result_frame.columnconfigure(0, weight=1)
       

        self.vehicle_type_label = tk.Label(result_frame, text="Vehicle Type: ", bg='#505050', fg='white')
        self.vehicle_type_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.entry_time_label = tk.Label(result_frame, text="Entry Time: ", bg='#505050', fg='white')
        self.entry_time_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.exit_time_label = tk.Label(result_frame, text="Exit Time: ", bg='#505050', fg='white')
        self.exit_time_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.parking_fees_label = tk.Label(result_frame, text="Parking Fees: ", bg='#505050', fg='white')
        self.parking_fees_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    def setup_available_spaces_tab(self):
        control_frame = tk.Frame(self.availableSpacesTab, bg='#505050')
        control_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
        control_frame.columnconfigure(2, weight=1)
        control_frame.rowconfigure(0, weight=1)
        control_frame.rowconfigure(1, weight=1)
        control_frame.rowconfigure(2, weight=1)
        control_frame.rowconfigure(3, weight=1)
        control_frame.rowconfigure(4, weight=1)

        # Add parking slot section
        self.parking_slot_label = tk.Label(control_frame, text="Add Parking Slot", bg='#505050', fg='white')
        self.parking_slot_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.parking_slot_type_label = tk.Label(control_frame, text="Slot Type", bg='#505050', fg='white')
        self.parking_slot_type_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        self.parking_slot_type_box = ttk.Combobox(control_frame, values=["2 Wheeler", "4 Wheeler"], state="readonly")
        self.parking_slot_type_box.set("Select Slot Type")
        self.parking_slot_type_box.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        self.parking_slot_entry = tk.Entry(control_frame)
        self.parking_slot_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        self.add_slot_button = tk.Button(control_frame, text="Add Slot", command=self.add_parking_slot)
        self.add_slot_button.grid(row=1, column=3, padx=10, pady=5)

        # List of available slots
        self.available_slots_label = tk.Label(control_frame, text="Available Slots", bg='#505050', fg='white')
        self.available_slots_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        self.available_slots_listbox = tk.Listbox(control_frame)
        self.available_slots_listbox.grid(row=2, column=1, padx=10, pady=5, columnspan=3, sticky="ew")

        # Assign slot to vehicle section
        self.assign_slot_label = tk.Label(control_frame, text="Assign Slot to Vehicle", bg='#505050', fg='white')
        self.assign_slot_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        self.vehicle_id_entry = tk.Entry(control_frame)
        self.vehicle_id_entry.grid(row=3, column=1, padx=10, pady=5, sticky="ew")
        self.vehicle_id_entry.insert(0, "Vehicle ID")

        self.slot_id_entry = tk.Entry(control_frame)
        self.slot_id_entry.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
        self.slot_id_entry.insert(0, "Slot ID")

        self.assign_slot_button = tk.Button(control_frame, text="Assign Slot", command=self.assign_slot_to_vehicle)
        self.assign_slot_button.grid(row=3, column=3, padx=10, pady=5)

        self.vehicle_id_label = tk.Label(control_frame, text="Vehicle ID", bg='#505050', fg='white')
        self.vehicle_id_label.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        self.slot_id_label = tk.Label(control_frame, text="Vehicle ID", bg='#505050', fg='white')
        self.slot_id_label.grid(row=4, column=2, padx=10, pady=5, sticky="w")

        self.fetch_available_parking_slots()

    def add_parking_slot(self):
        slot = self.parking_slot_entry.get()
        slot_type= self.parking_slot_type_box.get()
        token = auth.get_access_token()
        
        if not token:
            messagebox.showerror("Error", "No access token found. Please log in again.")
            return
        
        data = {
            "slot_id" : int(slot),
            "slot_type": slot_type,
            "vehicle_id": 0
        }

        try:
            response = requests.post(
                f'http://127.0.0.1:8000/parking_slots/?token={token}',
                headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                json=data
            )

            if response.status_code == 200:
                messagebox.showinfo("Success", "Parking slot added successfully!")
                self.parking_slot_entry.delete(0, tk.END)  # Clear the entry after adding
                self.fetch_available_parking_slots()  # Refresh the listbox
            else:
                response_data = response.json()
                messagebox.showerror("Error", f"Failed to update vehicle data: {response_data.get('detail', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def fetch_available_parking_slots(self):
        self.available_slots_listbox.delete(0, tk.END)  # Clear the listbox before updating
        try:
            response = requests.get('http://127.0.0.1:8000/parking-slots/available')
            if response.status_code == 200:
                available_slots = response.json()
                for slot in available_slots:
                    slot_info = f"Slot ID: {slot['slot_id']}, Slot Type: {slot['slot_type']}"
                    self.available_slots_listbox.insert(tk.END, slot_info)
            else:
                print("Failed to fetch data from the API")
        except Exception as e:
            print(f"An error occurred: {e}")

    def assign_slot_to_vehicle(self):
        vehicle_id = self.vehicle_id_entry.get()
        slot_id = self.slot_id_entry.get()
        token = auth.get_access_token()

        if not token:
            messagebox.showerror("Error", "No access token found. Please log in again.")
            return

        if vehicle_id and slot_id:
            try:
                response = requests.put(
                    f'http://127.0.0.1:8000/parking_slots/{slot_id}/park_vehicle/{vehicle_id}?token={token}',
                    headers={'accept': 'application/json'}
                )

                if response.status_code == 200:
                    response_data = response.json()
                    messagebox.showinfo("Success", response_data.get("message", "Vehicle parked successfully"))
                    self.vehicle_id_entry.delete(0, tk.END)
                    self.slot_id_entry.delete(0, tk.END)
                    self.fetch_available_parking_slots()  # Refresh the listbox
                else:
                    response_data = response.json()
                    messagebox.showerror("Error", f"Failed to assign slot: {response_data.get('detail', 'Unknown error')}")

            except requests.exceptions.RequestException as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def search_vehicle(self):
        plate_number = self.search_entry.get()
        token = auth.get_access_token()

        if not token:
            messagebox.showerror("Error", "No access token found. Please log in again.")
            return

        try:
            response = requests.get(
                f'http://127.0.0.1:8000/vehicles/{plate_number}?token={token}',
                headers={'accept': 'application/json'}
            )

            if response.status_code == 200:
                vehicle_data = response.json()
                self.vehicle_type_label.config(text=f"Vehicle Type: {vehicle_data['vehicle_type']}")
                self.entry_time_label.config(text=f"Entry Time: {vehicle_data['entry_time']}")
                self.exit_time_label.config(text=f"Exit Time: {vehicle_data['exit_time']}")
                self.parking_fees_label.config(text=f"Parking Fees: {vehicle_data['parking_fees']}")
            else:
                response_data = response.json()
                messagebox.showerror("Error", f"Failed to fetch vehicle data: {response_data.get('detail', 'Unknown error')}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_time(self):
        now = datetime.now()
        self.date_label.config(text=now.date().strftime('%Y-%m-%d'))
        self.time_label.config(text=now.strftime('%H:%M:%S'))
        self.root.after(1000, self.update_time)

    def send_vehicle_data(self):
        vehicle_type = self.vehicle_type_box.get()
        predicted_plate = self.plate_number_entry.get()
        actual_plate = self.correct_plate_entry.get()
        entry_time = datetime.now().isoformat()
        token = auth.get_access_token()

        if not token:
            messagebox.showerror("Error", "No access token found. Please log in again.")
            return

        data = {
            "vehicle_id": vehicle_id,  # not assigned dynamically yet
            "vehicle_type": vehicle_type,
            "entry_time": entry_time,
            "predicted_number_plate": predicted_plate,
            "actual_number_plate": actual_plate,
            "exit_time": None,
            "parking_fees": 0
        }

        try:
            response = requests.post(
                f'http://127.0.0.1:8000/vehicles/?token={token}',
                headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                json=data
            )

            if response.status_code == 200:
                messagebox.showinfo("Success", "Vehicle data updated successfully!")
            else:
                response_data = response.json()
                messagebox.showerror("Error", f"Failed to update vehicle data: {response_data.get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_exit_time(self):

        token = auth.get_access_token()
        plate_number=  self.correct_plate_entry.get()
        formatted_exit_time = datetime.now().isoformat()

        if not token:
            messagebox.showerror("Error", "No access token found. Please log in again.")
            return

        try:
            response = requests.put(
                f'http://127.0.0.1:8000/vehicles/{plate_number}/exit?exit_time={formatted_exit_time}&token={token}',
                headers={'accept': 'application/json'}
            )
            if response.status_code == 200:
                messagebox.showinfo("Success", f"Vehicle {plate_number} exited at {formatted_exit_time}")
            else:
                messagebox.showerror("Error", f"Failed to update exit time: {response.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

        try:
            res = requests.get(
                f'http://127.0.0.1:8000/vehicles/{plate_number}?token={token}',
                headers={'accept': 'application/json'}
            )
            vehicle_data = res.json()
            parking_fees = vehicle_data['parking_fees']
            print(parking_fees)
            if res.status_code == 200:
                messagebox.showinfo("Parking Fees", f" Parking Fees = {parking_fees}")
            else:
                messagebox.showerror("Error", f"failed to retrieve parking fees")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def update_and_assign_slot(self):
        self.send_vehicle_data()
        self.auto_assign_parking_slot()

    def auto_assign_parking_slot(self):
        token = auth.get_access_token()
        #vehicle_id=13

        if not token:
            messagebox.showerror("Error", "No access token found. Please log in again.")
            return

        try:
            # Fetch available slots
            res = requests.get(
                f'http://127.0.0.1:8000/parking-slots/available?token={token}',
                headers={'accept': 'application/json'}
            )

            if res.status_code == 200:
                available_slots = res.json()
                if available_slots:
                    first_available_slot = available_slots[0]
                    slot_id = first_available_slot['slot_id']

                    # Assign the first available slot to the vehicle
                    response = requests.put(
                        f'http://127.0.0.1:8000/parking_slots/{slot_id}/park_vehicle/{vehicle_id}?token={token}',
                        headers={'accept': 'application/json'}
                    )

                    # Debugging: print response status code and text
                    print(f"Response Status Code: {response.status_code}")
                    print(f"Response Text: {response.text}")

                    if response.status_code == 200:
                        messagebox.showinfo("Success", f"Vehicle {vehicle_id} assigned to slot {slot_id}")
                        self.fetch_available_parking_slots()  # Refresh the available slots list
                    else:
                        messagebox.showerror("Error", f"Failed to assign slot: {response.text}")
                else:
                    messagebox.showinfo("Info", "No available parking slots")
            else:
                messagebox.showerror("Error", f"Failed to fetch available slots: {res.text}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def on_closing(self):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        self.root.destroy()



# if __name__ == "__main__":
#     root = tk.Tk()
#     app = DashboardApp(root)
#     root.protocol("WM_DELETE_WINDOW", app.on_closing)
#     root.mainloop()
