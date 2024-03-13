import tkinter as tk
from PIL import Image, ImageTk
import subprocess


def open_food_script():
    # Execute the Python script for a new game
    subprocess.Popen(["python", "main.py"])


def open_household_script():
    # Execute the Python script for settings
    subprocess.Popen(["python", "main2a.py"])


def open_car_script():
    # Execute the Python script for settings
    subprocess.Popen(["python", "main3a.py"])


# Create the main window
root = tk.Tk()
root.title("Carbon Footprint Calculator")

# Load the background image
background_image = Image.open("../resource/background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

# Set the window size
window_width = 600
window_height = 600
root.geometry(f"{window_width}x{window_height}")

# Create a label to display the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create a label for the title
title_label = tk.Label(root, text="Carbon Footprint Calculator", font=("Helvetica", 24), fg="black")
title_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

# Create buttons for options
food_button = tk.Button(root, text="Food", font=("Helvetica", 16), command=open_food_script)
food_button.place(relx=0.5, rely=0.3, anchor=tk.CENTER)

household_button = tk.Button(root, text="Household", font=("Helvetica", 16), command=open_household_script)
household_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

car_button = tk.Button(root, text="Car", font=("Helvetica", 16), command=open_car_script)
car_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

exit_button = tk.Button(root, text="Exit", font=("Helvetica", 16), command=root.destroy)
exit_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

# Run the Tkinter event loop
root.mainloop()
