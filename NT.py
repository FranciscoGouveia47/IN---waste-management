import csv
import os
import sys
import json
import math
import datetime
import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import filedialog
import xlwings as xw
import shutil  # Import the shutil module for file operations
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg')  # Use this backend or try other available backends
import matplotlib.pyplot as plt

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@ INTIAL BACKUP CHECK @@@@@@@@@@@ INTIAL BACKUP CHECK @@@@@@@@@@@ INTIAL BACKUP CHECK @@@@@@@@@@@ INTIAL BA
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Define the path for the directive file
directory_file_path = 'directory_file.json'

# Define the file names for each CSV file
file_name_inventory_excel = 'Inventory_data.xlsx'
file_name_inventory = 'inventory_data.csv'
file_name_assumptions_excel = 'Assumptions_data.xlsx'
file_name_assumptions = 'Assumptions_data.csv'
backup_file_name = 'inventory_data_backup.xlsx'

# Get the current timestamp
current_time = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
# Create a new file name with timestamp
output_file_name = f'output_data_{current_time}.csv'

def check_files_exist(directory_path, file_names):
    """
    Check if all specified files exist in the given directory.

    Args:
    - directory_path (str): Path to the directory where files are expected.
    - file_names (list): List of file names to check for existence.

    Returns:
    - bool: True if all files exist, False otherwise.
    """
    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            print(f"File '{file_name}' not found in directory '{directory_path}'.")
            return False
    return True

def get_user_directives():
    """
    Get user directives for directory paths and file operations.

    Returns:
    - dict: A dictionary containing the user's choices for directory paths.
    """
    # Check if the directive file exists
    if os.path.exists(directory_file_path):
        # Read the user's choices from the file
        with open(directory_file_path, 'r') as file:
            config = json.load(file)
    else:
        # Create a Tkinter root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the main window

        # Function to open directory dialog and return selected path
        def open_directory_dialog():
            return filedialog.askdirectory()

        # Prompt the user to select directories using dialog windows
        directory_path_inventory = open_directory_dialog()

        # Check if required files exist in the inventory directory
        if not check_files_exist(directory_path_inventory, [file_name_inventory_excel, file_name_inventory]):
            raise FileNotFoundError("Required files not found in the inventory directory. Please check and retry.")

        # Assign assumptions directory as the same as inventory for simplicity
        directory_path_assumptions = directory_path_inventory

        # Define backup and output directories based on inventory directory
        backup_directory = os.path.join(directory_path_inventory, 'Backup')
        output_directory = os.path.join(directory_path_inventory, 'Output')

        # Save the user's choices to the file
        config = {
            'directory_path_inventory': directory_path_inventory,
            'directory_path_assumptions': directory_path_assumptions,
            'backup_directory': backup_directory,
            'output_directory': output_directory
        }

        with open(directory_file_path, 'w') as file:
            json.dump(config, file, indent=4)

    return config

try:
    # Get the user's directives
    config = get_user_directives()

    # Use the directives in your code
    directory_path_inventory = config['directory_path_inventory']
    directory_path_assumptions = config['directory_path_assumptions']
    backup_directory = config['backup_directory']
    output_directory = config['output_directory']

    # Use the check_files_exist function to verify assumptions directory files
    if not check_files_exist(directory_path_assumptions, [file_name_assumptions_excel, file_name_assumptions]):
        raise FileNotFoundError("Required files not found in the assumptions directory. Please check and retry.")

    # Proceed with your code execution
    print("All required files found. Proceeding with execution...")

except FileNotFoundError as e:
    print(f"Error: {e}")
    # Handle the error as needed, e.g., exit the program or prompt the user
    # to correct the directories/files.

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@ INTIAL BACKUP CHECK @@@@@@@@@@@ INTIAL BACKUP CHECK @@@@@@@@@@@ INTIAL BACKUP CHECK @@@@@@@@@@@ INTIAL BAC
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def find_indices(matrix, target):
    """
    Find the indices of all occurrences of a target value in a 2D matrix.

    This function iterates through each element in a 2D matrix and returns a list of tuples,
    each containing the row and column indices where the target value is found.

    Parameters:
    matrix (list of list of int/float/str): The 2D matrix to search through.
    target (int/float/str): The value to find in the matrix.

    Returns:
    list of tuple: A list of tuples, where each tuple contains the row index and column index
    of an occurrence of the target value in the matrix.

    Example:
    >>> matrix = [
    ...     [1, 2, 3],
    ...     [4, 5, 6],
    ...     [7, 8, 3]
    ... ]
    >>> find_indices(matrix, 3)
    [(0, 2), (2, 2)]
    """
    indices = []
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            if value == target:
                indices.append((i, j))
    return indices

def Inventory_File_conflict():
    """
    Handle conflict between main and backup inventory files.
    """
    # Create the main window outside of if-else to avoid UnboundLocalError
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    result = messagebox.askyesno("Inventory File conflict",
                                 "There is a backup file in the backup folder. Do you wish to overwrite the active file (Main directory) with the backup?")
    if result:
        # Replace the main Excel file with the backup data
        shutil.copy(os.path.join(backup_directory, backup_file_name),
                    os.path.join(directory_path_inventory, file_name_inventory_excel))
        # Display a pop-up window with a message
        messagebox.showinfo("Inventory File conflict", "Main directory File overwriten by backup")
    else:
        # Display a pop-up window with a message
        messagebox.showinfo("Inventory File conflict", "Main directory File kept")

    # Destroy the tkinter main window in both branches
    root.destroy()


if os.path.exists(os.path.join(backup_directory, backup_file_name)):
    # Create the main window (you can skip this if your script is simple)
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    # Call the function to ask for confirmation
    Inventory_File_conflict()

    root.destroy()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@ File Reading @@@@@@@ File Reading @@@@@@@ File Reading @@@@@@@ File Reading @@@@@@@ File Reading @@@@@@@ File R
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Read the Excel files into separate DataFrames
df_inventory = pd.read_excel(os.path.join(directory_path_inventory, file_name_inventory_excel))
df_assumptions = pd.read_excel(os.path.join(directory_path_assumptions, file_name_assumptions_excel))

# Save the DataFrames to CSV files with semicolon as the separator
df_inventory.to_csv(os.path.join(directory_path_inventory, file_name_inventory), index=False, sep=';')
df_assumptions.to_csv(os.path.join(directory_path_assumptions, file_name_assumptions), index=False, sep=';')

# Create empty lists to store the CSV data
inventory_data = []
assumptions_data = []

# Open and read the inventory CSV file
with open(os.path.join(directory_path_inventory, file_name_inventory), 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    for row in csvreader:
        inventory_data.append(row)

# Convert each element to float in the inventory_data list (excluding the first column)
for i in range(len(inventory_data)):
    for j in range(0, len(inventory_data[i])):  # Start from the second column
        try:
            # Try converting to float directly
            inventory_data[i][j] = float(inventory_data[i][j])
        except ValueError:
            try:
                # If the direct conversion fails, replace ',' with '.' and then convert to float
                inventory_data[i][j] = float(inventory_data[i][j].replace(',', '.'))
            except ValueError:
                pass  # If both conversion attempts fail, leave the value as is

# Open and read the inventory CSV file
with open(os.path.join(directory_path_assumptions, file_name_assumptions), 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    for row in csvreader:
        assumptions_data.append(row)

# Convert each element to float in the inventory_data list (excluding the first column)
for i in range(len(assumptions_data)):
    for j in range(0, len(assumptions_data[i])):  # Start from the second column
        try:
            # Try converting to float directly
            assumptions_data[i][j] = float(assumptions_data[i][j])
        except ValueError:
            try:
                # If the direct conversion fails, replace ',' with '.' and then convert to float
                assumptions_data[i][j] = float(assumptions_data[i][j].replace(',', '.'))
            except ValueError:
                pass  # If both conversion attempts fail, leave the value as is

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@ check 1 @@@@@@@@@@@@ check 1 @@@@@@@@@@@@ check 1 @@@@@@@@@@@@@ check 1 @@@@@@@@@@@ check 1 @@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
mass_percentage_MSW = []
percentage_total_MSW = 0
mass_total_MSW = 0
mass_MSW = []

for i in range(find_indices(inventory_data, 'A1')[0][0], find_indices(inventory_data, 'AT1')[0][0]):
    percentage_total_MSW += inventory_data[i][find_indices(inventory_data, 'Mass %')[0][1]]
    mass_total_MSW += inventory_data[i][find_indices(inventory_data, 'Mass (t)')[0][1]]
    mass_percentage_MSW.append(inventory_data[i][find_indices(inventory_data, 'Mass %')[0][1]])
    mass_MSW.append(inventory_data[i][find_indices(inventory_data, 'Mass (t)')[0][1]])

print('-------------')
if percentage_total_MSW == 100 and round(mass_total_MSW, 3) == round(inventory_data[1][0], 3):
    print('Check 1A done')
elif percentage_total_MSW != 100 and round(mass_total_MSW, 3) == round(inventory_data[1][0], 3):
    print('MSW percentage sum is not 100% =>' + str(percentage_total_MSW))
    sys.exit("Stopping execution. Failed Check 1A")
else:
    print('MSW mass sum does not match total mass')
    sys.exit("Stopping execution. Failed Check 1A")

mass_percentage_SCW = []
percentage_total_SCW = 0
mass_total_SCW = 0
mass_SCW = []

for i in range(find_indices(inventory_data, 'B1')[0][0], find_indices(inventory_data, 'BT1')[0][0]):
    percentage_total_SCW += inventory_data[i][find_indices(inventory_data, 'Mass %')[1][1]]
    mass_total_SCW += inventory_data[i][find_indices(inventory_data, 'Mass (t)')[1][1]]
    mass_percentage_SCW.append(inventory_data[i][find_indices(inventory_data, 'Mass %')[1][1]])
    mass_SCW.append(inventory_data[i][find_indices(inventory_data, 'Mass (t)')[1][1]])

print()
if percentage_total_SCW == 100 and round(mass_total_SCW, 3) == round(
        inventory_data[find_indices(inventory_data, 'Sep. Collected Waste total mass (t)')[0][0] + 1][0], 3):
    print('Check 1B done')
elif percentage_total_SCW != 100 and round(mass_total_SCW, 3) == round(inventory_data[47][0], 3):
    print('SCW percentage sum is not 100% =>' + str(percentage_total_SCW))
    sys.exit("Stopping execution. Failed Check 1B")
else:
    print('SCW mass sum does not match total mass')
    sys.exit("Stopping execution. Failed Check 1B")

print('-------------')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@DATA RELOAD@@@@@@@@@DATA RELOAD@@@@@@@@@DATA RELOAD@@@@@@@@@DATA RELOAD@@@@@@@@@DATA RELOAD@@@@@@@@@DATA RELO
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
inventory_data = []
assumptions_data = []

# Open and read the inventory CSV file
with open(os.path.join(directory_path_inventory, file_name_inventory), 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    for row in csvreader:
        inventory_data.append(row)

# Convert each element to float in the inventory_data list (excluding the first column)
for i in range(len(inventory_data)):
    for j in range(0, len(inventory_data[i])):  # Start from the second column
        try:
            # Try converting to float directly
            inventory_data[i][j] = float(inventory_data[i][j])
        except ValueError:
            try:
                # If the direct conversion fails, replace ',' with '.' and then convert to float
                inventory_data[i][j] = float(inventory_data[i][j].replace(',', '.'))
            except ValueError:
                pass  # If both conversion attempts fail, leave the value as is

# Open and read the inventory CSV file
with open(os.path.join(directory_path_assumptions, file_name_assumptions), 'r') as file:
    csvreader = csv.reader(file, delimiter=';')
    for row in csvreader:
        assumptions_data.append(row)

# Convert each element to float in the inventory_data list (excluding the first column)
for i in range(len(assumptions_data)):
    for j in range(0, len(assumptions_data[i])):  # Start from the second column
        try:
            # Try converting to float directly
            assumptions_data[i][j] = float(assumptions_data[i][j])
        except ValueError:
            try:
                # If the direct conversion fails, replace ',' with '.' and then convert to float
                assumptions_data[i][j] = float(assumptions_data[i][j].replace(',', '.'))
            except ValueError:
                pass  # If both conversion attempts fail, leave the value as is

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@ check 1.1 @@@@@@@@@@@@ check 1.1 @@@@@@@@@@@@ check 1.1 @@@@@@@@@@@@@ check 1.1 @@@@@@@@@@@ check 1.1 @@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

percentage_total_MSW = 0
mass_MSW = []

for i in range(find_indices(inventory_data, 'A1')[0][0], find_indices(inventory_data, 'AT1')[0][0]):
    percentage_total_MSW += inventory_data[i][find_indices(inventory_data, 'Mass %')[0][1]]
    mass_MSW.append(inventory_data[i][find_indices(inventory_data, 'Mass (t)')[0][1]])

if percentage_total_MSW == 100 and round(mass_total_MSW, 3) == round(inventory_data[1][0], 3):
    print('Check 2 done')
elif percentage_total_MSW != 100 and round(mass_total_MSW, 3) == round(inventory_data[1][0], 3):
    print('MSW percentage sum is not 100% =>' + str(percentage_total_MSW))
    sys.exit("Stopping execution. Failed Check 2")
else:
    print('MSW mass sum does not match total mass')
    sys.exit("Stopping execution. Failed Check 2")

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@ data acquisition @@@@@@@@@@ data acquisition @@@@@@@@@@ data acquisition @@@@@@@@@@ data acquisition @@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
category_names_MSW = []
category_names_SCW = []
for i in range((find_indices(inventory_data, 'A1')[0][0]), (find_indices(inventory_data, 'A9')[0][0]) + 1):
    category_names_MSW.append(inventory_data[i][(find_indices(inventory_data, 'Category')[0][1])])

for i in range((find_indices(inventory_data, 'B1')[0][0]), (find_indices(inventory_data, 'B9')[0][0]) + 1):
    category_names_SCW.append(inventory_data[i][(find_indices(inventory_data, 'Category')[1][1])])

total_energy = inventory_data[find_indices(inventory_data, 'AT1')[0][0]][
    find_indices(inventory_data, 'Total energy contribuition (MJ/Kg)')[0][1]]

INC_energy = []
for i in range((find_indices(inventory_data, 'A1')[0][0]), (find_indices(inventory_data, 'AT1')[0][0])):
    INC_energy.append(inventory_data[i][(find_indices(inventory_data, 'Energy(MJ/Kg)')[0][1])])

mass_matrix_MSW = []
mass_matrix_SCW = []

for i in range((find_indices(inventory_data, 'Mixed waste to MBT, composting (t)')[0][0]) + 1,
               (find_indices(inventory_data, 'Mixed waste to MBT, composting (t)')[0][0]) + len(mass_MSW) + 1):
    row = []
    for j in range((find_indices(inventory_data, 'Mixed waste to MBT, composting (t)')[0][1]),
                   (find_indices(inventory_data, 'Mixed waste to Gasification (t)')[0][1]) + 1):
        row.append(inventory_data[i][j])

    mass_matrix_MSW.append(row)

for i in range((find_indices(inventory_data, 'S.C. waste to MBT, Gasification (t)')[0][0]) + 1,
               (find_indices(inventory_data, 'S.C. waste to MBT, Gasification (t)')[0][0]) + len(mass_SCW) + 1):
    row = []
    for j in range((find_indices(inventory_data, 'S.C. waste to MBT, Gasification (t)')[0][1]),
                   (find_indices(inventory_data, 'S.C. waste to MBT, Recycling (t)')[0][1]) + 1):
        row.append(inventory_data[i][j])

    mass_matrix_SCW.append(row)

column_sums_mass_matrix_MSW = [sum(column) for column in zip(*mass_matrix_MSW)]

table1_assumptions = []
for i in range((find_indices(assumptions_data, 'MSW component')[0][0] + 2),
               (find_indices(assumptions_data, 'Table 2.1: METHANE CORRECTION FACTORS (MCF)')[0][0]) - 3 + 1):
    row = []
    for j in range((find_indices(assumptions_data, 'Dry matter content in % of wet weight')[0][1]),
                   (find_indices(assumptions_data, 'Fossil carbon fraction in % of total carbon')[0][1]) + 2 + 1):
        # Check if the entry is a float, if not, assume it's 0
        entry = assumptions_data[i][j]
        if isinstance(entry, float):
            row.append(entry)
        else:
            row.append(0.0)  # Assuming it's 0 if not a float
    table1_assumptions.append(row)

table21_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 2.1: METHANE CORRECTION FACTORS (MCF)')[0][0] + 2),
               (find_indices(assumptions_data, 'Table 3: RECOMMENDED DEFAULT HALF-LIFE VALUES (YR)')[0][0]) - 2 + 1):
    table21_assumptions.append(assumptions_data[i][(find_indices(assumptions_data,
                                                                 'Table 2.1: METHANE CORRECTION FACTORS (MCF)')[0][
        1]) + 1])

table22_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 2.2: Oxidation Factor (OX)')[0][0] + 2),
               (find_indices(assumptions_data, 'Table 2.2: Oxidation Factor (OX)')[0][0]) + 3 + 1):
    table22_assumptions.append(
        assumptions_data[i][(find_indices(assumptions_data, 'Table 2.2: Oxidation Factor (OX)')[0][1]) + 1])

table23_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 2.3: Correction factor for greenhouse gases (CO2eq)')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 2.3: Correction factor for greenhouse gases (CO2eq)')[0][0]) + 3):
    table23_assumptions.append(
        assumptions_data[i][
            (find_indices(assumptions_data, 'Table 2.3: Correction factor for greenhouse gases (CO2eq)')[0][1]) + 1])

