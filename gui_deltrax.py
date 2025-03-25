import tkinter as tk
from import_data_nested import my_test_fun
""" Author Michael McNerney 25/03/2025.
This code is a GUI for running the processing of a .DAT data log files which is produced by other logger software.
It allows the user to read the instructions shown in the Tkinter box before using the button options
to either proceed with the process or exit the GUI. The "Start File Processing button calls the main imported
function "my_test_fun" from the import_data_nested.py file. That process opens a file open dialog box
and processes the .DAT file before asking the user where they want to save the new Excel file. It then delivers 
a "completion" info message at the end to confirm to the user when the process is complete. the App should then
shut down and to run it again, the app has to be restarted."""


root = tk.Tk()
root.geometry("600x500")
root.title("E-Tracker Data Log Processor (MMcNerney)")
label = tk.Label(root, text="Convert E-Tracker .DAT datalog files into Excel files", font=("Arial)", 17))
label.pack(padx=10, pady=10)

button = tk.Button(root, text="Start File Processing", command=my_test_fun, font=('Arial', 14))
button.pack(padx=10, pady=20)

label = tk.Label(root, text="Click on the button above to start the process\nNavigate to the .DAT file when the file "
                            "open dialog box appears and click OK\nThis software will then process the file and when "
                            "finished will open a file save as dialog box"
                            " and ask you where you want it saved to.\n\nGive it a name, select the location and "
                            "click OK.\n\n"
                            "The new Excel format report will be saved there.\nYou can then use the Excel report file "
                            "to produce\n"
                            "detailed reports and graphs either in Excel or Word\n"
                            "To end program use the EXIT button",
                 wraplength=290, font=("Arial)", 10))
label.pack(padx=10, pady=20)
button = tk.Button(root, text="Exit", command=root.destroy, font=('Arial', 17))
button.pack(padx=20, pady=10)


root.mainloop()
