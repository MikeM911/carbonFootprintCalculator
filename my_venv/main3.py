import pandas as pd
import tkinter as tk
from tkinter import ttk

class TransportCategoryApp:
    def __init__(self, car_data):
        self.total_var = None
        self.result_label = None
        self.make_var = tk.StringVar()
        self.model_var = tk.StringVar()
        self.vehicle_class_var = tk.StringVar()
        self.car_data = car_data

        self.labels_and_vars = [
            ("Make:", self.make_var, car_data['Make'].unique().tolist(), ttk.Combobox, 20),
            ("Model:", self.model_var, [], ttk.Combobox, 20),
            ("Vehicle Class:", self.vehicle_class_var, car_data['Vehicle Class'].unique().tolist(), ttk.Combobox, None),
            ("Fuel Consumption:", tk.StringVar(), None, tk.Entry, None),
        ]

        self.frame = ttk.LabelFrame(root, text="Transport")
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        create_category_widgets(root, 1, 0, "Transport", self.labels_and_vars, self)

        # Set event binding to update model choices when the make is selected
        self.make_var.trace_add("write", self.update_model_choices)

    def update_model_choices(self, *args):
        selected_make = self.make_var.get()

        if selected_make:
            models_for_make = self.car_data[self.car_data['Make'] == selected_make]['Model'].unique().tolist()
            self.labels_and_vars[1][3].set_values(models_for_make)

            # If the current selected model is not in the new choices, clear the selection
            if self.model_var.get() not in models_for_make:
                self.labels_and_vars[1][1].set('')

    def retrieve_data(self):
        make = self.labels_and_vars[0][1].get()
        model = self.labels_and_vars[1][1].get()
        vehicle_class = self.labels_and_vars[2][1].get()

        try:
            for index, row in self.car_data.iterrows():
                if row['Make'] == make and row['Model'] == model and row['Vehicle Class'] == vehicle_class:
                    self.labels_and_vars[3][1].set(row['Fuel Consumption Comb (L/100 km)'])
                    self.total_var.set(row['Total'])
                    self.result_label.config(text="Data retrieved successfully!")
                    return

            self.result_label.config(text="Data not found for the given inputs.")

        except FileNotFoundError:
            self.result_label.config(text="CSV file not found.")

    def set_total_var(self, total_var):
        self.total_var = total_var

class MyCombobox(ttk.Combobox):
    def set_values(self, values):
        self['values'] = values

def set_combobox_values(combobox, values):
    combobox['values'] = values

# Add this function to set values to combobox
MyCombobox.set_values = set_combobox_values

def read_car_data(file_path):
    car_data = pd.read_csv(file_path)
    return car_data

def get_vehicle_classes(car_data):
    return car_data['Vehicle Class'].unique().tolist()

def create_label_entry_pair(parent, row, column, label_text, entry_var=None, options=None, widget_type=tk.Entry, combobox_width=None):
    label = tk.Label(parent, text=label_text)
    label.grid(row=row, column=column, padx=5, pady=5, sticky="e")

    if options:
        # Sort the options alphabetically
        options = sorted(options)
        entry = MyCombobox(parent, values=options, textvariable=entry_var, width=combobox_width)
    else:
        entry = widget_type(parent, textvariable=entry_var)

    entry.grid(row=row, column=column + 1, padx=5, pady=5)
    return entry

def create_category_widgets(parent, row, column, category_name, labels_and_vars, transport_category_app=None):
    frame = ttk.LabelFrame(parent, text=category_name)
    frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    for i, (label_text, entry_var, options, widget_type, combobox_width) in enumerate(labels_and_vars, start=1):
        create_label_entry_pair(frame, i, 0, label_text, entry_var, options, widget_type, combobox_width)

    total_var = tk.StringVar()
    total_label = tk.Label(frame, text="Total:")
    total_label.grid(row=i + 1, column=0, pady=5, sticky="e")
    total_entry = tk.Entry(frame, textvariable=total_var, state="readonly")
    total_entry.grid(row=i + 1, column=1, pady=5)

    if transport_category_app:
        transport_category_app.set_total_var(total_var)

    retrieve_button = tk.Button(frame, text="Retrieve Data", command=transport_category_app.retrieve_data)
    retrieve_button.grid(row=i + 2, column=0, columnspan=2, pady=5, sticky="nsew")

    transport_category_app.result_label = ttk.Label(frame, text="")
    transport_category_app.result_label.grid(row=i + 3, column=0, columnspan=2)

# Create the main Tkinter window
root = tk.Tk()

# Set the title of the window
root.title("Carbon Footprint Calculator")

# Set the background color of the main window to navy blue
root.configure(bg='navy')

# Create and place a Label widget to display a title within the window
title_label = tk.Label(root, text="Blue Marble Carbon Footprint Calculator", font=("Helvetica", 16), bg='navy', fg='white')
title_label.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

# Read car makes and models from CSV file
car_data = read_car_data("../resource/car.csv")

# Instantiate the TransportCategoryApp
transport_category_app = TransportCategoryApp(car_data)

# Use Checkbutton for "Car Type" in Transport category
create_category_widgets(root, 1, 0, "Transport", [
    ("Make:", tk.StringVar(), car_data['Make'].unique().tolist(), MyCombobox, 20),
    ("Model:", tk.StringVar(), car_data['Model'].unique().tolist(), MyCombobox, 20),
    ("Vehicle Class:", tk.StringVar(), car_data['Vehicle Class'].unique().tolist(), ttk.Combobox, None),
    ("Fuel Consumption:", tk.StringVar(), None, tk.Entry, None),
], transport_category_app)

# Set column weights to make them expand and fill any extra space
for i in range(1, 2):  # Assuming there is 1 column
    root.columnconfigure(i, weight=1)

# Set the window size to 600x400 pixels
window_width = 600
window_height = 400
root.geometry(f"{window_width}x{window_height}")

# Run the Tkinter event loop
root.mainloop()