table3_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 3: RECOMMENDED DEFAULT HALF-LIFE VALUES (YR)')[0][0] + 4),
               (find_indices(assumptions_data, 'Table 4: GHG emission factors for waste collection and transport')[0][
                   0]) - 2 + 1):
    row = []
    for j in range((find_indices(assumptions_data, 'Table 3: RECOMMENDED DEFAULT HALF-LIFE VALUES (YR)')[0][1] + 1),
                   (find_indices(assumptions_data, 'Table 3: RECOMMENDED DEFAULT HALF-LIFE VALUES (YR)')[0][
                       1]) + 12 + 1):
        row.append(assumptions_data[i][j])
    table3_assumptions.append(row)

table4_assumptions = []
for i in range(
        (find_indices(assumptions_data, 'Table 4: GHG emission factors for waste collection and transport')[0][0] + 1),
        (find_indices(assumptions_data, 'Table 5: Composting Parameters (MSW)')[0][0]) - 2 + 1):
    table4_assumptions.append(assumptions_data[i][(find_indices(assumptions_data,
                                                                'Table 4: GHG emission factors for waste collection and transport')[
        0][1]) + 2])

table5_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 5: Composting Parameters (MSW)')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 6: Anaerobic Digestion Parameters (MSW)')[0][0]) - 2 + 1):
    table5_assumptions.append(
        (assumptions_data[i][(find_indices(assumptions_data, 'Table 5: Composting Parameters (MSW)')[0][1] + 1)]))

table51_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 5.1: Composting Parameters (SCW)')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 6.1: Anaerobic Digestion Parameters (SCW)')[0][0]) - 2 + 1):
    table51_assumptions.append(
        (assumptions_data[i][(find_indices(assumptions_data, 'Table 5.1: Composting Parameters (SCW)')[0][1] + 1)]))

table6_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 6: Anaerobic Digestion Parameters (MSW)')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 7: Incineration Parameters')[0][0]) - 2 + 1):
    table6_assumptions.append(
        (assumptions_data[i][
            (find_indices(assumptions_data, 'Table 6: Anaerobic Digestion Parameters (MSW)')[0][1] + 1)]))

table61_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 6.1: Anaerobic Digestion Parameters (SCW)')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 7: Incineration Parameters')[0][0]) - 2 + 1):
    table61_assumptions.append(
        (assumptions_data[i][
            (find_indices(assumptions_data, 'Table 6.1: Anaerobic Digestion Parameters (SCW)')[0][1] + 1)]))

table7_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 7: Incineration Parameters')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 8: Landfill Parameters')[0][0]) - 2 + 1):
    table7_assumptions.append(
        (assumptions_data[i][(find_indices(assumptions_data, 'Table 7: Incineration Parameters')[0][1] + 1)]))

table71_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 7.1: CH4 EMISSION FACTORS FOR INCINERATION OF MSW')[0][0] + 2),
               (find_indices(assumptions_data, 'Table 7.1: CH4 EMISSION FACTORS FOR INCINERATION OF MSW')[0][
                    0] + 4 + 1)):
    table71_assumptions.append(
        (assumptions_data[i][
            (find_indices(assumptions_data, 'Table 7.1: CH4 EMISSION FACTORS FOR INCINERATION OF MSW')[0][1] + 2)]))

table72_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 7.2: N2O EMISSION FACTORS FOR INCINERATION OF MSW')[0][0] + 2),
               (find_indices(assumptions_data, 'Table 7.2: N2O EMISSION FACTORS FOR INCINERATION OF MSW')[0][
                    0] + 4 + 1)):
    table72_assumptions.append(
        (assumptions_data[i][
            (find_indices(assumptions_data, 'Table 7.2: N2O EMISSION FACTORS FOR INCINERATION OF MSW')[0][1] + 2)]))

table8_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 8: Landfill Parameters')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 9: Gasification Parameters')[0][0]) - 2 + 1):
    table8_assumptions.append(
        (assumptions_data[i][(find_indices(assumptions_data, 'Table 8: Landfill Parameters')[0][1] + 1)]))

table9_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 9: Gasification Parameters')[0][0] + 1),
               (find_indices(assumptions_data, 'Table 10: Recycling Parameters')[0][0]) - 2 + 1):
    table9_assumptions.append(
        (assumptions_data[i][(find_indices(assumptions_data, 'Table 9: Gasification Parameters')[0][1] + 1)]))

table10_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 10: Recycling Parameters')[0][0] + 2),
               (find_indices(assumptions_data, 'Table 11: DOC contents (SCW)')[0][0]) - 2 + 1):
    row = []
    for j in range((find_indices(assumptions_data, 'Table 10: Recycling Parameters')[0][1] + 1),
                   (find_indices(assumptions_data,
                                 'Emission factors for waste collection and transport (t CO2(eq)/t recycled material)')[
                       0][
                       1]) + 1):
        entry = assumptions_data[i][j]
        if isinstance(entry, float):
            row.append(entry)
        else:
            row.append(0.0)  # Assuming it's 0 if not a float
    table10_assumptions.append(row)

table11_assumptions = []
for i in range((find_indices(assumptions_data, 'Table 11: DOC contents (SCW)')[0][0] + 3),
               (find_indices(assumptions_data, 'Biowaste (Garden and Park waste)')[-1][0]) + 1):
    row = []
    for j in range((find_indices(assumptions_data, 'Dry matter content in % of wet weight')[1][1]),
                   (find_indices(assumptions_data, 'Fossil carbon fraction in % of total carbon')[1][1]) + 2 + 1):
        # Check if the entry is a float, if not, assume it's 0
        entry = assumptions_data[i][j]
        if isinstance(entry, float):
            row.append(entry)
        else:
            row.append(0.0)  # Assuming it's 0 if not a float
    table11_assumptions.append(row)

# Calculate Mass dry basis matrix
Mass_dry_MSW = []
for i in range(len(table1_assumptions)):
    row = []
    for value in mass_matrix_MSW[i]:
        row.append(value * table1_assumptions[i][0] / 100)
    Mass_dry_MSW.append(row)

Mass_dry_SCW = []
for i in range(len(table11_assumptions)):
    row = []
    for value in mass_matrix_SCW[i]:
        row.append(value * table11_assumptions[i][0] / 100)
    Mass_dry_SCW.append(row)

print('------------------Data loaded successfully---------------------------------------------------------------------')
print()

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@ Recycling @@@@@@@@@@ Recycling @@@@@@@@@@ Recycling @@@@@@@@@@ Recycling @@@@@@@@@@ Recycling @@@@@@@@@@ Re
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

