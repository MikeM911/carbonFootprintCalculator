import csv
import tkinter as tk
from tkinter import ttk


def read_csv(file_path, selected_columns):
    # Open the CSV file and read its contents
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        # Read the header row of the CSV
        header = next(reader)
        # Filter columns based on selected words
        selected_indices = [header.index(word) for word in selected_columns]
        # Create a list of lists containing data from selected columns
        data = [[row[i] for i in selected_indices] for row in reader]
    # Return the selected columns and filtered data
    return selected_columns, data


class CSVTableApp:
    def __init__(self, root, header, data):
        # Initialize the main application window
        self.root = root
        self.root.title("CSV Table Viewer")

        # Create a Treeview widget for displaying the CSV data
        self.tree = ttk.Treeview(root, columns=header, show="headings")

        # Set column headings in the Treeview
        for col in header:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

        # Insert data rows into the Treeview
        for row in data:
            self.tree.insert("", "end", values=row)

        # Pack the Treeview widget into the application window
        self.tree.pack(expand=True, fill="both")


def main():
    # Specify the path to the CSV file and the selected columns
    file_path = "../resource/food.csv"  # Replace with the path to your CSV file
    selected_columns = ["Area", "Year", "Food Transport", "Food Household Consumption", "Food Retail", "Food Packaging", "total_emission"]

    # Read the CSV file and extract selected columns
    header, data = read_csv(file_path, selected_columns)

    # Create the main Tkinter window
    root = tk.Tk()
    # Initialize the CSVTableApp with header and data
    app = CSVTableApp(root, header, data)
    # Start the Tkinter event loop
    root.mainloop()


# Entry point of the script
if __name__ == "__main__":
    main()
