import csv
import tkinter as tk
from tkinter import ttk
from functools import partial
import pandas as pd

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
        initial_values = self.read_initial_values_from_csv()

        labels_and_vars = [
            ("COUNTRY:", tk.StringVar(value=initial_values.get('COUNTRY', '')),
             self.get_unique_values('COUNTRY'), ttk.Combobox),
            ("MONTH_NAME:", tk.StringVar(value=initial_values.get('MONTH_NAME', '')),
             self.get_unique_values('MONTH_NAME'), ttk.Combobox),
            ("YEAR:", tk.StringVar(value=initial_values.get('YEAR', '')),
             self.get_unique_values('YEAR'), ttk.Combobox),
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
            # Read the CSV file into a DataFrame
            df = pd.read_csv('../resource/house.csv')

            # Filter rows based on user input
            filtered_df = df[(df['COUNTRY'] == country) & (df['MONTH_NAME'] == month_name) & (df['YEAR'] == year)]

            if not filtered_df.empty:
                # Extract values from the 'PRODUCT' column
                product_values = filtered_df.iloc[0][['Hydro', 'Natural gas', 'Renewables', 'Non-renewables']]

                # Update the corresponding Entry widgets for Hydro, Natural gas, Renewables, and Non-renewables
                labels_and_vars[3][1].set(product_values['Hydro'])
                labels_and_vars[4][1].set(product_values['Natural gas'])
                labels_and_vars[5][1].set(product_values['Renewables'])
                labels_and_vars[6][1].set(product_values['Non-renewables'])

            else:
                self.clear_output_labels(labels_and_vars)

        except FileNotFoundError:
            print("File not found")

    def clear_output_labels(self, labels_and_vars):
        for i in range(3, len(labels_and_vars)):
            labels_and_vars[i][1].set("")

    def read_initial_values_from_csv(self):
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv('../resource/house.csv')

            if not df.empty:
                return {'COUNTRY': df.iloc[0]['COUNTRY'], 'MONTH_NAME': df.iloc[0]['MONTH_NAME'], 'YEAR': df.iloc[0]['YEAR']}
        except FileNotFoundError:
            print("File not found")
        return {}

    def get_unique_values(self, column_name):
        try:
            # Read the CSV file into a DataFrame
            df = pd.read_csv('../resource/house.csv')

            return sorted(set(df[column_name]))
        except FileNotFoundError:
            print("File not found")


if __name__ == "__main__":
    app = CarbonFootprintCalculator()
    app.mainloop()