mass_list_recycling = []
for i in range(len(mass_matrix_SCW)):
    mass_list_recycling.append(mass_matrix_SCW[i][len(mass_matrix_SCW[0]) - 1])

recycling_emissions = []  # ton of CO2 eq
recycling_material_recovery = []  # ton of recovered material
recycling_energy_consumption = []  # MJ
for i in range(len(mass_matrix_SCW)):
    recycling_emissions.append(mass_list_recycling[i] * (table10_assumptions[i][0] + table10_assumptions[i][3]))
    recycling_material_recovery.append(mass_list_recycling[i] * table10_assumptions[i][1])
    recycling_energy_consumption.append(mass_list_recycling[i] * table10_assumptions[i][2])

# Results --------------------------------------------------------------------------------------------------------------
print()
print('--------------------Recycling Results--------------------------------------------------------------------------')
for i in range(len(category_names_SCW)):
    print(str(category_names_SCW[i]) + ': ' + str(
        round(recycling_emissions[i], 3)) + ' Tons of CO2 eq. emitted / / ' + str(
        round(recycling_material_recovery[i], 3)) + ' Tons of material recovered / / ' + str(
        round(recycling_energy_consumption[i], 3)) + ' MJ spent')
print('Overall Total: ' + str(round(sum(recycling_emissions), 3)) + ' Tons of CO2 eq. emitted / / ' + str(
    round(sum(recycling_material_recovery), 3)) + ' Tons of material recovered / / ' + str(
    round(sum(recycling_energy_consumption), 3)) + ' MJ spent')
print('---------------------------------------------------------------------------------------------------------------')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@Composting Mixed@@@@@@@@@@Composting Mixed@@@@@@@@@@Composting Mixed@@@@@@@@@@Composting Mixed@@@@@@@@@@Comp
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# -----------------------------------------------------------------------------------------------------------------------
# MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION-----

# Calculate Comp_mass_MSW; Comp_DOCi_Wi_MSW; DOCi_Wi_min and DOCi_Wi_max
Comp_mass_MSW = 0  # tons of wet waste
Comp_compost_mass_MSW = []
Comp_compost_mass_min_MSW = []
Comp_compost_mass_max_MSW = []
Comp_DOCi_Wi_MSW = []  # tons of degradable Carbon
Comp_DOCi_Wi_min_MSW = []  # tons of degradable Carbon
Comp_DOCi_Wi_max_MSW = []  # tons of degradable Carbon
for i in range(len(table1_assumptions)):
    k = Mass_dry_MSW[i][0] * table1_assumptions[i][4] / 100
    k_min = Mass_dry_MSW[i][0] * table1_assumptions[i][5] / 100
    k_max = Mass_dry_MSW[i][0] * table1_assumptions[i][6] / 100
    l = Mass_dry_MSW[i][0] * (1 - table1_assumptions[i][4] / 100)
    l_max = Mass_dry_MSW[i][0] * (1 - table1_assumptions[i][5] / 100)
    l_min = Mass_dry_MSW[i][0] * (1 - table1_assumptions[i][6] / 100)
    Comp_mass_MSW += mass_matrix_MSW[i][0]
    Comp_DOCi_Wi_MSW.append(k)
    Comp_DOCi_Wi_min_MSW.append(k_min)
    Comp_DOCi_Wi_max_MSW.append(k_max)
    Comp_compost_mass_MSW.append(l)
    Comp_compost_mass_min_MSW.append(l_min)
    Comp_compost_mass_max_MSW.append(l_max)

# Transport emissions
Comp_transp_emissions_MSW = Comp_mass_MSW * table4_assumptions[6]  # tons of CO2 eq.

Comp_CO2_eq_MSW = []  # tons of CO2 eq.
Comp_CO2_eq_min_MSW = []  # tons of CO2 eq.
Comp_CO2_eq_max_MSW = []  # tons of CO2 eq.
for i in range(len(Comp_DOCi_Wi_MSW)):
    Comp_DDOCm_CH4 = Comp_DOCi_Wi_MSW[i] * table5_assumptions[0] * table5_assumptions[
        1]  # tons of degradable Carbon that can become CH4
    Comp_DDOCm_CH4_min = Comp_DOCi_Wi_min_MSW[i] * table5_assumptions[0] * table5_assumptions[
        1]  # tons of degradable Carbon that can become CH4
    Comp_DDOCm_CH4_max = Comp_DOCi_Wi_max_MSW[i] * table5_assumptions[0] * table5_assumptions[
        1]  # tons of degradable Carbon that can become CH4

    # It is assumed that the carbon that can become CH4 becomes that and the rest becomes C02
    Comp_DDOCm_CO2 = (Comp_DOCi_Wi_MSW[i] - Comp_DDOCm_CH4) * (
            1 - table5_assumptions[1])  # tons of degradable Carbon that can become CO2
    Comp_DDOCm_CO2_min = (Comp_DOCi_Wi_min_MSW[i] - Comp_DDOCm_CH4_min) * (
            1 - table5_assumptions[1])  # tons of degradable Carbon that can become CO2
    Comp_DDOCm_CO2_max = (Comp_DOCi_Wi_max_MSW[i] - Comp_DDOCm_CH4_max) * (
            1 - table5_assumptions[1])  # tons of degradable Carbon that can become CO2

    # CH4 potencial = DDOC_CH4 * CH4/C * F * (1 - OX)
    Comp_CH4_generation_potencial = Comp_DDOCm_CH4 * table5_assumptions[3] * table5_assumptions[5] * (
            1 - table5_assumptions[4])  # tons of CH4
    Comp_CH4_generation_potencial_min = Comp_DDOCm_CH4_min * table5_assumptions[3] * table5_assumptions[5] * (
            1 - table5_assumptions[4])  # tons of CH4
    Comp_CH4_generation_potencial_max = Comp_DDOCm_CH4_max * table5_assumptions[3] * table5_assumptions[5] * (
            1 - table5_assumptions[4])  # tons of CH4

    Comp_CO2_generation_potencial = Comp_DDOCm_CO2 * table5_assumptions[2]  # tons of C02
    Comp_CO2_generation_potencial_min = Comp_DDOCm_CO2_min * table5_assumptions[2]  # tons of C02
    Comp_CO2_generation_potencial_max = Comp_DDOCm_CO2_max * table5_assumptions[2]  # tons of C02

    Comp_CO2_eq_MSW.append(Comp_CO2_generation_potencial + Comp_CH4_generation_potencial * table23_assumptions[0])
    Comp_CO2_eq_min_MSW.append(
        Comp_CO2_generation_potencial_min + Comp_CH4_generation_potencial_min * table23_assumptions[0])
    Comp_CO2_eq_max_MSW.append(
        Comp_CO2_generation_potencial_max + Comp_CH4_generation_potencial_max * table23_assumptions[0])

# ----------------------------------------------------------------------------------------------------------------------
# SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION-----

# Calculate Comp_mass_MSW; Comp_DOCi_Wi_MSW; DOCi_Wi_min and DOCi_Wi_max
Comp_mass_SCW = 0  # tons of wet waste
Comp_compost_mass_SCW = []
Comp_compost_mass_min_SCW = []
Comp_compost_mass_max_SCW = []
Comp_DOCi_Wi_SCW = []  # tons of degradable Carbon
Comp_DOCi_Wi_min_SCW = []  # tons of degradable Carbon
Comp_DOCi_Wi_max_SCW = []  # tons of degradable Carbon
for i in range(len(table11_assumptions)):
    k = Mass_dry_SCW[i][1] * table11_assumptions[i][4] / 100
    k_min = Mass_dry_SCW[i][1] * table11_assumptions[i][5] / 100
    k_max = Mass_dry_SCW[i][1] * table11_assumptions[i][6] / 100
    l = Mass_dry_SCW[i][1] * (1 - table11_assumptions[i][4] / 100)
    l_max = Mass_dry_SCW[i][1] * (1 - table11_assumptions[i][5] / 100)
    l_min = Mass_dry_SCW[i][1] * (1 - table11_assumptions[i][6] / 100)
    Comp_mass_SCW += mass_matrix_SCW[i][1]
    Comp_DOCi_Wi_SCW.append(k)
    Comp_DOCi_Wi_min_SCW.append(k_min)
    Comp_DOCi_Wi_max_SCW.append(k_max)
    Comp_compost_mass_SCW.append(l)
    Comp_compost_mass_min_SCW.append(l_min)
    Comp_compost_mass_max_SCW.append(l_max)

# Transport emissions
Comp_transp_emissions_SCW = Comp_mass_SCW * table4_assumptions[4]  # tons of CO2 eq.

Comp_CO2_eq_SCW = []  # tons of CO2 eq.
Comp_CO2_eq_min_SCW = []  # tons of CO2 eq.
Comp_CO2_eq_max_SCW = []  # tons of CO2 eq.
for i in range(len(Comp_DOCi_Wi_SCW)):
    Comp_DDOCm_CH4 = Comp_DOCi_Wi_SCW[i] * table51_assumptions[0] * table51_assumptions[
        1]  # tons of degradable Carbon that can become CH4
    Comp_DDOCm_CH4_min = Comp_DOCi_Wi_min_SCW[i] * table51_assumptions[0] * table51_assumptions[
        1]  # tons of degradable Carbon that can become CH4
    Comp_DDOCm_CH4_max = Comp_DOCi_Wi_max_SCW[i] * table51_assumptions[0] * table51_assumptions[
        1]  # tons of degradable Carbon that can become CH4

    # It is assumed that the carbon that can become CH4 becomes that and the rest becomes C02
    Comp_DDOCm_CO2 = (Comp_DOCi_Wi_SCW[i] - Comp_DDOCm_CH4) * (
            1 - table51_assumptions[1])  # tons of degradable Carbon that can become CO2
    Comp_DDOCm_CO2_min = (Comp_DOCi_Wi_min_SCW[i] - Comp_DDOCm_CH4_min) * (
            1 - table51_assumptions[1])  # tons of degradable Carbon that can become CO2
    Comp_DDOCm_CO2_max = (Comp_DOCi_Wi_max_SCW[i] - Comp_DDOCm_CH4_max) * (
            1 - table51_assumptions[1])  # tons of degradable Carbon that can become CO2

    # CH4 potencial = DDOC_CH4 * CH4/C * F * (1 - OX)
    Comp_CH4_generation_potencial = Comp_DDOCm_CH4 * table51_assumptions[3] * table51_assumptions[5] * (
            1 - table51_assumptions[4])  # tons of CH4
    Comp_CH4_generation_potencial_min = Comp_DDOCm_CH4_min * table51_assumptions[3] * table51_assumptions[5] * (
            1 - table51_assumptions[4])  # tons of CH4
    Comp_CH4_generation_potencial_max = Comp_DDOCm_CH4_max * table51_assumptions[3] * table51_assumptions[5] * (
            1 - table51_assumptions[4])  # tons of CH4

    Comp_CO2_generation_potencial = Comp_DDOCm_CO2 * table51_assumptions[2]  # tons of C02
    Comp_CO2_generation_potencial_min = Comp_DDOCm_CO2_min * table51_assumptions[2]  # tons of C02
    Comp_CO2_generation_potencial_max = Comp_DDOCm_CO2_max * table51_assumptions[2]  # tons of C02

    Comp_CO2_eq_SCW.append(Comp_CO2_generation_potencial + Comp_CH4_generation_potencial * table23_assumptions[0])
    Comp_CO2_eq_min_SCW.append(
        Comp_CO2_generation_potencial_min + Comp_CH4_generation_potencial_min * table23_assumptions[0])
    Comp_CO2_eq_max_SCW.append(
        Comp_CO2_generation_potencial_max + Comp_CH4_generation_potencial_max * table23_assumptions[0])

print()
print('--------------------Composting Results-------------------------------------------------------------------------')
print('<MSW Results>')
for i in range(len(category_names_MSW)):
    print(str(category_names_MSW[i]) + ': ' + str(round(Comp_CO2_eq_MSW[i], 3)) + ' Tons of CO2 eq. / / ' + str(
        round(Comp_compost_mass_MSW[i], 3)) + ' Tons of Compost (db)')
