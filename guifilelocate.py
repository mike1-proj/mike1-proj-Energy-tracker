import tkinter as tk
from tkinter import filedialog
import pandas as pd

# first  attempt at a file open process. I used a modified version in the actual main code

file_data = ""


def load_file():
    global file_data
    file_path = filedialog.askopenfilename(title="Select a file")
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
        text_var.set(f"File loaded: {file_path}")
        file_data = file_content  # Store the file content in a global variable
        root.destroy()


# Create the main window


root = tk.Tk()
root.title("File Loader")
root.geometry("400x200")

# Create UI elements
text_var = tk.StringVar()
text_var.set("No file selected")

label = tk.Label(root, textvariable=text_var, wraplength=350)
label.pack(pady=10)

button = tk.Button(root, text="Browse", command=load_file)
button.pack(pady=5)

# Run the application
root.mainloop()

# now the code below will allow me to save the file using the gui process to locate the target


def save_file(df):
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    file_path = filedialog.asksaveasfilename(
        title="Save CSV File",
        defaultextension=".csv",  # Ensures the file has a .csv extension
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
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

# Call the save function
save_file(df)
