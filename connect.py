import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Global variables
data = None  # Holds the loaded data from the Excel file
selected_options = []  # Stores the selected places for simulation
selected_timescale_value = ""  # Stores the selected time series scale
config_file = "WPM_config.txt"  # File used to save and load the coefficient file path

# Function to load the saved coefficient file path from config file
def load_config():
    """Load the last used coefficient file path from the config file."""
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return f.read().strip()  # Read and remove any extra spaces/newlines
    return None

# Function to save the coefficient file path to the config file
def save_config(file_path):
    """Save the coefficient file path to the config file."""
    with open(config_file, "w") as f:
        f.write(file_path)

# Function to handle the loading of the Excel file
def load_excel_file():
    """Opens a file dialog to select and load an Excel file."""
    global data
    # Open a file dialog to select an Excel file
    file_path = askopenfilename(title="Select Excel file", filetypes=[("Excel files", "*.xlsx *.xls")])
    if file_path:  # Check if a file was selected
        try:
            # Load the data using pandas
            data = pd.read_excel(file_path)
            print("Excel file loaded successfully!")

            # Update the status label
            status_label.config(text="Data loaded", fg="green")

            # Enable the second button for editing simulation
            button2.config(state=tk.NORMAL)
        except Exception as e:
            print(f"Error loading Excel file: {e}")
    else:
        print("No file selected.")

# Function to open a window for selecting simulation options (checkboxes and timescale)
def open_checkbox_window():
    """Opens a window to select simulation options and time scale."""
    global data, selected_options, selected_timescale_value
    if data is not None:
        # Get unique values from the first column (places) of the data
        unique_values = data.iloc[:, 0].drop_duplicates().dropna().tolist()

        # Create a new window for checkboxes and combo box
        checkbox_window = tk.Toplevel(root)
        checkbox_window.title("Select Options")
        checkbox_window.geometry("400x400")  # Set a fixed size for the window

        # Frame for the "Select All" checkbox
        select_all_frame = tk.Frame(checkbox_window)
        select_all_frame.pack(fill=tk.X, padx=10, pady=5)

        # Function to select/deselect all checkboxes
        def toggle_select_all():
            select_all_state = select_all_var.get()
            for var in checkbox_states.values():
                var.set(select_all_state)

        # Add a "Select All" checkbox at the top
        select_all_var = tk.BooleanVar()
        select_all_checkbox = tk.Checkbutton(select_all_frame, text="Select All", variable=select_all_var,
                                             command=toggle_select_all)
        select_all_checkbox.pack(anchor="w")

        # Frame for the scrollable area (checkboxes)
        canvas_frame = tk.Frame(checkbox_window)
        canvas_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Create a canvas and scrollbar for checkboxes
        canvas = tk.Canvas(canvas_frame, height=150)
        scrollbar = tk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold the checkboxes
        checkbox_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=checkbox_frame, anchor="nw")

        # Add a vertical scrollbar
        scrollbar.pack(side=tk.RIGHT, fill="y")
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        checkbox_states = {}

        # Create individual checkboxes for each unique value (Place)
        for value in unique_values:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, text=value, variable=var)
            checkbox.pack(anchor="w", padx=10, pady=2)  # Add consistent padding
            checkbox_states[value] = var

        # Update the scrollable region to include all checkboxes
        checkbox_frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        # Frame for combo box and confirm button
        bottom_frame = tk.Frame(checkbox_window)
        bottom_frame.pack(fill=tk.X, padx=10, pady=5)

        # Label and combo box for time series scale
        combo_frame = tk.Frame(bottom_frame)
        combo_frame.pack(anchor="w", pady=5)
        tk.Label(combo_frame, text="Time series scale", font=("Arial", 12)).grid(row=0, column=0, padx=5, sticky="w")
        timescales = ["1 month", "3 months", "6 months", "1 year", "5 years", "10 years"]
        selected_timescale = tk.StringVar()
        timescale_combo = ttk.Combobox(combo_frame, textvariable=selected_timescale, values=timescales,
                                       state="readonly", width=12)
        timescale_combo.grid(row=0, column=1, padx=5, sticky="w")

        # Function to enable confirm button if both conditions are met (checkboxes and timescale)
        def update_confirm_button_state():
            any_checkbox_selected = any(var.get() for var in checkbox_states.values())
            combo_selected = selected_timescale.get() != ""
            confirm_button.config(state=tk.NORMAL if any_checkbox_selected and combo_selected else tk.DISABLED)

        # Bind events to update the confirm button's state
        for var in checkbox_states.values():
            var.trace_add("write", lambda *args: update_confirm_button_state())
        timescale_combo.bind("<<ComboboxSelected>>", lambda event: update_confirm_button_state())

        # Button to confirm selection
        def confirm_selection():
            global selected_options, selected_timescale_value
            selected_options = [key for key, var in checkbox_states.items() if var.get()]
            selected_timescale_value = selected_timescale.get()

            # Update the status label
            status_label.config(text="Data loaded and edited", fg="green")

            # Enable the third button for final confirmation
            button3.config(state=tk.NORMAL)

            checkbox_window.destroy()

        # Add the confirm button centered in the bottom frame
        confirm_button = tk.Button(bottom_frame, text="Confirm", command=confirm_selection, state=tk.DISABLED)
        confirm_button.pack(pady=10)