print('Transport emissions: ' + str(round(Comp_transp_emissions_MSW, 3)) + ' Tons of CO2 eq.')
print()

print('<SCW Results>')
for i in range(len(category_names_SCW)):
    print(str(category_names_SCW[i]) + ': ' + str(round(Comp_CO2_eq_SCW[i], 3)) + ' Tons of CO2 eq. / / ' + str(
        round(Comp_compost_mass_SCW[i], 3)) + ' Tons of Compost (db)')
print('Transport emissions: ' + str(round(Comp_transp_emissions_SCW, 3)) + ' Tons of CO2 eq.')
print()

print('<Overall Results>')
print('GHG Emissions: ' + str(
    round(sum(Comp_CO2_eq_MSW) + sum(Comp_CO2_eq_SCW) + Comp_transp_emissions_MSW + Comp_transp_emissions_SCW,
          3)) + ' Tons of CO2 eq. // Min: ' + str(
    round(sum(Comp_CO2_eq_min_MSW) + sum(Comp_CO2_eq_min_SCW) + Comp_transp_emissions_MSW + Comp_transp_emissions_SCW,
          3)) + ' Tons of CO2 eq. // Max: ' + str(
    round(sum(Comp_CO2_eq_max_MSW) + sum(Comp_CO2_eq_max_SCW) + Comp_transp_emissions_MSW + Comp_transp_emissions_SCW,
          3)) + ' Tons of CO2 eq.')
print('Material recovery: ' + str(
    round(sum(Comp_compost_mass_MSW) + sum(Comp_compost_mass_SCW), 3)) + ' Tons of Compost (db) // Min: ' + str(
    round(sum(Comp_compost_mass_min_MSW) + sum(Comp_compost_mass_min_SCW), 3)) + ' Tons of Compost (db) // Max: ' + str(
    round(sum(Comp_compost_mass_max_MSW) + sum(Comp_compost_mass_max_SCW), 3)) + ' Tons of Compost (db)')
print('Energy recovery: Not Applicable')
print('---------------------------------------------------------------------------------------------------------------')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@AD Mixed@@@@@@@@@@AD Mixed@@@@@@@@@@AD Mixed@@@@@@@@@@AD Mixed@@@@@@@@@@AD Mixed@@@@@@@@@@AD Mixed@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# -----------------------------------------------------------------------------------------------------------------------
# MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION------MSW SECTION-----

# Calculations very similar to the composting segment
AD_DOCi_Wi_MSW = []
AD_DOCi_Wi_min_MSW = []
AD_DOCi_Wi_max_MSW = []
AD_mass_MSW = 0
AD_digestate_mass_MSW = []
AD_digestate_mass_min_MSW = []
AD_digestate_mass_max_MSW = []
for i in range(len(table1_assumptions)):
    k = Mass_dry_MSW[i][1] * table1_assumptions[i][4] / 100
    k_min = Mass_dry_MSW[i][1] * table1_assumptions[i][5] / 100
    k_max = Mass_dry_MSW[i][1] * table1_assumptions[i][6] / 100
    l = Mass_dry_MSW[i][1] * (1 - table1_assumptions[i][4] / 100)
    l_max = Mass_dry_MSW[i][1] * (1 - table1_assumptions[i][5] / 100)
    l_min = Mass_dry_MSW[i][1] * (1 - table1_assumptions[i][6] / 100)
    AD_mass_MSW += mass_matrix_MSW[i][1]
    AD_DOCi_Wi_MSW.append(k)
    AD_DOCi_Wi_min_MSW.append(k_min)
    AD_DOCi_Wi_max_MSW.append(k_max)
    AD_digestate_mass_MSW.append(l)
    AD_digestate_mass_min_MSW.append(l_min)
    AD_digestate_mass_max_MSW.append(l_max)
# transport emissions
AD_transp_emissions_MSW = AD_mass_MSW * table4_assumptions[6]

AD_CH4_recovered_MSW = []
AD_CH4_recovered_min_MSW = []
AD_CH4_recovered_max_MSW = []

AD_CO2_eq_MSW = []
AD_CO2_eq_min_MSW = []
AD_CO2_eq_max_MSW = []

for i in range(len(AD_DOCi_Wi_MSW)):
    AD_DDOCm_CH4 = AD_DOCi_Wi_MSW[i] * table6_assumptions[0] * table6_assumptions[1]
    AD_DDOCm_CH4_min = AD_DOCi_Wi_min_MSW[i] * table6_assumptions[0] * table6_assumptions[1]
    AD_DDOCm_CH4_max = AD_DOCi_Wi_max_MSW[i] * table6_assumptions[0] * table6_assumptions[1]

    AD_DDOCm_CO2 = (AD_DOCi_Wi_MSW[i] - AD_DDOCm_CH4) * (1 - table6_assumptions[1])
    AD_DDOCm_CO2_min = (AD_DOCi_Wi_min_MSW[i] - AD_DDOCm_CH4_min) * (1 - table6_assumptions[1])
    AD_DDOCm_CO2_max = (AD_DOCi_Wi_max_MSW[i] - AD_DDOCm_CH4_max) * (1 - table6_assumptions[1])

    # CH4 potencial = DDOC_CH4 * CH4/C * F * (1 - OX)
    AD_CH4_generation_potencial = AD_DDOCm_CH4 * table6_assumptions[3] * table6_assumptions[6] * (
            1 - table6_assumptions[4])
    AD_CH4_generation_potencial_min = AD_DDOCm_CH4_min * table6_assumptions[3] * table6_assumptions[6] * (
            1 - table6_assumptions[4])
    AD_CH4_generation_potencial_max = AD_DDOCm_CH4_max * table6_assumptions[3] * table6_assumptions[6] * (
            1 - table6_assumptions[4])

    AD_CO2_generation_potencial = AD_DDOCm_CO2 * table6_assumptions[2]
    AD_CO2_generation_potencial_min = AD_DDOCm_CO2_min * table6_assumptions[2]
    AD_CO2_generation_potencial_max = AD_DDOCm_CO2_max * table6_assumptions[2]

    # Recovery of CH4-------
    AD_CH4_recovered_MSW.append(AD_CH4_generation_potencial * table6_assumptions[5])
    AD_CH4_recovered_min_MSW.append(AD_CH4_generation_potencial_min * table6_assumptions[5])
    AD_CH4_recovered_max_MSW.append(AD_CH4_generation_potencial_max * table6_assumptions[5])

    AD_CO2_eq_MSW.append(AD_CO2_generation_potencial + (AD_CH4_generation_potencial - AD_CH4_recovered_MSW[i]) * \
                         table23_assumptions[0])
    AD_CO2_eq_min_MSW.append(
        AD_CO2_generation_potencial_min + (AD_CH4_generation_potencial_min - AD_CH4_recovered_min_MSW[i]) * \
        table23_assumptions[0])
    AD_CO2_eq_max_MSW.append(
        AD_CO2_generation_potencial_max + (AD_CH4_generation_potencial_max - AD_CH4_recovered_max_MSW[i]) * \
        table23_assumptions[0])

# ----------------------------------------------------------------------------------------------------------------------
# SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION------SCW SECTION-----

# Calculations very similar to the composting segment
AD_DOCi_Wi_SCW = []
AD_DOCi_Wi_min_SCW = []
AD_DOCi_Wi_max_SCW = []
AD_mass_SCW = 0
AD_digestate_mass_SCW = []
AD_digestate_mass_min_SCW = []
AD_digestate_mass_max_SCW = []
for i in range(len(table11_assumptions)):
    k = Mass_dry_SCW[i][2] * table11_assumptions[i][4] / 100
    k_min = Mass_dry_SCW[i][2] * table11_assumptions[i][5] / 100
    k_max = Mass_dry_SCW[i][2] * table11_assumptions[i][6] / 100
    l = Mass_dry_SCW[i][2] * (1 - table11_assumptions[i][4] / 100)
    l_max = Mass_dry_SCW[i][2] * (1 - table11_assumptions[i][5] / 100)
    l_min = Mass_dry_SCW[i][2] * (1 - table11_assumptions[i][6] / 100)
    AD_mass_SCW += mass_matrix_SCW[i][2]
    AD_DOCi_Wi_SCW.append(k)
    AD_DOCi_Wi_min_SCW.append(k_min)
    AD_DOCi_Wi_max_SCW.append(k_max)
    AD_digestate_mass_SCW.append(l)
    AD_digestate_mass_min_SCW.append(l_min)
    AD_digestate_mass_max_SCW.append(l_max)
# transport emissions
AD_transp_emissions_SCW = AD_mass_SCW * table4_assumptions[5]

AD_CH4_recovered_SCW = []
AD_CH4_recovered_min_SCW = []
AD_CH4_recovered_max_SCW = []

AD_CO2_eq_SCW = []
AD_CO2_eq_min_SCW = []
AD_CO2_eq_max_SCW = []

for i in range(len(AD_DOCi_Wi_SCW)):
    AD_DDOCm_CH4 = AD_DOCi_Wi_SCW[i] * table61_assumptions[0] * table61_assumptions[1]
    AD_DDOCm_CH4_min = AD_DOCi_Wi_min_SCW[i] * table61_assumptions[0] * table61_assumptions[1]
    AD_DDOCm_CH4_max = AD_DOCi_Wi_max_SCW[i] * table61_assumptions[0] * table61_assumptions[1]

    AD_DDOCm_CO2 = (AD_DOCi_Wi_SCW[i] - AD_DDOCm_CH4) * (1 - table61_assumptions[1])
    AD_DDOCm_CO2_min = (AD_DOCi_Wi_min_SCW[i] - AD_DDOCm_CH4_min) * (1 - table61_assumptions[1])
    AD_DDOCm_CO2_max = (AD_DOCi_Wi_max_SCW[i] - AD_DDOCm_CH4_max) * (1 - table61_assumptions[1])

    # CH4 potencial = DDOC_CH4 * CH4/C * F * (1 - OX)
    AD_CH4_generation_potencial = AD_DDOCm_CH4 * table61_assumptions[3] * table61_assumptions[6] * (
            1 - table61_assumptions[4])
    AD_CH4_generation_potencial_min = AD_DDOCm_CH4_min * table61_assumptions[3] * table61_assumptions[6] * (
            1 - table61_assumptions[4])
    AD_CH4_generation_potencial_max = AD_DDOCm_CH4_max * table61_assumptions[3] * table61_assumptions[6] * (
            1 - table61_assumptions[4])

    AD_CO2_generation_potencial = AD_DDOCm_CO2 * table61_assumptions[2]
    AD_CO2_generation_potencial_min = AD_DDOCm_CO2_min * table61_assumptions[2]
    AD_CO2_generation_potencial_max = AD_DDOCm_CO2_max * table61_assumptions[2]

    # Recovery of CH4-------
    AD_CH4_recovered_SCW.append(AD_CH4_generation_potencial * table61_assumptions[5])
    AD_CH4_recovered_min_SCW.append(AD_CH4_generation_potencial_min * table61_assumptions[5])
    AD_CH4_recovered_max_SCW.append(AD_CH4_generation_potencial_max * table61_assumptions[5])

    AD_CO2_eq_SCW.append(AD_CO2_generation_potencial + (AD_CH4_generation_potencial - AD_CH4_recovered_SCW[i]) * \
                         table23_assumptions[0])
    AD_CO2_eq_min_SCW.append(
        AD_CO2_generation_potencial_min + (AD_CH4_generation_potencial_min - AD_CH4_recovered_min_SCW[i]) * \
        table23_assumptions[0])
    AD_CO2_eq_max_SCW.append(
        AD_CO2_generation_potencial_max + (AD_CH4_generation_potencial_max - AD_CH4_recovered_max_SCW[i]) * \
        table23_assumptions[0])

print()
print('---------------Anaerobic Digestion Results---------------------------------------------------------------------')
print('<MSW Results>')
for i in range(len(category_names_MSW)):
    print(str(category_names_MSW[i]) + ': ' + str(round(AD_CO2_eq_MSW[i], 3)) + ' Tons of CO2 eq. / / ' + str(
        round(AD_digestate_mass_MSW[i], 3)) + ' Tons of Digestate (db) + ' + str(
        round(AD_CH4_recovered_MSW[i], 3)) + ' Tons of CH4 recovered')
