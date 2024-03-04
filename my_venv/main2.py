import csv
import tkinter as tk
from tkinter import ttk
from functools import partial
from house import read_csv

class CarbonFootprintCalculator(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Carbon Footprint Calculator")
        self.configure(bg='navy')

        # Create and place a Label widget to display a title within the window
        title_label = tk.Label(self, text="Blue Marble Carbon Footprint Calculator", font=("Helvetica", 16),
                               bg='navy', fg='white')
        title_label.grid(row=0, column=0, columnspan=4, pady=20, sticky="nsew")

        # Read initial values from the CSV file
        initial_country, initial_month, initial_year = self.read_initial_values_from_csv()

        labels_and_vars = [
            ("COUNTRY:", tk.StringVar(value=initial_country), self.get_unique_values('COUNTRY'), ttk.Combobox),
            ("MONTH_NAME:", tk.StringVar(value=initial_month), self.get_unique_values('MONTH_NAME'), ttk.Combobox),
            ("YEAR:", tk.StringVar(value=initial_year), self.get_unique_values('YEAR'), ttk.Combobox),
            ("Hydro:", tk.StringVar(), None, tk.Entry),
            ("Natural gas:", tk.StringVar(), None, tk.Entry),
            ("Renewables:", tk.StringVar(), None, tk.Entry),
            ("Non-renewables:", tk.StringVar(), None, tk.Entry),
        ]

        self.create_category_widgets("Household", labels_and_vars)

        # Set column weights to make them expand and fill any extra space
        for i in range(1, 3):
            self.columnconfigure(i, weight=1)

        # Set the window size
        self.geometry("1000x600")

    def create_category_widgets(self, category_name, labels_and_vars):
        frame = ttk.LabelFrame(self, text=category_name)
        frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        for i, (label_text, entry_var, options, widget_type) in enumerate(labels_and_vars, start=1):
            entry = self.create_label_entry_pair(frame, i, 0, label_text, entry_var, options, widget_type)

        retrieve_button = tk.Button(frame, text="Retrieve Data",
                                    command=partial(self.retrieve_data, labels_and_vars))
        retrieve_button.grid(row=i + 1, column=0, columnspan=2, pady=5, sticky="nsew")

    def create_label_entry_pair(self, parent, row, column, label_text, entry_var=None, options=None,
                                widget_type=tk.Entry):
        label = tk.Label(parent, text=label_text)
        label.grid(row=row, column=column, padx=5, pady=5, sticky="e")

        if options:
            entry = ttk.Combobox(parent, values=options, textvariable=entry_var)
        else:
            entry = widget_type(parent, textvariable=entry_var)

        entry.grid(row=row, column=column + 1, padx=5, pady=5)
        return entry

    def retrieve_data(self, labels_and_vars):
        country = labels_and_vars[0][1].get()
        month_name = labels_and_vars[1][1].get()
        year = labels_and_vars[2][1].get()

        try:
            file_path = "../resource/house.csv"
            selected_columns = ["COUNTRY", "YEAR", "MONTH_NAME", "PRODUCT", "VALUE"]
            header, data = read_csv(file_path, selected_columns)

            for row in data:
                if row[0] == country and row[2] == month_name and row[1] == year:
                    self.display_values(labels_and_vars, row[3], row[4])
                    return

            # If no matching row is found
            self.clear_output_labels(labels_and_vars)

        except FileNotFoundError:
            print("File not found")

    def display_values(self, labels_and_vars, products, values):
        products_list = products.split(';') if products else []
        values_list = values.split(';') if values else []

        # Retrieve all values at once before updating any widgets
        all_values = dict(zip(
            [l[0].lower() for l in labels_and_vars[3:]],
            [v.strip() for v in values_list]
        ))

        # Update each output widget with its corresponding value
        for i in range(3, len(labels_and_vars)):
            label_name = labels_and_vars[i][0].lower()
            value = all_values.get(label_name, '')
            widget_type = labels_and_vars[i][3]

            if widget_type == ttk.Combobox:
                labels_and_vars[i][1]['VALUE'] = value.split(',')
            else:
                labels_and_vars[i][1].set(value)

    def clear_output_labels(self, labels_and_vars):
        for i in range(3, len(labels_and_vars)):
            labels_and_vars[i][1].set("")

    def read_initial_values_from_csv(self):
        try:
            with open('../resource/house.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                if reader:
                    row = next(reader, None)
                    if row:
                        return row['COUNTRY'], row['MONTH_NAME'], row['YEAR']
        except FileNotFoundError:
            print("File not found")
        return "", "", ""

    def get_unique_values(self, column_name):
        try:
            with open('../resource/house.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                return sorted(set(row[column_name] for row in reader))
        except FileNotFoundError:
            print("File not found")


if __name__ == "__main__":
    app = CarbonFootprintCalculator()
    app.mainloop()
