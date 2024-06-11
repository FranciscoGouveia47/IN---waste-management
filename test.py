import matplotlib.pyplot as plt

# Create a plot
plt.plot([1, 2, 3], [4, 5, 6])
plt.title('Sample Plot')

# Try to maximize the figure window if in a GUI environment
try:
    manager = plt.get_current_fig_manager()
    # Check if the backend is correctly set to one that supports the window attribute
    if hasattr(manager, 'window'):
        manager.window.state('zoomed')  # Maximize the figure window to full screen
    else:
        print("The current backend does not support the 'window' attribute.")
except Exception as e:
    print(f"An error occurred while trying to maximize the window: {e}")

# Show plot
plt.show()