print('Transport emissions: ' + str(round(AD_transp_emissions_MSW, 3)) + ' Tons of CO2 eq.')
print()

print('<SCW Results>')
for i in range(len(category_names_SCW)):
    print(str(category_names_SCW[i]) + ': ' + str(round(AD_CO2_eq_SCW[i], 3)) + ' Tons of CO2 eq. / / ' + str(
        round(AD_digestate_mass_SCW[i], 3)) + ' Tons of Digestate (db) + ' + str(
        round(AD_CH4_recovered_SCW[i], 3)) + ' Tons of CH4 recovered')
print('Transport emissions: ' + str(round(AD_transp_emissions_SCW, 3)) + ' Tons of CO2 eq.')
print()

print('<Overall Results>')
print('GHG Emissions: ' + str(
    round(sum(AD_CO2_eq_MSW) + sum(AD_CO2_eq_SCW) + AD_transp_emissions_MSW + AD_transp_emissions_SCW,
          3)) + ' Tons of CO2 eq. // Min: ' + str(
    round(sum(AD_CO2_eq_min_MSW) + sum(AD_CO2_eq_min_SCW) + AD_transp_emissions_MSW + AD_transp_emissions_SCW,
          3)) + ' Tons of CO2 eq. // Max: ' + str(
    round(sum(AD_CO2_eq_max_MSW) + sum(AD_CO2_eq_max_SCW) + AD_transp_emissions_MSW + AD_transp_emissions_SCW,
          3)) + ' Tons of CO2 eq.')
print('Material recovery: ' + str(
    round(sum(AD_digestate_mass_MSW) + sum(AD_digestate_mass_SCW), 3)) + ' Tons of digestate (db) + ' + str(
    round(sum(AD_CH4_recovered_MSW) + sum(AD_CH4_recovered_SCW), 3)) + ' Tons of CH4 recovered // Min: ' + str(
    round(sum(AD_digestate_mass_min_MSW) + sum(AD_digestate_mass_min_SCW), 3)) + ' Tons of digestate (db) + ' + str(
    round(sum(AD_CH4_recovered_min_MSW) + sum(AD_CH4_recovered_min_SCW), 3)) + ' Tons of CH4 recovered // Max: ' + str(
    round(sum(AD_digestate_mass_max_MSW) + sum(AD_digestate_mass_max_SCW), 3)) + ' Tons of digestate (db) + ' + str(
    round(sum(AD_CH4_recovered_max_MSW) + sum(AD_CH4_recovered_max_SCW), 3)) + ' Tons of CH4 recovered')
print('Energy recovery: Not Applicable')
print('---------------------------------------------------------------------------------------------------------------')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@Landfill@@@@@@@@@@Landfill@@@@@@@@@@Landfill@@@@@@@@@@Landfill@@@@@@@@@@Landfill@@@@@@@@@@Landfill@@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

# Calculations very similar to the composting and AD segments

LF_mass = 0
LF_DOCi_Wi = []
LF_DOCi_Wi_min = []
LF_DOCi_Wi_max = []
for i in range(len(table1_assumptions)):
    k = Mass_dry_MSW[i][3] * table1_assumptions[i][4] / 100
    k_min = Mass_dry_MSW[i][3] * table1_assumptions[i][5] / 100
    k_max = Mass_dry_MSW[i][3] * table1_assumptions[i][6] / 100
    LF_mass += mass_matrix_MSW[i][3]
    LF_DOCi_Wi.append(k)
    LF_DOCi_Wi_min.append(k_min)
    LF_DOCi_Wi_max.append(k_max)

LF_transp_emissions = LF_mass * table4_assumptions[8]

LF_CH4_recovered = []
LF_CH4_recovered_min = []
LF_CH4_recovered_max = []
LF_CO2_eq = []
LF_CO2_eq_min = []
LF_CO2_eq_max = []
for i in range(len(LF_DOCi_Wi)):
    LF_DDOCm_CH4 = LF_DOCi_Wi[i] * table8_assumptions[0] * table8_assumptions[1]
    LF_DDOCm_CH4_min = LF_DOCi_Wi_min[i] * table8_assumptions[0] * table8_assumptions[1]
    LF_DDOCm_CH4_max = LF_DOCi_Wi_max[i] * table8_assumptions[0] * table8_assumptions[1]

    LF_DDOCm_CO2 = (LF_DOCi_Wi[i] - LF_DDOCm_CH4) * (1 - table8_assumptions[1])
    LF_DDOCm_CO2_min = (LF_DOCi_Wi_min[i] - LF_DDOCm_CH4_min) * (1 - table8_assumptions[1])
    LF_DDOCm_CO2_max = (LF_DOCi_Wi_max[i] - LF_DDOCm_CH4_max) * (1 - table8_assumptions[1])

    # CH4 potencial = DDOC_CH4 * CH4/C * F * (1 - OX)
    LF_CH4_generation_potencial = LF_DDOCm_CH4 * table8_assumptions[3] * table8_assumptions[6] * (
            1 - table8_assumptions[4])
    LF_CH4_generation_potencial_min = LF_DDOCm_CH4_min * table8_assumptions[3] * table8_assumptions[6] * (
            1 - table8_assumptions[4])
    LF_CH4_generation_potencial_max = LF_DDOCm_CH4_max * table8_assumptions[3] * table8_assumptions[6] * (
            1 - table8_assumptions[4])

    LF_CO2_generation_potencial = LF_DDOCm_CO2 * table8_assumptions[2]
    LF_CO2_generation_potencial_min = LF_DDOCm_CO2_min * table8_assumptions[2]
    LF_CO2_generation_potencial_max = LF_DDOCm_CO2_max * table8_assumptions[2]

    # Recovery of CH4-------
    # CH4_recovered = CH4 potencial * R
    LF_CH4_recovered.append(LF_CH4_generation_potencial * table8_assumptions[5])
    LF_CH4_recovered_min.append(LF_CH4_generation_potencial_min * table8_assumptions[5])
    LF_CH4_recovered_max.append(LF_CH4_generation_potencial_max * table8_assumptions[5])

    # Flaring--------
    # CH4_flared = CH4 potencial * Flare efficiency * fraction flared
    LF_CH4_flaring = LF_CH4_generation_potencial * table8_assumptions[7] * table8_assumptions[8]
    LF_CH4_flaring_min = LF_CH4_generation_potencial_min * table8_assumptions[7] * table8_assumptions[8]
    LF_CH4_flaring_max = LF_CH4_generation_potencial_max * table8_assumptions[7] * table8_assumptions[8]

    # CH4 emissions --------
    LF_CH4_emissions = LF_CH4_generation_potencial - LF_CH4_recovered[i] - LF_CH4_flaring
    LF_CH4_emissions_min = LF_CH4_generation_potencial_min - LF_CH4_recovered_min[i] - LF_CH4_flaring_min
    LF_CH4_emissions_max = LF_CH4_generation_potencial_max - LF_CH4_recovered_max[i] - LF_CH4_flaring_max

    # CO2 emissions -------
    # CO2 emissions= CO2 potencial + CH4 flared * Conversion to CO2 ratio
    LF_CO2_emissions = LF_CO2_generation_potencial + LF_CH4_flaring * table8_assumptions[9]
    LF_CO2_emissions_min = LF_CO2_generation_potencial_min + LF_CH4_flaring_min * table8_assumptions[9]
    LF_CO2_emissions_max = LF_CO2_generation_potencial_max + LF_CH4_flaring_max * table8_assumptions[9]

    LF_CO2_eq.append(LF_CO2_emissions + LF_CH4_emissions * table23_assumptions[0])
    LF_CO2_eq_min.append(LF_CO2_emissions_min + LF_CH4_emissions_min * table23_assumptions[0])
    LF_CO2_eq_max.append(LF_CO2_emissions_max + LF_CH4_emissions_max * table23_assumptions[0])


# FIRST ORDER DECAY Model-----------------------------------------------------------------------------------------------
def open_analysis_window():
    """
    Create and display the FOD Analysis Landfill window with interactive widgets.

    This function creates a Tkinter window containing multiple widgets, such as labels, comboboxes,
    an entry field, and a confirm button. The window allows users to select options and input data
    related to landfill analysis, including waste presence, decomposition delay, and climate conditions.
    The confirm button remains disabled until all required fields are appropriately filled out.
    """

    def on_select_combobox1(event):
        """
        Handle selection event for the first combobox.

        This function is triggered when the user selects an option from the first combobox.
        If the selected option is 'Yes', it displays the entry label and entry widget for waste input.
        Otherwise, it hides these widgets. It also calls validate_fields to check if all required
        fields are filled.

        Parameters:
        event (tk.Event): The event object containing information about the selection event.
        """
        if combobox1.get() == 'Yes':
            entry_label.grid(row=3, column=0, padx=5, pady=5)  # Show entry label
            entry.grid(row=3, column=1, padx=5, pady=5)  # Show entry widget
        else:
            entry_label.grid_forget()  # Hide entry label
            entry.grid_forget()  # Hide entry widget
        validate_fields()  # Validate if all fields are filled

    def on_select_combobox2(event):
        """
        Handle selection event for the second combobox.

        This function is triggered when the user selects an option from the second combobox.
        It calls validate_fields to check if all required fields are filled.

        Parameters:
        event (tk.Event): The event object containing information about the selection event.
        """
        validate_fields()  # Validate if all fields are filled

    def on_select_climate(event):
        """
        Handle selection event for the climate comboboxes.

        This function is triggered when the user selects an option from either of the climate comboboxes.
        It enables the confirm button if both climate comboboxes have selections, otherwise it disables the button.

        Parameters:
        event (tk.Event): The event object containing information about the selection event.
        """
        if combobox3.get() and combobox4.get():  # Check if both comboboxes have selections
            confirm_button.config(state="normal")  # Enable confirm button if both comboboxes have selections
        else:
            confirm_button.config(
                state="disabled")  # Disable confirm button if either combobox doesn't have a selection

    def validate_fields():
        """
        Validate if all required fields are filled.

        This function checks if all comboboxes and the entry field (if applicable) are filled.
        It enables the confirm button if all fields are appropriately filled, otherwise it disables the button.
        It also calls adjust_window_size to adjust the window size based on widget visibility.
        """
        if combobox1.get() and combobox2.get() and combobox3.get() and combobox4.get():
            if combobox1.get() == 'Yes':
                if entry.get().strip():  # Check if entry is not empty
                    confirm_button.config(state="normal")  # Enable confirm button
                else:
                    confirm_button.config(state="disabled")  # Disable confirm button if entry is empty
            else:
                confirm_button.config(state="normal")  # Enable confirm button if all fields are filled
        else:
            confirm_button.config(state="disabled")  # Disable confirm button if any field is empty
        adjust_window_size()  # Adjust window size based on widget visibility

    def adjust_window_size():
        """
        Adjust the window size based on the visibility of widgets.

        This function updates the window size to fit all currently visible widgets,
        adding some padding for better layout.
        """
        root.update_idletasks()
        width = root.winfo_reqwidth() + 20  # Add some padding
        height = root.winfo_reqheight()
        root.geometry(f'{width}x{height}')

    def confirm_selection():
        """
        Handle the confirm button click event.

        This function retrieves the selected and entered data from the widgets,
        stores them in global variables, and closes the Tkinter window.
        """
        global FOD_data, Climate
        combo1 = combobox1.get()
        combo2 = combobox2.get()
        tons = entry.get().strip() if combo1 == 'Yes' else '0'
        FOD_data.clear()  # Clear existing data before adding new values
        FOD_data.extend([combo1, tons, combo2])

        region = combobox3.get()
        weather = combobox4.get()
        Climate.clear()  # Clear existing data before adding new values
        Climate.extend([region, weather])

        root.quit()  # Close the window
        root.destroy()

    # Create a Tkinter window
    root = tk.Tk()

    # Set the title of the window
    root.title("FOD Analysis Landfill")

    # Define the options for the first combobox
    options1 = ['Yes', 'No']

    # Define the options for the second combobox
    options2 = ["No Delay", "1 month", '2 months', '3 months', '4 months', '5 months']

    # Add labels for each combobox title
    title1 = ttk.Label(root, text='Is there any waste already on site?')
    title1.grid(row=1, column=0, padx=5, pady=5)
    title2 = ttk.Label(root, text="Delay before the decomposition starts:")
    title2.grid(row=1, column=1, padx=5, pady=5)

    # Create the first combobox widget
    combobox1 = ttk.Combobox(root, values=options1, state="readonly")
    combobox1.bind("<<ComboboxSelected>>", on_select_combobox1)  # Bind selection event

    # Create the second combobox widget
    combobox2 = ttk.Combobox(root, values=options2, state="readonly")
    combobox2.bind("<<ComboboxSelected>>", on_select_combobox2)  # Bind selection event

    # Create an entry widget for tons of waste
    entry_label = ttk.Label(root, text="Tons of waste:")
    entry = ttk.Entry(root)
    entry.bind("<KeyRelease>", lambda event: validate_fields())  # Bind key release event to validate entry

    # Create labels for the climate selection
    title3 = ttk.Label(root, text="Region:")
    title3.grid(row=4, column=0, padx=5, pady=5)
    title4 = ttk.Label(root, text="Weather:")
    title4.grid(row=4, column=1, padx=5, pady=5)

    # Define the options for the third combobox
    options3 = ["Boreal and Temperate", "Tropical"]

    # Define the options for the fourth combobox
    options4 = ["Dry", "Wet"]

    # Create the third combobox widget
    combobox3 = ttk.Combobox(root, values=options3, state="readonly")
    combobox3.bind("<<ComboboxSelected>>", on_select_climate)  # Bind selection event

    # Create the fourth combobox widget
    combobox4 = ttk.Combobox(root, values=options4, state="readonly")
    combobox4.bind("<<ComboboxSelected>>", on_select_climate)  # Bind selection event

    # Create a confirm button
    confirm_button = ttk.Button(root, text="Confirm", command=confirm_selection, state="disabled")

    # Arrange the comboboxes, entry, and confirm button
    combobox1.grid(row=2, column=0, padx=5, pady=5)
    combobox2.grid(row=2, column=1, padx=5, pady=5)
    combobox3.grid(row=5, column=0, padx=5, pady=5)
    combobox4.grid(row=5, column=1, padx=5, pady=5)
    confirm_button.grid(row=6, columnspan=2, pady=10)

    # Adjust window size to fit all widgets
    adjust_window_size()

    # Run the Tkinter event loop
    root.mainloop()


