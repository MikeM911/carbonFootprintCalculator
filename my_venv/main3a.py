import tkinter as tk
from tkinter import ttk
import pandas as pd

# Function to calculate fuel consumption
def calculate_fuel_consumption(make, model, distance):
    try:
        # Get the fuel consumption for the given make and model
        fuel_consumption_comb = df[(df['Make'] == make) & (df['Model'] == model)]['Fuel Consumption Comb (L/100 km)'].values[0]

        # Calculate the total fuel consumption based on the provided distance
        total_fuel_consumption = (float(distance) / 100) * fuel_consumption_comb
        return fuel_consumption_comb, total_fuel_consumption
    except (IndexError, ValueError):
        return None, None

# Function to update model options based on selected make
def update_model_options(*args):
    selected_make = make_var.get()
    model_dropdown['values'] = tuple(df[df['Make'] == selected_make]['Model'].unique())
    model_var.set(model_dropdown['values'][0])

# Function to handle submission
def submit():
    make_value = make_var.get()
    model_value = model_var.get()
    distance_value = distance_entry.get()

    try:
        # Check if Distance is blank
        if distance_value == "":
            raise ValueError("Distance field is blank")

        # Calculate the fuel consumption
        fuel_consumption_comb, total_fuel_consumption = calculate_fuel_consumption(make_value, model_value, distance_value)

        if fuel_consumption_comb is not None and total_fuel_consumption is not None:
            result_label.config(
                text=f"Make: {make_value}\nModel: {model_value}\nDistance: {distance_value} km\nFuel Consumption Comb: {fuel_consumption_comb:.2f} L/100 km\n\nTotal Fuel Consumption: {total_fuel_consumption:.2f} L")
        else:
            result_label.config(text="Error: Make and Model not found in the dataset.")
    except ValueError as e:
        result_label.config(text=str(e))

# Read the CSV file with pandas
df = pd.read_csv('../resource/car.csv')

# Extract unique values from the 'Make' and 'Model' columns
make_options = df['Make'].unique()

# Create the main window
root = tk.Tk()
root.title("Car Information App")  # Set the title of the window

# Set the background color to navy blue
root.configure(bg="#001F3F")  # Hex color for navy blue

# Set the size of the window
root.geometry("500x500")  # Width x Height

# Create a title label
title_label = tk.Label(root, text="Blue Marble Carbon Footprint Calculator", font=("Helvetica", 16, "bold"),
                       bg="#001F3F", fg="white")
title_label.grid(row=0, column=0, columnspan=2, pady=10)

# Create labels and entry widgets for Make and Model
make_label = tk.Label(root, text="Make:", bg="#001F3F", fg="white")  # Set text and foreground color
make_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)

# Create a variable to store the selected make
make_var = tk.StringVar(root)
make_var.set(make_options[0])  # Set the default value

# Create a dropdown menu for Make with increased width
make_dropdown = tk.OptionMenu(root, make_var, *make_options, command=update_model_options)
make_dropdown.config(width=20)  # Set the width of the dropdown menu
make_dropdown.grid(row=1, column=1, padx=10, pady=5)

model_label = tk.Label(root, text="Model:", bg="#001F3F", fg="white")  # Set text and foreground color
model_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

# Create a variable to store the selected model
model_var = tk.StringVar(root)
model_var.set(df[df['Make'] == make_var.get()]['Model'].unique()[0])  # Set the default value

# Create a dropdown menu for Model with increased width
model_dropdown = ttk.Combobox(root, textvariable=model_var)
model_dropdown.config(width=20)  # Set the width of the dropdown menu
model_dropdown.grid(row=2, column=1, padx=10, pady=5)

# Create an entry widget for Distance
distance_label = tk.Label(root, text="Enter Distance value (in km):", bg="#001F3F", fg="white")
distance_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)

distance_entry = tk.Entry(root)
distance_entry.grid(row=3, column=1, padx=10, pady=5)

# Create a button to submit the values
submit_button = tk.Button(root, text="Submit", command=submit, bg="#0074CC",
                          fg="white")  # Set background and foreground color
submit_button.grid(row=4, column=0, columnspan=2, pady=10)

# Display the result
result_label = tk.Label(root, text="", bg="#001F3F", fg="white")  # Set background and foreground color
result_label.grid(row=5, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()
