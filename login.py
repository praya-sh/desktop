import tkinter as tk
from tkinter import messagebox
import requests
from dashboard import *
import auth

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("1000x600")  # Set window size to 1000 by 800

        self.app_label= tk.Label(root, text="Superveyes: A Machine Learning Assisted Parking Management System",  font=("Arial", 18))
        self.app_label.pack(pady=20)
        # Create and place the username label and entry
        self.username_label = tk.Label(root, text="Username:", font=("Arial", 14))
        self.username_label.pack(pady=20)
        self.username_entry = tk.Entry(root, font=("Arial", 14))
        self.username_entry.pack(pady=20)

        # Create and place the password label and entry
        self.password_label = tk.Label(root, text="Password:", font=("Arial", 14))
        self.password_label.pack(pady=20)
        self.password_entry = tk.Entry(root, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=20)

        # Create and place the login button
        self.login_button = tk.Button(root, text="Login", command=self.handle_login, font=("Arial", 14))
        self.login_button.pack(pady=20)

    def handle_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Make the POST request to the backend API
        try:
            response = requests.post(
                'http://127.0.0.1:8000/login',
                headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                json={'username': username, 'password': password}
            )
            response_data = response.json()

            if response.status_code == 200:
                # Store the access token
                access_token = response_data.get('access_token')
                auth.set_access_token(access_token)

                messagebox.showinfo("Success", "Login Successful!")
                self.redirect_to_dashboard()
            else:
                messagebox.showerror("Error", f"Login Failed: {response_data.get('detail', 'Unknown error')}")
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def redirect_to_dashboard(self):
        self.root.destroy()  # Close the login window
        dashboard_root = tk.Tk()
        dashboard_app = DashboardApp(dashboard_root)
        dashboard_root.mainloop()