def FOD_Landfill():
    """
    Display the First Order Decay (FOD) Landfill analysis window.

    This function initiates a dialog asking the user if they wish to perform a time-dependent analysis.
    If the user selects "yes," it opens the FOD analysis window for user input. Based on the user's
    selections, it retrieves and processes climate data, waste delay information, and waste deposit details.
    It allows for detailed input of waste categories and amounts through dynamically created sliders and entry fields.
    """
    global FOD_data, Climate, Delay, Reaction_rate_constant, slider_values, Flag_FOD

    result = messagebox.askquestion("Landfill: First Order Decay Model",
                                    "Do you wish to make a time dependent analysis?")
    if result == "yes":
        Flag_FOD = True
        open_analysis_window()
        # Now the values should be saved in FOD_data and Climate after the Tkinter window closes

        row = []
        if Climate[0] == 'Tropical':
            if Climate[1] == 'Dry':
                for i in range(0, len(table3_assumptions)):
                    for j in range(6, 8 + 1):
                        row.append(table3_assumptions[i][j])
                    Half_life.append(row)
                    row = []
            else:
                for i in range(0, len(table3_assumptions)):
                    for j in range(9, 11 + 1):
                        row.append(table3_assumptions[i][j])
                    Half_life.append(row)
                    row = []
        else:
            if Climate[0][1] == 'Dry':
                for i in range(0, len(table3_assumptions)):
                    for j in range(0, 2 + 1):
                        row.append(table3_assumptions[i][j])
                    Half_life.append(row)
                    row = []
            else:
                for i in range(0, len(table3_assumptions)):
                    for j in range(3, 5 + 1):
                        row.append(table3_assumptions[i][j])
                    Half_life.append(row)
                    row = []

        delay_mapping = {
            'No Delay': 0,
            '1 month': 1,
            '2 months': 2,
            '3 months': 3,
            '4 months': 4,
            '5 months': 5
        }

        Delay = delay_mapping.get(FOD_data[2], 0)

        def create_combobox():
            """
            Create a combobox widget for selecting the number of waste deposits.

            This function creates and returns a combobox widget allowing the user to select the
            number of waste deposits during the simulation. It also adds a label above the combobox.
            """
            combobox_label = tk.Label(window, text="How many waste deposits will be done during the simulation:")
            combobox_label.pack()

            combobox = ttk.Combobox(window, values=list(range(11)), state="readonly")
            combobox.current(0)
            combobox.pack()
            return combobox

        def create_sliders(num_sliders):
            """
            Create sliders for inputting waste data.

            This function dynamically creates sliders based on the number of waste deposits selected
            by the user. Each slider represents a different waste deposit, allowing for input of waste
            data such as total mass and category-specific percentages.

            Parameters:
            num_sliders (int): The number of sliders to create.
            """
            global sliders

            # Destroy any existing sliders and labels
            for widget in window.winfo_children():
                if isinstance(widget, tk.Frame):
                    widget.destroy()

            # Find the width of the widest label
            max_label_width = max(len(text) for text in slider_texts)

            # Create new sliders and store their values in a list
            sliders = []  # Reset sliders list
            for i in range(num_sliders):
                frame = tk.Frame(window)
                frame.pack(anchor="w", padx=10, pady=5)
                label = tk.Label(frame, text=slider_texts[i], width=max_label_width)
                label.pack(side="left")
                slider = tk.Scale(frame, from_=0, to=200, orient="horizontal", resolution=1,
                                  command=lambda value, idx=i: None)
                slider.pack(side="left", padx=5)
                add_button = ttk.Button(frame, text="Add data", command=lambda idx=i: open_data_entry_window(idx))
                add_button.pack(side="left")
                subtext_label = tk.Label(frame, text="Not loaded",
                                         fg="gray")  # Subtext label initially says "Not loaded"
                subtext_label.pack(side="left")
                sliders.append((slider, add_button, subtext_label))
                waste_data.append([])  # Initialize an empty list for each slider to store waste data

        def open_data_entry_window(slider_idx):
            """
            Open a data entry window for detailed waste category input.

            This function creates a new window allowing the user to input detailed waste category data
            for a specific slider (waste deposit). The user can input total mass and category-specific
            percentages, which must sum to 100%.

            Parameters:
            slider_idx (int): The index of the slider for which the data entry window is opened.
            """
            # Create new window for data entry
            data_entry_window = tk.Toplevel(window)
            data_entry_window.title("Waste Category Input")

            # Create a new label and entry field for total mass (dry basis)
            total_mass_label = tk.Label(data_entry_window, text="Total Mass (Dry Basis)")
            total_mass_label.grid(row=0, columnspan=2, padx=10, pady=5)
            total_mass_entry = tk.Entry(data_entry_window)
            total_mass_entry.grid(row=1, columnspan=2, padx=10, pady=5)

            # Create label for title
            title_label = tk.Label(data_entry_window, text="Fill with waste data", font=("Helvetica", 10))
            title_label.grid(row=2, columnspan=2, padx=10, pady=10)

            # Create labels and entry fields for each category
            categories = [
                "Paper/Cardboard", "Textiles", "Food waste", "Wood",
                "Garden and Park waste", "Rubber and Leather", "Plastics",
                "Metal", "Glass"
            ]
            entry_fields = []

            for idx, category in enumerate(categories):
                label = tk.Label(data_entry_window, text=category)
                label.grid(row=idx + 3, column=0, padx=10, pady=5)
                entry = tk.Entry(data_entry_window)
                entry.grid(row=idx + 3, column=1, padx=10, pady=5)
                entry.insert(tk.END, " %")  # Initial value with percentage symbol
                entry.bind('<Button-1>', on_click)  # Bind click event to entry field
                entry.bind('<Key>', on_key)  # Bind key event to entry field
                entry.bind('<FocusOut>', on_focus_out)  # Bind focus out event to entry field
                entry_fields.append(entry)

            def confirm_values():
                """
                Confirm and save the values entered in the data entry window.

                This function validates the input values for total mass and category-specific percentages.
                It checks that percentages sum to 100 and that all inputs are valid. If the inputs are valid,
                it saves the values and closes the data entry window. Otherwise, it displays an error message.
                """
                total_percentage = 0
                invalid_input = False

                # Clear previous waste data
                waste_data[slider_idx] = []

                # Get total mass value
                total_mass_val = total_mass_entry.get().strip()

                # Check if total mass value is empty or contains only percentage signs
                if total_mass_val == "" or total_mass_val == "%":
                    total_mass_val = "0"

                try:
                    total_mass = float(total_mass_val)  # Convert total mass value to float
                    if total_mass < 0:
                        invalid_input = True
                except ValueError:
                    invalid_input = True

                if invalid_input:
                    # Display error message if total mass is not a valid number or is negative
                    error_label.config(text="Error: Total mass must be a valid non-negative number")
                    return

                # Append total mass to waste_data list
                waste_data[slider_idx].append(total_mass)

                # Get values from entry fields and calculate total percentage
                for entry in entry_fields:
                    val = entry.get().strip()
                    if val == "" or val == "%":  # Check if entry is empty or contains only percentage signs
                        val = "0"
                    try:
                        percentage = float(val.rstrip('%'))  # Remove '%' symbol
                        if percentage < 0 or percentage > 100:
                            invalid_input = True
                            break
                        total_percentage += percentage
                        waste_data[slider_idx].append(percentage)
                    except ValueError:
                        invalid_input = True
                        break

                # Check if total percentage is 100 and there are no invalid inputs
                if total_percentage == 100 and not invalid_input:
                    # Update subtext label on the original window to "Loaded"
                    sliders[slider_idx][2].config(text="Loaded", fg="green")
                    # Close the window
                    data_entry_window.destroy()
                elif total_percentage == 0:  # Allow confirmation with no values entered
                    # Update subtext label on the original window to "Not loaded"
                    sliders[slider_idx][2].config(text="Not loaded", fg="gray")
                    data_entry_window.destroy()
                else:
                    # Display error message if percentages don't add up to 100 or there are invalid inputs
                    error_label.config(text="Error: Percentages must add up to 100 and be valid numbers")

            # Create confirm button
            confirm_button = tk.Button(data_entry_window, text="Confirm", command=confirm_values)
            confirm_button.grid(row=len(categories) + 4, columnspan=2, padx=10, pady=10)

            # Create error label
            error_label = tk.Label(data_entry_window, fg="red")
            error_label.grid(row=len(categories) + 5, columnspan=2, padx=10, pady=5)

        def on_click(event):
            """
            Handle click event on entry fields to clear default text.

            This function clears the default text (percentage symbol) when the user clicks on an entry field.

            Parameters:
            event: The event object containing information about the click event.
            """
            widget = event.widget
            widget.delete(0, tk.END)

        def on_key(event):
            """
            Handle key event on entry fields to manage percentage symbol input.

            This function manages the input of the percentage symbol in entry fields. It ensures
            that only valid inputs are accepted.

            Parameters:
            event: The event object containing information about the key event.
            """
            widget = event.widget
            current_val = widget.get().strip()
            if current_val == " %" and event.char != "%":
                widget.delete(0, tk.END)
            elif current_val == "" and event.char == "%":
                widget.insert(tk.END, " %")

        def on_focus_out(event):
            """
            Handle focus out event on entry fields to reset default text.

            This function resets the default text (percentage symbol) when the user leaves an entry field
            without entering any data.

            Parameters:
            event: The event object containing information about the focus out event.
            """
            widget = event.widget
            current_val = widget.get().strip()
            if current_val == "":
                widget.insert(tk.END, " %")

        def save_values():
            """
            Save the values from the sliders and waste data input.

            This function retrieves the values from the sliders and saves the waste data input by the user.
            It then closes the main FOD analysis window.
            """
            global slider_values
            slider_values = [slider.get() for slider, _, _ in sliders]
            # print("Slider values:", slider_values)
            # print("Waste data:", waste_data)
            window.destroy()  # Close the window after confirming
            window.quit()

        def selection_changed(event):
            """
            Update the number of sliders when the combobox selection changes.

            This function dynamically updates the number of sliders based on the user's selection
            in the combobox.

            Parameters:
            event: The event object containing information about the combobox selection change.
            """
            num_sliders = int(combobox.get())
            create_sliders(num_sliders)

        # Create the main window
        window = tk.Tk()
        window.title("FOD Analysis Landfill")

        # Create a Combobox
        combobox = create_combobox()

        # Create Confirm button
        confirm_button = ttk.Button(window, text="Confirm", command=save_values)

        # Update sliders if Combobox selection changes
        combobox.bind("<<ComboboxSelected>>", selection_changed)

        # Create initial sliders
        create_sliders(int(combobox.get()))

        # Pack Confirm button
        confirm_button.pack()

        # Run the GUI event loop
        window.mainloop()


