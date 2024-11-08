import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from collections import Counter

# Import the UserDatabase class
from user_database import UserDatabase

# Wheel settings
wheel_radius = 250
center = (300, 300)
num_segments = 6  # Number of slices on the wheel (will match with genres)
angle_per_segment = 360 / num_segments

# Genre settings
genres = ["Fantasy", "Adventure", "Sci-Fi", "Horror", "Mystery", "Comedy"]
labels = genres

# Color settings (one color for each genre)
colors = ["#FF6347", "#FFD700", "#8A2BE2", "#DC143C", "#20B2AA", "#FF8C00"]  # Red, Yellow, Purple, Crimson, Light Sea Green, Dark Orange

class SpinYarnGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Spin a Yarn Game")
        self.root.geometry("800x600")
        self.root.config(bg="#f0f0f0")

        self.main_frame = tk.Frame(self.root, bg="white", bd=5, relief="groove")
        self.main_frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)

        self.title_label = tk.Label(self.main_frame, text="Spin a Yarn Game", font=("Helvetica", 32, "bold"), fg="#4B0082", bg="white")
        self.title_label.pack(pady=30)

        self.play_button_friends = ttk.Button(self.main_frame, text="Play with Friends", style="TButton", command=self.ask_number_of_players)
        self.play_button_friends.pack(pady=20)

        self.players = []
        self.current_player_index = 0
        self.selected_genre = None
        self.stories = []
        self.votes = []

        self.style = ttk.Style()
        self.style.configure("TButton", font=("Helvetica", 14), relief="flat", background="#1E3A8A", foreground="blue")
        self.style.map("TButton", background=[("active", "#1D3F87")])

        # Initialize the UserDatabase
        self.user_db = UserDatabase()

    # Show signup page
    def show_signup_page(self):
        self.clear_frame()

        self.signup_label = tk.Label(self.main_frame, text="Sign Up", font=("Helvetica", 24), fg="#4B0082", bg="white")
        self.signup_label.pack(pady=30)

        self.username_label = tk.Label(self.main_frame, text="Username:", font=("Helvetica", 16), bg="white")
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Helvetica", 16), bg="white")
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=10)

        self.signup_button = ttk.Button(self.main_frame, text="Sign Up", command=self.signup)
        self.signup_button.pack(pady=20)

    # Show login page
    def show_login_page(self):
        self.clear_frame()

        self.login_label = tk.Label(self.main_frame, text="Login", font=("Helvetica", 24), fg="#4B0082", bg="white")
        self.login_label.pack(pady=30)

        self.username_label = tk.Label(self.main_frame, text="Username:", font=("Helvetica", 16), bg="white")
        self.username_label.pack(pady=10)
        self.username_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
        self.username_entry.pack(pady=10)

        self.password_label = tk.Label(self.main_frame, text="Password:", font=("Helvetica", 16), bg="white")
        self.password_label.pack(pady=10)
        self.password_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ttk.Button(self.main_frame, text="Login", command=self.login)
        self.login_button.pack(pady=20)

    # Signup method (using SQLite database)
    def signup(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Check if username already exists
        if self.user_db.username_exists(username):
            messagebox.showerror("Error", "Username already exists. Please login.")
            return

        # Add the new user to the database
        self.user_db.add_user(username, password)
        messagebox.showinfo("Success", "Account created successfully!")
        self.show_login_page()

    # Login method (validating against SQLite database)
    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Both fields are required.")
            return

        # Validate the username and password
        if not self.user_db.validate_user(username, password):
            messagebox.showerror("Error", "Invalid username or password.")
            return

        messagebox.showinfo("Success", f"Welcome back, {username}!")
        self.show_main_game()

    # Show the main game interface
    def show_main_game(self):
        self.clear_frame()

        self.title_label = tk.Label(self.main_frame, text="Spin a Yarn Game", font=("Helvetica", 32, "bold"), fg="#4B0082", bg="white")
        self.title_label.pack(pady=30)

        self.play_button_friends = ttk.Button(self.main_frame, text="Play with Friends", style="TButton", command=self.ask_number_of_players)
        self.play_button_friends.pack(pady=20)

    def ask_number_of_players(self):
        self.clear_frame()

        self.number_label = tk.Label(self.main_frame, text="Enter number of players:", font=("Helvetica", 18), bg="white")
        self.number_label.pack(pady=20)

        self.number_entry = ttk.Entry(self.main_frame, font=("Helvetica", 14), width=5)
        self.number_entry.pack(pady=10)

        self.submit_number_button = ttk.Button(self.main_frame, text="Submit", command=self.get_player_names)
        self.submit_number_button.pack(pady=20)

    def get_player_names(self):
        try:
            num_players = int(self.number_entry.get())
            if num_players < 2:
                raise ValueError("At least 2 players are required.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
            return
        
        self.clear_frame()
        self.players = []
        self.get_names(num_players)

    def get_names(self, num_players):
        self.name_label = tk.Label(self.main_frame, text=f"Enter names for {num_players} players:", font=("Helvetica", 18), bg="white")
        self.name_label.pack(pady=20)

        self.name_entries = []
        for i in range(num_players):
            entry = ttk.Entry(self.main_frame, font=("Helvetica", 14))
            entry.pack(pady=5)
            self.name_entries.append(entry)

        self.start_button = ttk.Button(self.main_frame, text="Start Game", command=self.start_game_from_entries)
        self.start_button.pack(pady=20)

    def start_game_from_entries(self):
        self.players = [entry.get().strip() for entry in self.name_entries]
        self.players = [name for name in self.players if name]  # Remove empty names

        if len(self.players) < 2:
            messagebox.showerror("Error", "Please enter at least two names.")
        else:
            self.start_game()

    def start_game(self):
        self.clear_frame()
        self.stories = []
        self.current_player_index = 0
        self.spin_button_friends = ttk.Button(self.main_frame, text="Spin the Genre Wheel", command=self.spin_wheel, style="TButton")
        self.spin_button_friends.pack(pady=30)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SpinYarnGame(root)
    app.show_signup_page()  # Start by showing the signup page
    root.mainloop()
