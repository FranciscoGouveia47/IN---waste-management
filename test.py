import os
import json
import tkinter as tk
from tkinter import filedialog

# Define the path for the directive file
directory_file_path = 'directory_file.json'

# Define expected file names
file_name_inventory_excel = 'Inventory_data.xlsx'
file_name_inventory = 'inventory_data.csv'
file_name_assumptions_excel = 'Assumptions_data.xlsx'
file_name_assumptions = 'Assumptions_data.csv'

def check_files_exist(directory_path, file_names):
    for file_name in file_names:
        file_path = os.path.join(directory_path, file_name)
        if not os.path.exists(file_path):
            print(f"File '{file_name}' not found in directory '{directory_path}'.")
            return False
    return True

def get_user_directives():
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