sliders = []  # Define sliders as a global variable
slider_texts = ["Time between t0 to t1 (months)", "Time between t1 to t2 (months)", "Time between t2 to t3 (months)",
                "Time between t3 to t4 (months)",
                "Time between t4 to t5 (months)", "Time between t5 to t6 (months)", "Time between t6 to t7 (months)",
                "Time between t7 to t8 (months)",
                'Time between t8 to t9 (months)', 'Time between t9 to t10 (months)']  # Custom text for each slider

waste_data = []  # Define waste_data list to store waste data for each slider
FOD_data = []
Delay = 0
Climate = []
Half_life = []
slider_values = []
Flag_FOD = False

# Call the function to initiate the FOD landfill analysis
FOD_Landfill()

if Flag_FOD == True:
    Flag_FOD = False
    Reaction_rate_constant = [[0] * len(Half_life[0]) for _ in range(len(Half_life))]
    for i in range(len(Half_life)):
        for j in range(len(Half_life[0])):
            Reaction_rate_constant[i][j] = math.log(2) / Half_life[i][j]

    k_constant = []
    for j in range(len(Reaction_rate_constant[0])):
        row = [Reaction_rate_constant[0][j], Reaction_rate_constant[0][j], Reaction_rate_constant[3][j],
               Reaction_rate_constant[1][j], Reaction_rate_constant[2][j], Reaction_rate_constant[4][j],
               0, 0, 0]
        k_constant.append(row)

    FOD_waste_mass = []
    for i in range(len(waste_data)):
        row = []
        for j in range(1, len(waste_data[0])):
            row.append(waste_data[i][0] * waste_data[i][j] / 100)
        FOD_waste_mass.append(row)

    FOD_DOCi_Wi = []
    FOD_DOCi_Wi_min = []
    FOD_DOCi_Wi_max = []
    for i in range(len(FOD_waste_mass)):
        row = []
        row_min = []
        row_max = []
        for j in range(len(FOD_waste_mass[0])):
            row.append(FOD_waste_mass[i][j] * table1_assumptions[j][4] / 100)
            row_min.append(FOD_waste_mass[i][j] * table1_assumptions[j][5] / 100)
            row_max.append(FOD_waste_mass[i][j] * table1_assumptions[j][6] / 100)
        FOD_DOCi_Wi.append(row)
        FOD_DOCi_Wi_min.append(row_min)
        FOD_DOCi_Wi_max.append(row_max)
    zero_array = [0] * len(category_names_MSW)
    FOD_DOCi_Wi.append(zero_array)
    slider_values.append(360)
    for i in range(len(FOD_DOCi_Wi)):
        if FOD_DOCi_Wi[i] == []:
            FOD_DOCi_Wi[i] = zero_array

    try:
        # Try converting FOD_data[1] to a float
        FOD_data[1] = float(FOD_data[1])
    except (ValueError, IndexError):
        # If conversion fails or FOD_data[1] is not available, set it to 0
        FOD_data[1] = 0

    og_category_dic = {'Paper/Cardboard': 23.2,
                       'Textiles': 3.9,
                       'Food waste': 33.9,
                       'Wood': 8.2,
                       'Garden and Park waste': 9.8,
                       'Rubber and Leather': 1.4,
                       'Plastics': 8.5,
                       'Metal': 4.6,
                       'Glass': 6.5}

    Bulk_percentage_dic = {}

    for element in category_names_MSW:
        if element in og_category_dic.keys():
            Bulk_percentage_dic[element] = og_category_dic[element]
        else:
            Bulk_percentage_dic[element] = 0

    Bulk_percentage = list(Bulk_percentage_dic.values())

    FOD_DOC_in_site = []
    FOD_DDOC_mass0 = []
    for i in range(len(Bulk_percentage)):
        FOD_DOC_in_site.append((Bulk_percentage[i] / 100 * float(FOD_data[1])) * table1_assumptions[i][4] / 100)
        FOD_DDOC_mass0.append(LF_DOCi_Wi[i] + FOD_DOC_in_site[i])

    FOD_DDOC_mass = []
    results = []
    t = Delay / 12
    n = 50

    t_plot = []
    a = False
    if len(slider_values) != 0:
        for i in range(len(slider_values)):
            time = np.linspace(t, t + (slider_values[i] / 12), n).astype(float)
            for j in range(len(FOD_DDOC_mass0)):
                row = []
                for k in range(len(time)):
                    mass = FOD_DDOC_mass0[j] * (math.exp((-k_constant[0][j]) * time[k]))
                    row.append(mass)
                FOD_DDOC_mass.append(row)

            results.append(FOD_DDOC_mass)
            t_check = 0
            for p in range(len(FOD_DDOC_mass)):
                t_check += FOD_DDOC_mass[p][-1]

            if t_check == sum(FOD_DOCi_Wi[i]):  # this condition is non usable
                t_plot.append(time)
                t = time[-1]
                a = True
            else:
                if i == 0:
                    t_plot.append(time)
                    t = 0
                else:
                    if a == True:
                        t_plot.append(time)
                        a = False
                    else:
                        max_prev = max(t_plot[i - 1])
                        time += max_prev
                        t_plot.append(time)
                    t = 0

            for l in range(len(FOD_DDOC_mass)):
                FOD_DDOC_mass0[l] = FOD_DDOC_mass[l][-1] + FOD_DOCi_Wi[i][l]
            FOD_DDOC_mass = []

    results_plot = []
    for i in range(len(results[0])):
        a = []
        for k in range(len(results)):
            a += results[k][i]
        results_plot.append(a)

    y_plot = []
    plot_c = 0
    for i in range(len(results_plot)):
        row = []
        plot_c = 0
        for j in range(len(t_plot)):
            y_plot_segment = results_plot[i][plot_c:plot_c + n]
            row.append(y_plot_segment)
            plot_c += n
        y_plot.append(row)

    FOD_CH4_emissions = []

    for i in range(len(y_plot)):
        dif2 = []
        for j in range(len(y_plot[i])):
            dif1 = []
            for m in range(1, len(y_plot[i][j])):
                # Calculate the time interval between data points
                time_interval = t_plot[j][m] - t_plot[j][m - 1]
                # Compute the difference in DDOC mass between consecutive points and convert to CH4 emissions
                difference = abs(y_plot[i][j][m] - y_plot[i][j][m - 1]) * table8_assumptions[6] * (
                        16 / 12) / time_interval
                dif1.append(difference)
            dif2.append(dif1)
        FOD_CH4_emissions.append(dif2)

    fig1, axes1 = plt.subplots(2, 4, figsize=(16, 9))  # Increase figure size for better spacing
    axes1 = axes1.flatten()

    for u, ax in enumerate(axes1):
        for i, y in enumerate(y_plot[u]):
            ax.plot(t_plot[i], y, marker='o', markersize=2)

            # Connect consecutive segments with dashed lines
            if i > 0:
                ax.plot([t_plot[i - 1][-1], t_plot[i][0]], [y_plot[u][i - 1][-1], y_plot[u][i][0]], color='gray',
                        linestyle='--', label='_nolegend_')

        ax.set_xlabel('time (years)')
        ax.set_ylabel('DDOC mass (tons)')
        ax.set_title(f'Category {u + 1}: DOC decay with time')

        # # Creating legend dynamically
        # legend_labels = [f'segment {i + 1}' for i in range(len(y_plot[u]))]
        # ax.legend(legend_labels)

        ax.grid(True)

    plt.tight_layout(pad=2.5)  # Increase padding between subplots
    plt.get_current_fig_manager().window.state('zoomed')  # Maximize the figure window to full screen

    # Plotting the second set of data
    fig2, axes2 = plt.subplots(2, 4, figsize=(16, 9))  # Increase figure size for better spacing
    axes2 = axes2.flatten()

    for u, ax in enumerate(axes2):
        for i, y in enumerate(FOD_CH4_emissions[u]):
            ax.plot(t_plot[i][:-1], y, marker='o', markersize=2)

            # Connect consecutive segments with dashed lines
            if i > 0:
                ax.plot(t_plot[i - 1][-1], FOD_CH4_emissions[u][i - 1][-1], t_plot[i][0], FOD_CH4_emissions[u][i][0],
                        color='gray', linestyle='--', label='_nolegend_')

        ax.set_xlabel('time (years)')
        ax.set_ylabel('CH4 produced (tons)')
        ax.set_title(f'Category {u + 1}: CH4 emissions over time')

        ax.grid(True)

    plt.tight_layout(pad=2.5)  # Increase padding between subplots
    plt.get_current_fig_manager().window.state('zoomed')  # Maximize the figure window to full screen

    plt.show()

# -----------------------------------------------------------------------------------------
print()
print('---------------------Landfill Results--------------------------------------------------------------------------')
for i in range(len(category_names_MSW)):
    print(str(category_names_MSW[i]) + ': ' + str(round(LF_CO2_eq[i], 3)) + ' Tons of CO2 eq. ) / / ' + str(
        round(LF_CH4_recovered[i], 3)) + ' Tons of CH4 recovered')
print('Transport emissions: ' + str(round(LF_transp_emissions, 3)) + ' Tons of CO2 eq.')
print()
print('<Overall Results>')
print('GHG Emissions: ' + str(round(sum(LF_CO2_eq), 3)) + ' Tons of CO2 eq. // Min: ' + str(
    round(sum(LF_CO2_eq_min), 3)) + ' Tons of CO2 eq. // Max: ' + str(
    round(sum(LF_CO2_eq_max), 3)) + ' Tons of CO2 eq.')
print('Material recovery: ' + str(round(sum(LF_CH4_recovered), 3)) + ' Tons of CH4 recovered // Min: ' + str(
    round(sum(LF_CH4_recovered_min), 3)) + ' Tons of CH4 recovered // Max: ' + str(
    round(sum(LF_CH4_recovered_max), 3)) + ' Tons of CH4 recovered')
print('Energy recovery: Not Applicable')
print('---------------------------------------------------------------------------------------------------------------')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@@Incineration@@@@@@@@@@Incineration@@@@@@@@@@Incineration@@@@@@@@@@Incineration@@@@@@@@@Incineration@@@@@@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
INC_CO2_emissions_list = []
INC_flag = True

# Create the main Tkinter window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Ask the question
question_window = tk.Toplevel()
question_window.title("Incineration Question")

question_text = "Does the incineration system have any kind of energy recovery component?"
question_label = ttk.Label(question_window, text=question_text, wraplength=300)
question_label.pack(padx=10, pady=10)


def handle_answer(answer):
    global INC_flag
    INC_flag = answer
    question_window.destroy()
    root.destroy()  # Close the root window after answering the question
    root.quit()  # Quit the Tkinter main loop


yes_button = ttk.Button(question_window, text="Yes", command=lambda: handle_answer(True), width=8)
yes_button.pack(side="left", padx=(5, 2), pady=5, ipadx=10)

no_button = ttk.Button(question_window, text="No", command=lambda: handle_answer(False), width=8)
no_button.pack(side="right", padx=(2, 5), pady=5, ipadx=10)

