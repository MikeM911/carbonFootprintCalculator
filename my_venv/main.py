# Food Carbon Footprint Calculator

import csv
import tkinter as tk
from tkinter import ttk


class FoodCategoryApp:
    def __init__(self):
        self.total_var = None
        self.result_label = None  # Define result_label as an attribute
        self.labels_and_vars = [
            ("Area:", tk.StringVar(), ["Canada"], ttk.Combobox),
            ("Year:", tk.StringVar(value="2000"), list(range(2000, 2021)), ttk.Combobox),
            ("Food Transport:", tk.StringVar(), None, tk.Entry),
            ("Food Household Consumption:", tk.StringVar(), None, tk.Entry),
            ("Food Retail:", tk.StringVar(), None, tk.Entry),
            ("Food Packaging:", tk.StringVar(), None, tk.Entry),
        ]

        # CSV data for Food category
        self.food_csv_data = [
            ["Canada", "2000", "10", "20", "5", "8"],
            ["Canada", "2005", "8", "15", "4", "6"],
            # Add more rows as needed
        ]

        self.frame = ttk.LabelFrame(root, text="Food")
        self.frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        create_category_widgets(root, 1, 0, "Food", self.labels_and_vars, self)

    def retrieve_data(self):
        area = self.labels_and_vars[0][1].get()
        year = self.labels_and_vars[1][1].get()

        try:
            with open('../resource/food.csv', 'r') as file:
                csv_reader = csv.DictReader(file)

                # Find the corresponding row based on user input
                for row in csv_reader:
                    if row['Area'] == area and row['Year'] == year:
                        # Display the corresponding outputs
                        self.labels_and_vars[2][1].set(row['Food Transport'])
                        self.labels_and_vars[3][1].set(row['Food Household Consumption'])
                        self.labels_and_vars[4][1].set(row['Food Retail'])
                        self.labels_and_vars[5][1].set(row['Food Packaging'])
                        self.total_var.set(row['total_emission'])
                        self.result_label.config(text="Data retrieved successfully!")
                        return

            # If the loop completes without finding a match
            self.result_label.config(text="Data not found for the given inputs.")

        except FileNotFoundError:
            self.result_label.config(text="CSV file not found.")

    def set_total_var(self, total_var):
        self.total_var = total_var


def create_label_entry_pair(parent, row, column, label_text, entry_var=None, options=None, widget_type=tk.Entry):
    """
    Create a label and an entry widget pair in the specified parent with the given text and options.

    Parameters:
        parent (tk.Widget): The parent widget to place the label and entry.
        row (int): The row in the grid to place the label and entry.
        column (int): The column in the grid to place the label and entry.
        label_text (str): The text to display in the label.
        entry_var (tk.StringVar, optional): The StringVar associated with the entry widget.
        options (list, optional): List of options for a Combobox widget.
        widget_type (tk.Widget, optional): The type of entry widget to create (default is Entry).

    Returns:
        tk.Widget: The created entry widget.
    """
    label = tk.Label(parent, text=label_text)
    label.grid(row=row, column=column, padx=5, pady=5, sticky="e")

    if options:
        entry = ttk.Combobox(parent, values=options, textvariable=entry_var)
    else:
        entry = widget_type(parent, textvariable=entry_var)

    entry.grid(row=row, column=column + 1, padx=5, pady=5)
    return entry


def create_category_widgets(parent, row, column, category_name, labels_and_vars, food_category_app=None):
    """
    Create widgets for a category within the parent widget.

    Parameters:
        parent (tk.Widget): The parent widget to place the category widgets.
        row (int): The row in the grid to place the category widgets.
        column (int): The column in the grid to place the category widgets.
        category_name (str): The name of the category.
        labels_and_vars (list): List of tuples containing label text, entry variable, options, and widget type.
        food_category_app (FoodCategoryApp, optional): An instance of FoodCategoryApp.
    """
    frame = ttk.LabelFrame(parent, text=category_name)
    frame.grid(row=row, column=column, padx=10, pady=10, sticky="nsew")

    for i, (label_text, entry_var, options, widget_type) in enumerate(labels_and_vars, start=1):
        entry = create_label_entry_pair(frame, i, 0, label_text, entry_var, options, widget_type)

    total_var = tk.StringVar()
    total_label = tk.Label(frame, text="Total:")
    total_label.grid(row=i + 1, column=0, pady=5, sticky="e")
    total_entry = tk.Entry(frame, textvariable=total_var, state="readonly")
    total_entry.grid(row=i + 1, column=1, pady=5)

    if food_category_app:
        food_category_app.set_total_var(total_var)

    # Add a button to retrieve data based on user input
    retrieve_button = tk.Button(frame, text="Retrieve Data", command=food_category_app.retrieve_data)
    retrieve_button.grid(row=i + 2, column=0, columnspan=2, pady=5, sticky="nsew")

    # Add a label for displaying the result of the data retrieval
    food_category_app.result_label = ttk.Label(frame, text="")
    food_category_app.result_label.grid(row=i + 3, column=0, columnspan=2)


# Create the main Tkinter window
root = tk.Tk()

# Set the title of the window
root.title("Food Information App")

# Set the background color of the main window to navy blue
root.configure(bg='navy')

# Create and place a Label widget to display a title within the window
title_label = tk.Label(root, text="Blue Marble Carbon Footprint Calculator", font=("Helvetica", 16), bg='navy',
                       fg='white')
title_label.grid(row=0, column=0, columnspan=4, pady=20, sticky="nsew")  # Set sticky to center the text

food_category_app = FoodCategoryApp()

# Set column weights to make them expand and fill any extra space
for i in range(1, 4):  # Assuming there are 3 columns
    root.columnconfigure(i, weight=1)

# Set the window size to 600x600 pixels
window_width = 500
window_height = 500
root.geometry(f"{window_width}x{window_height}")

# Run the Tkinter event loop
root.mainloop()
