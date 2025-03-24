import tkinter as tk
from tkinter import filedialog
import pandas as pd


def save_file(df):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.asksaveasfilename(
        title="Save file as xlsx Excel File",
        defaultextension=".csv",  # Ensures the file has a .csv extension
        filetypes=[("CSV", "*.csv"), ("All Files", "*.*")]
    )

    if file_path:  # Check if the user selected a file
        try:
            df.to_csv(file_path, index=False)  # Save without the index column
            print(f"File saved successfully at: {file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")
    else:
        print("Save operation canceled.")


# Example DataFrame
data = {"Name": ["Alice", "Bob", "Charlie"], "Age": [25, 30, 35]}
df = pd.DataFrame(data)
print(df)
# Call the save function
save_file(df)