question_window.mainloop()

# CO2 emissions
INC_CO2_emissions_list = []
INC_CO2_emissions_list_all_C = []

for i in range(len(Mass_dry_MSW)):
    # CO2_emissions_fossil_only = Dry mass * (total C %) * (fossil C %) * CO2/C mass ratio * OX factor
    INC_CO2_emissions_list.append(
        Mass_dry_MSW[i][2] * (table1_assumptions[i][7] / 100) * (table1_assumptions[i][11] / 100) *
        table7_assumptions[1] * table7_assumptions[2])

    # CO2_emissions_total_C = Dry mass * (total C %) * CO2/C mass ratio * OX factor
    INC_CO2_emissions_list_all_C.append(
        Mass_dry_MSW[i][2] * (table1_assumptions[i][7] / 100) * table7_assumptions[1] * table7_assumptions[2])

INC_CO2_emissions = sum(INC_CO2_emissions_list)  # tons of CO2
INC_CO2_emissions_all_C = sum(INC_CO2_emissions_list_all_C)  # tons of CO2

INC_mass = sum(mass[2] for mass in mass_matrix_MSW)  # tons

# CH4 emissions
INC_CH4_emissions = INC_mass * table7_assumptions[3] * 10 ** (-6)  # Kg of CH4

# N2O emissions
INC_N2O_emissions = INC_mass * table7_assumptions[4] * 10 ** (-6)  # Kg of N2O

# Transport emissions
INC_transp_emissions = INC_mass * table4_assumptions[7]  # tons of CO2 eq.

# CO2 eq calculations
INC_total_emissions = INC_CO2_emissions + INC_transp_emissions + INC_CH4_emissions * table23_assumptions[
    0] * 10 ** -3 + INC_N2O_emissions * table23_assumptions[1] * 10 ** -3  # tons of CO2 eq
INC_total_emissions_all_C = INC_CO2_emissions_all_C + INC_transp_emissions + INC_CH4_emissions * table23_assumptions[
    0] * 10 ** -3 + INC_N2O_emissions * table23_assumptions[1] * 10 ** -3  # tons of CO2 eq

# Energy calculations
INC_energy_value = 0  # MJ/Kg
INC_energy_recovered = 0  # MJ

if INC_flag == True:
    for i in range(len(mass_matrix_MSW)):
        INC_energy_value += (mass_matrix_MSW[i][2] * INC_energy[i]) / INC_mass
    # Energy = Calorific value of waste * mass of waste * efficiency
    INC_energy_recovered = INC_energy_value * INC_mass * (table7_assumptions[0] / 100)  # MJ

print()
print('-------------------Incineration Results------------------------------------------------------------------------')
print('GHG Emissions(Fossil Carbon): ' + str(round(INC_total_emissions, 3)) + ' Tons of CO2 eq.')
print('GHG Emissions(Total Carbon content): ' + str(round(INC_total_emissions_all_C, 3)) + ' Tons of CO2 eq.')
print('Material recovery: Not Applicable')
if INC_flag == True:
    print('Energy recovery: ' + str(round(INC_energy_recovered, 3)) + ' MJ')
else:
    print('Energy recovery: System does not have an energy recovery component')
print('---------------------------------------------------------------------------------------------------------------')

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@Output files@@@@@@@@@Output files@@@@@@@@@Output files@@@@@@@@@Output files@@@@@@@@@Output files@@@@@@@@@Outp
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
file_output_path = os.path.join(output_directory, output_file_name)
# Check if the directory exists, if not, create it
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

with open(file_output_path, mode='w', newline='') as file:
    writer = csv.writer(file)

    # Recycling Results
    writer.writerow(['Recycling Results------------------------------------------------------------------------------'])
    writer.writerow(['Category', 'Emissions (Tons of CO2 eq.)', 'Material Recovery (Tons)', 'Energy Consumption (MJ)'])
    for i in range(len(category_names_SCW)):
        writer.writerow(
            [category_names_SCW[i], round(recycling_emissions[i], 3), round(recycling_material_recovery[i], 3),
             round(recycling_energy_consumption[i], 3)])
    writer.writerow(['Overall Total', round(sum(recycling_emissions), 3), round(sum(recycling_material_recovery), 3),
                     round(sum(recycling_energy_consumption), 3)])
    writer.writerow([])

    # Composting Results
    writer.writerow([])
    writer.writerow(['Composting Results-----------------------------------------------------------------------------'])
    writer.writerow(['MSW Results'])
    writer.writerow(['Category', 'Emissions (Tons of CO2 eq.)', 'Material Recovery (Tons of compost)'])
    for i in range(len(category_names_MSW)):
        writer.writerow([category_names_MSW[i], round(Comp_CO2_eq_MSW[i], 3), round(Comp_compost_mass_MSW[i], 3)])
    writer.writerow([])
    writer.writerow(['Transport emissions', round(Comp_transp_emissions_MSW, 3)])

    writer.writerow([])
    writer.writerow(['SCW Results'])
    writer.writerow(['Category', 'Emissions (Tons of CO2 eq.)', 'Material Recovery (Tons of compost)'])
    for i in range(len(category_names_SCW)):
        writer.writerow([category_names_SCW[i], round(Comp_CO2_eq_SCW[i], 3), round(Comp_compost_mass_SCW[i], 3)])
    writer.writerow([])
    writer.writerow(['Transport emissions', round(Comp_transp_emissions_SCW, 3)])

    writer.writerow([])
    writer.writerow(['Overall Results'])
    writer.writerow(['', 'Average', 'Min', 'Max'])
    writer.writerow(['GHG Emissions:',
                     round(sum(Comp_CO2_eq_MSW) + sum(
                         Comp_CO2_eq_SCW) + Comp_transp_emissions_MSW + Comp_transp_emissions_SCW, 3),
                     round(sum(Comp_CO2_eq_min_MSW) + sum(
                         Comp_CO2_eq_min_SCW) + Comp_transp_emissions_MSW + Comp_transp_emissions_SCW, 3),
                    round(sum(Comp_CO2_eq_max_MSW) + sum(
                        Comp_CO2_eq_max_SCW) + Comp_transp_emissions_MSW + Comp_transp_emissions_SCW, 3)])
    writer.writerow(['Material Recovery:',
                     round(sum(Comp_compost_mass_MSW) + sum(Comp_compost_mass_SCW), 3),
                     round(sum(Comp_compost_mass_min_MSW) + sum(Comp_compost_mass_min_SCW), 3),
                     round(sum(Comp_compost_mass_max_MSW) + sum(Comp_compost_mass_max_SCW), 3)])

    # Anaerobic Digestion Results
    writer.writerow([])
    writer.writerow(['Anaerobic Digestion Results--------------------------------------------------------------------'])
    writer.writerow(['MSW Results'])
    writer.writerow(
        ['Category', 'Emissions (Tons of CO2 eq.)', 'Material Recovery (Tons of digestate)', 'Recovered CH4 (tons)'])
    for i in range(len(category_names_MSW)):
        writer.writerow([category_names_MSW[i], round(AD_CO2_eq_MSW[i], 3), round(AD_digestate_mass_MSW[i], 3),
                         round(AD_CH4_recovered_MSW[i], 3)])
    writer.writerow([])
    writer.writerow(['Transport emissions', round(AD_transp_emissions_MSW, 3)])

    writer.writerow([])
    writer.writerow(['SCW Results'])
    writer.writerow(
        ['Category', 'Emissions (Tons of CO2 eq.)', 'Material Recovery (Tons of digestate)', 'Recovered CH4 (tons)'])
    for i in range(len(category_names_SCW)):
        writer.writerow([category_names_SCW[i], round(AD_CO2_eq_SCW[i], 3), round(AD_digestate_mass_SCW[i], 3),
                         round(AD_CH4_recovered_SCW[i], 3)])
    writer.writerow([])
    writer.writerow(['Transport emissions', round(AD_transp_emissions_SCW, 3)])

    writer.writerow([])
    writer.writerow(['Overall Results'])
    writer.writerow(['', 'Average', 'Min', 'Max'])
    writer.writerow(['GHG Emissions:',
                     round(sum(AD_CO2_eq_MSW) + sum(AD_CO2_eq_SCW) + AD_transp_emissions_MSW + AD_transp_emissions_SCW,
                           3),
                     round(sum(AD_CO2_eq_min_MSW) + sum(
                         AD_CO2_eq_min_SCW) + AD_transp_emissions_MSW + AD_transp_emissions_SCW, 3),
                     round(sum(AD_CO2_eq_max_MSW) + sum(
                         AD_CO2_eq_max_SCW) + AD_transp_emissions_MSW + AD_transp_emissions_SCW, 3)])
    writer.writerow(['Material Recovery:',
                     round(sum(AD_digestate_mass_MSW) + sum(AD_digestate_mass_SCW), 3),
                     round(sum(AD_digestate_mass_min_MSW) + sum(AD_digestate_mass_min_SCW), 3),
                     round(sum(AD_digestate_mass_max_MSW) + sum(AD_digestate_mass_max_SCW), 3)])
    writer.writerow(['CH4 Recovery:',
                     round(sum(AD_CH4_recovered_MSW) + sum(AD_CH4_recovered_SCW), 3),
                     round(sum(AD_CH4_recovered_min_MSW) + sum(AD_CH4_recovered_min_SCW), 3),
                     round(sum(AD_CH4_recovered_max_MSW) + sum(AD_CH4_recovered_max_SCW), 3)])

    # Landfill Results
    writer.writerow([])
    writer.writerow(['Landfill Results-------------------------------------------------------------------------------'])
    writer.writerow(['Category', 'Emissions (Tons of CO2 eq.)', 'Recovered CH4 (tons)'])
    for i in range(len(category_names_MSW)):
        writer.writerow([category_names_MSW[i], round(LF_CO2_eq[i], 3), round(LF_CH4_recovered[i], 3)])
    writer.writerow([])
    writer.writerow(['Transport emissions', round(LF_transp_emissions, 3)])

    writer.writerow([])
    writer.writerow(['Overall Results'])
    writer.writerow(['', 'Average', 'Min', 'Max'])
    writer.writerow(
        ['GHG Emissions:', round(sum(LF_CO2_eq), 3), round(sum(LF_CO2_eq_min), 3), round(sum(LF_CO2_eq_max), 3)])
    writer.writerow(['Material Recovery:', round(sum(LF_CH4_recovered), 3), round(sum(LF_CH4_recovered_min), 3),
                     round(sum(LF_CH4_recovered_max), 3)])

    # Incineration Results
    writer.writerow([])
    writer.writerow(['Incineration Results---------------------------------------------------------------------------'])
    writer.writerow(['GHG Emissions (Fossil Carbon)', round(INC_total_emissions, 3)])
    writer.writerow(['GHG Emissions (Total Carbon content)', round(INC_total_emissions_all_C, 3)])
    if INC_flag:
        writer.writerow(['Energy Recovery', round(INC_energy_recovered, 3)])
    else:
        writer.writerow(['Energy Recovery', 'System does not have an energy recovery component'])

print('CSV file created successfully.')


# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# @@@@@@@@@Backup end@@@@@@@@@Backup end@@@@@@@@@Backup end@@@@@@@@@Backup end@@@@@@@@@Backup end@@@@@@@@@Backup end@@@@
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


def Backup_choice():
    # Create the main window outside of if-else to avoid UnboundLocalError
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    result = messagebox.askyesno("Backup settings",
                                 "The simulation is over. Do you wish for the Active data to become the new backup stage?")
    if result:
        # Ensure backup directory exists; create if it doesn't
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        # Copy the inventory file to the backup directory
        shutil.copy(os.path.join(directory_path_inventory, file_name_inventory_excel),
                    os.path.join(backup_directory, backup_file_name))

        # Display a pop-up window with a message
        messagebox.showinfo("Backup settings", "Original Backup overwritten by Main directory File")
    else:
        # Display a pop-up window with a message
        messagebox.showinfo("Backup settings", "Original Backup File kept")

    # Destroy the tkinter main window in both branches
    root.destroy()

    # Call the Backup_choice() function


Backup_choice()