# Function to confirm the selections and proceed with simulation
def confirm_and_exit():
    """Validates the selected options, performs the linear regression, and generates plots."""
    global root
    print("Application confirmed and proceeding...")

    # Ensure the 'Place' column exists in the data
    if 'Place' not in data.columns:
        print("Error: 'Place' column not found in the dataset.")
        exit()

    # Filter rows based on selected options (places)
    sim_data = data[data['Place'].isin(selected_options)]

    if sim_data.empty:
        print("No data matched the selected options.")
        return

    # Load the saved coefficient file path, if available
    saved_coef_path = load_config()

    if saved_coef_path:
        # Use the saved file path if it exists
        file_path_coef = saved_coef_path
        print(f"Using previously selected coefficient file: {file_path_coef}")
    else:
        # Open file dialog to select a new CSV file if no saved path
        file_path_coef = askopenfilename(
            title="Select Coefficient file",
            filetypes=[("CSV files", "*.csv")]
        )

    if file_path_coef:
        # Save the new file path for future use
        save_config(file_path_coef)

        # Read CSV with a custom separator (e.g., comma, semicolon, tab)
        df = pd.read_csv(file_path_coef, sep=',')  # Change ',' to your desired separator
    else:
        print("No coefficient file selected.")
        return

    # Get variable names (columns starting from the third column)
    variables = sim_data.columns[2:].tolist()

    # Linear regression coefficients (from the loaded CSV)
    coef_ridge = df.iloc[:, 1].tolist()
    coef_lasso = df.iloc[:, 2].tolist()

    # Apply multivariate linear regression for each row
    def compute_lr(row, coefficients):
        """Compute the linear regression for a given row and coefficients."""
        result = coefficients[0]  # Start with intercept
        for i, coef in enumerate(coefficients[1:], start=1):
            try:
                value = float(row[str(variables[i - 1])])  # Convert to float
                result += coef * value
            except ValueError:
                print(f"Skipping {variables[i - 1]} due to conversion error")
                continue
        return result

    # Apply regression outputs to the simulation data
    sim_data = sim_data.copy()  # Ensure it's a copy
    sim_data.loc[:, 'Ridge_output'] = sim_data.apply(lambda row: compute_lr(row, coef_ridge), axis=1)
    sim_data.loc[:, 'Lasso_output'] = sim_data.apply(lambda row: compute_lr(row, coef_lasso), axis=1)

    # Print the updated DataFrame
    print(sim_data[['Place', 'Time step', 'Ridge_output', 'Lasso_output']])

    # Generate the plots for Ridge and Lasso regression
    generate_plots(sim_data, selected_timescale_value)

    # Save the output to a file (CSV for the regression results)
    output_file = asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if output_file:
        sim_data.to_csv(output_file, index=False)
        print(f"Results saved to {output_file}")

    # Destroy the main window
    root.destroy()

def generate_plots(sim_data, selected_timescale_value):
    """Generate Ridge and Lasso regression plots (but don't save them to files)."""
    # Ensure required columns exist
    if 'Place' not in sim_data.columns or 'Time step' not in sim_data.columns:
        print("Error: Missing required columns ('Place' or 'Time step') in the data.")
        return

    # Create Ridge plot
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    sns.set_palette("tab10")  # Set a color palette for different places
    for place in sim_data['Place'].unique():
        place_data = sim_data[sim_data['Place'] == place]
        ax1.plot(place_data['Time step'], place_data['Ridge_output'], marker='o', label=place)

    ax1.set_xlabel(f'Time step ({selected_timescale_value})')
    ax1.set_ylabel('Ridge Regression Output')
    ax1.set_title('Ridge Regression Results')
    ax1.legend(title="Places")
    ax1.grid(True)

    # Set x-axis limits
    ax1.set_xlim(0, int(sim_data['Time step'].max()))
    ax1.set_xticks(range(0, int(sim_data['Time step'].max()) + 1))

    # Show Ridge plot
    plt.show(block=False)  # Keep it open and allow the next plot

    # Create Lasso plot
    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for place in sim_data['Place'].unique():
        place_data = sim_data[sim_data['Place'] == place]
        ax2.plot(place_data['Time step'], place_data['Lasso_output'], marker='o', label=place)

    ax2.set_xlabel(f'Time step ({selected_timescale_value})')
    ax2.set_ylabel('Lasso Regression Output')
    ax2.set_title('Lasso Regression Results')
    ax2.legend(title="Places")
    ax2.grid(True)

    # Set x-axis limits
    ax2.set_xlim(0, int(sim_data['Time step'].max()))
    ax2.set_xticks(range(0, int(sim_data['Time step'].max()) + 1))

    # Show Lasso plot
    plt.show()  # Explicitly show the second plot

# Create the main window
root = tk.Tk()
root.title("WPM - Waste Prediction Model")
root.geometry("400x200")  # Set window size

# Create a frame for content
frame = tk.Frame(root)
frame.pack(expand=True)

# Add a label above the buttons
label = tk.Label(frame, text="Simulation Setup Phase", font=("Arial", 14))
label.pack(pady=10)

# Create another frame for the buttons
button_frame = tk.Frame(frame)
button_frame.pack()

# Create the buttons with click handlers
button1 = tk.Button(button_frame, text="Load Data File", command=load_excel_file)
button2 = tk.Button(button_frame, text="Edit Simulation", command=open_checkbox_window, state=tk.DISABLED)
button3 = tk.Button(button_frame, text="Confirm and Go", command=confirm_and_exit, state=tk.DISABLED)

# Pack the buttons in the button frame with horizontal arrangement
button1.pack(side=tk.LEFT, padx=10)
button2.pack(side=tk.LEFT, padx=10)
button3.pack(side=tk.LEFT, padx=10)

# Add a status label below the first button
status_label = tk.Label(frame, text="Data not loaded", fg="gray", font=("Arial", 10))
status_label.pack(pady=10)

# Run the application
root.mainloop()
