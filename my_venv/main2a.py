import tkinter as tk
from tkinter import ttk
import pandas as pd

def submit():
    try:
        # Get values from input fields
        country_value = country_var.get()
        month_value = month_var.get()
        year_value = year_var.get()
        household_size = household_entry.get()

        # Check if all fields are selected
        if country_value == "Select Country" or month_value == "Select Month" or year_value == "Select Year" or household_size == "":
            raise ValueError("Please input your selections")

        # Filter data based on selected values
        selected_data = data[(data['COUNTRY'] == country_value) & (data['MONTH_NAME'] == month_value) & (
                    data['YEAR'] == int(year_value))]

        # Ensure that the selected_data is not empty
        if not selected_data.empty:
            hydro_value = selected_data[selected_data['PRODUCT'] == 'Hydro']['VALUE'].values[0]
            natural_gas_value = selected_data[selected_data['PRODUCT'] == 'Natural gas']['VALUE'].values[0]
            renewables_value = selected_data[selected_data['PRODUCT'] == 'Renewables']['VALUE'].values[0]
            non_renewables_value = selected_data[selected_data['PRODUCT'] == 'Non-renewables']['VALUE'].values[0]

            # Calculate the total value
            total_value = hydro_value + natural_gas_value + renewables_value + non_renewables_value

            # Find similar year column in Population.csv
            population_data = pd.read_csv('../resource/Population.csv')
            population_value = population_data[year_value].loc[population_data['COUNTRY'] == country_value].values[0]

            # Calculate carbon footprint per person
            carbon_footprint_per_person = (total_value / population_value) * int(household_size) * 1000

            # Update labels with calculated values
            hydro_label_var.set(f"Hydro: {hydro_value}")
            natural_gas_label_var.set(f"Natural Gas: {natural_gas_value}")
            renewables_label_var.set(f"Renewables: {renewables_value}")
            non_renewables_label_var.set(f"Non-renewables: {non_renewables_value}")
            total_label_var.set(f"Total: {total_value}")
            carbon_footprint_label_var.set(f"Carbon Footprint Result: {carbon_footprint_per_person} kilo tonnes of CO2")
        else:
            # Update labels when data is not available
            hydro_label_var.set("Hydro: Data not available")
            natural_gas_label_var.set("Natural Gas: Data not available")
            renewables_label_var.set("Renewables: Data not available")
            non_renewables_label_var.set("Non-renewables: Data not available")
            total_label_var.set("Total: Data not available")
            carbon_footprint_label_var.set("Carbon Footprint per person: Data not available")
    except ValueError as e:
        # Handle the exception (display an error message, etc.)
        print(f"Error: {e}")

# Read data from the CSV file (replace 'house.csv' with your actual file name)
data = pd.read_csv('../resource/house.csv')
countries = sorted(data['COUNTRY'].unique())
months = sorted(data['MONTH_NAME'].unique())
years = sorted(data['YEAR'].unique())

# Create the main window
root = tk.Tk()
root.title("Household Information App")

# Set the background color to navy blue
root.configure(bg='#001F3F')  # Hex color for navy blue

# Set the dimensions of the window
root.geometry("500x500")  # Adjust the width and height as needed

# Create a title label
title_label = tk.Label(root, text="Blue Marble Carbon Footprint Calculator", font=('Helvetica', 16, 'bold'),
                       bg='#001F3F', fg='white')
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Create input fields and labels
tk.Label(root, text="Country:", bg='#001F3F', fg='white').grid(row=1, column=0, padx=10, pady=10)
country_var = tk.StringVar(root)
country_dropdown = ttk.Combobox(root, textvariable=country_var, values=countries, state="readonly")
country_dropdown.grid(row=1, column=1, padx=10, pady=10, sticky='w')
country_dropdown.set("Select Country")

tk.Label(root, text="Month:", bg='#001F3F', fg='white').grid(row=2, column=0, padx=10, pady=10)
month_var = tk.StringVar(root)
month_dropdown = ttk.Combobox(root, textvariable=month_var, values=months, state="readonly")
month_dropdown.grid(row=2, column=1, padx=10, pady=10, sticky='w')
month_dropdown.set("Select Month")

tk.Label(root, text="Year:", bg='#001F3F', fg='white').grid(row=3, column=0, padx=10, pady=10)
year_var = tk.StringVar(root)
year_dropdown = ttk.Combobox(root, textvariable=year_var, values=years, state="readonly")
year_dropdown.grid(row=3, column=1, padx=10, pady=10, sticky='w')
year_dropdown.set("Select Year")

tk.Label(root, text="Household Size:", bg='#001F3F', fg='white').grid(row=4, column=0, padx=10, pady=10)
household_entry = tk.Entry(root)
household_entry.grid(row=4, column=1, padx=10, pady=10, sticky='w')

# Create a submit button
submit_button = tk.Button(root, text="Submit", command=submit, bg='#2980b9', fg='white')
submit_button.grid(row=5, column=0, columnspan=2, pady=10)

# Create labels to display the calculated values
hydro_label_var = tk.StringVar()
hydro_label = tk.Label(root, textvariable=hydro_label_var, bg='#001F3F', fg='white')
hydro_label.grid(row=6, column=0, padx=10, pady=5, columnspan=2)

natural_gas_label_var = tk.StringVar()
natural_gas_label = tk.Label(root, textvariable=natural_gas_label_var, bg='#001F3F', fg='white')
natural_gas_label.grid(row=7, column=0, padx=10, pady=5, columnspan=2)

renewables_label_var = tk.StringVar()
renewables_label = tk.Label(root, textvariable=renewables_label_var, bg='#001F3F', fg='white')
renewables_label.grid(row=8, column=0, padx=10, pady=5, columnspan=2)

non_renewables_label_var = tk.StringVar()
non_renewables_label = tk.Label(root, textvariable=non_renewables_label_var, bg='#001F3F', fg='white')
non_renewables_label.grid(row=9, column=0, padx=10, pady=5, columnspan=2)

carbon_footprint_label_var = tk.StringVar()
carbon_footprint_label = tk.Label(root, textvariable=carbon_footprint_label_var, bg='#001F3F', fg='white')
carbon_footprint_label.grid(row=10, column=0, padx=10, pady=5, columnspan=2)

# Create a label to display the total value
total_label_var = tk.StringVar()
total_label = tk.Label(root, textvariable=total_label_var, bg='#001F3F', fg='white')
total_label.grid(row=11, column=0, padx=10, pady=5, columnspan=2)

# Calculate center position
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - root.winfo_reqwidth()) / 2
y_coordinate = (screen_height - root.winfo_reqheight()) / 2

# Set the window to be centered on the screen
root.geometry("+%d+%d" % (x_coordinate, y_coordinate))

# Run the main loop
root.mainloop()
