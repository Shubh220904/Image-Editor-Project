import tkinter as tk
from tkinter import filedialog, colorchooser, simpledialog
from tkinter import ttk
from PIL import ImageTk
from Func import *

# Initialize the main Tkinter window
root = tk.Tk()
root.geometry("1000x600")
root.title("Image Drawing Tool")
root.config(bg="#F0F0F0")  # Set a light background color

# Global variables for pen settings, file path, and images
pen_color = "black"
pen_size = 5
file_path = ""
original_image = None
canvas_image = None
cropping = False
crop_start = (0, 0)
edited_image = None

# Function to add an image to the canvas
def add_image():
    global file_path, original_image, edited_image, canvas_image

    # Open a file dialog to choose an image file
    file_path = filedialog.askopenfilename(initialdir="D:/backup dell/PD LAB PROJECT/pictures")
    
    # Open and resize the image
    original_image = open_and_resize_image(file_path)
    
    # Create a copy of the original image for editing
    edited_image = original_image.copy()

    # Configure the canvas to match the image size
    canvas.config(width=original_image.width, height=original_image.height)
    
    # Create a Tkinter PhotoImage object from the original image
    canvas_image = ImageTk.PhotoImage(original_image)
    
    # Display the image on the canvas
    canvas.create_image(0, 0, image=canvas_image, anchor="nw")

# Function to change the pen color
def change_color():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

# Function to change the pen size
def change_size(size):
    global pen_size
    pen_size = size

# Function to draw on the canvas
def draw(event):
    global edited_image
    x, y = event.x, event.y
    x1, y1 = (x - pen_size), (y - pen_size)
    x2, y2 = (x + pen_size), (y + pen_size)

    # Draw on the edited image
    draw_on_image(edited_image, x1, y1, x2, y2, pen_color, pen_size)
    
    # Display the edited image on the canvas
    display_image(edited_image)

# Function to start the crop operation
def start_crop(event):
    global cropping, crop_start, crop_rect
    crop_start = (event.x, event.y)
    
    # Create a rectangle for visualizing the crop area
    crop_rect = canvas.create_rectangle(0, 0, 0, 0, outline="red", dash=(2, 2))
    cropping = True
    
    # Bind the mouse release event to end the crop operation
    canvas.bind("<ButtonRelease-1>", end_crop)

# Function to end the crop operation
def end_crop(event):
    global cropping, crop_start, original_image, canvas_image, crop_rect
    x1, y1 = crop_start
    x2, y2 = (event.x, event.y)

    # Check if the crop area is valid (non-zero size)
    if x2 >= x1 and y2 >= y1:
        # Crop the original image
        cropped_image = crop_image(original_image, x1, y1, x2, y2)
        
        # Display the cropped image on the canvas
        display_image(cropped_image)

    # Reset crop-related variables
    cropping = False
    crop_start = (0, 0)
    canvas.delete(crop_rect)

# Function to clear the canvas and display the original image
def clear_canvas():
    global original_image, canvas_image
    canvas.delete("all")
    
    # Display the original image on the canvas
    canvas_image = ImageTk.PhotoImage(original_image)
    canvas.create_image(0, 0, image=canvas_image, anchor="nw")

# Function to apply a selected filter to the image
def apply_filter(selected_filter):
    global original_image, canvas_image
    
    # Open and resize the original image
    image = open_and_resize_image(file_path)
    
    # Apply the selected filter
    filtered_image = apply_selected_filter(image, selected_filter)
    
    # Display the filtered image on the canvas
    display_image(filtered_image)

# Function to rotate the image based on user input
def rotate_image_dialog():
    angle = simpledialog.askinteger("Rotate Image", "Enter rotation angle (in degrees):", parent=root, minvalue=0, maxvalue=360)
    if angle is not None:
        image = open_and_resize_image(file_path)
        rotated_image = rotate_image(image, angle)
        display_image(rotated_image)

# Function to flip the image based on user input
def flip_image_dialog():
    direction = simpledialog.askstring("Flip Image", "Enter direction (Vertical/Horizonal):", parent=root)
    if direction and direction.lower() in ["vertical", "horizontal"]:
        image = open_and_resize_image(file_path)
        flipped_image = flip_image(image, direction.capitalize())
        display_image(flipped_image)

# Function to initiate the crop operation
def crop_image_dialog():
    global cropping, drawing
    cropping = True
    drawing = False
    canvas.bind("<ButtonPress-1>", start_crop)

# Function to adjust brightness based on user input
def brightness_adjustment_dialog():
    factor = simpledialog.askfloat("Brightness Adjustment", "Enter brightness factor (0.1 - 2.0):", parent=root, minvalue=0.1, maxvalue=2.0)
    if factor is not None:
        image = open_and_resize_image(file_path)
        adjusted_image = adjust_brightness(image, factor)
        display_image(adjusted_image)

# Function to adjust contrast based on user input
def contrast_adjustment_dialog():
    factor = simpledialog.askfloat("Contrast Adjustment", "Enter contrast factor (0.1 - 2.0):", parent=root, minvalue=0.1, maxvalue=2.0)
    if factor is not None:
        image = open_and_resize_image(file_path)
        adjusted_image = adjust_contrast(image, factor)
        display_image(adjusted_image)

# Function to save the edited image to a file
def save_image_dialog():
    save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if save_path:
        save_image(original_image, save_path)

# Function to display the edited image on the canvas
def display_image(image):
    global canvas_image,original_image
    canvas_image = ImageTk.PhotoImage(image)
    canvas.config(width=canvas_image.width(), height=canvas_image.height())
    canvas.create_image(0, 0, image=canvas_image, anchor="nw")

# Function to initiate the drawing operation
def draw_image_dialog():
    global cropping, drawing
    cropping = False
    drawing = True
    canvas.bind("<B1-Motion>", draw)

# Left frame for UI controls
left_frame = tk.Frame(root, width=200, height=600, bg="#404040")  # Dark gray color
left_frame.pack(side="left", fill="y")

# Canvas for displaying images
canvas = tk.Canvas(root, width=750, height=600, bg="white")  # White background
canvas.pack()

# Buttons and UI controls
image_button = tk.Button(left_frame, text="Add Image", command=add_image, bg="#66ccff")  # Light blue color
image_button.pack(pady=15)

draw_button = tk.Button(left_frame, text="Draw", command=draw_image_dialog, bg="#66ccff")  # Light blue color
draw_button.pack(pady=5)

color_button = tk.Button(left_frame, text="Change Pen Color", command=change_color, bg="#66ccff")  # Light blue color
color_button.pack(pady=5)

pen_size_frame = tk.Frame(left_frame, bg="#404040")  # Dark gray color
pen_size_frame.pack(pady=5)

pen_size_1 = tk.Radiobutton(pen_size_frame, text="Small", value=3, command=lambda: change_size(3), bg="#404040", fg="white")  # Dark gray color with white text
pen_size_1.pack(side="left")

pen_size_2 = tk.Radiobutton(pen_size_frame, text="Medium", value=5, command=lambda: change_size(5), bg="#404040", fg="white")  # Dark gray color with white text
pen_size_2.pack(side="left")
pen_size_2.select()

pen_size_3 = tk.Radiobutton(pen_size_frame, text="Large", value=7, command=lambda: change_size(7), bg="#404040", fg="white")  # Dark gray color with white text
pen_size_3.pack(side="left")

clear_button = tk.Button(left_frame, text="Clear", command=clear_canvas, bg="#FF9797")  # Light red color
clear_button.pack(pady=10)

filter_label = tk.Label(left_frame, text="Select Filter", bg="#404040", fg="white")  # Dark gray color with white text
filter_label.pack()
filter_combobox = ttk.Combobox(left_frame, values=["Black and White", "Blur", "Emboss", "Sharpen", "Smooth"], background="#66ccff")  # Light blue color
filter_combobox.pack()

filter_combobox.bind("<<ComboboxSelected>>", lambda event: apply_filter(filter_combobox.get()))

rotate_button = tk.Button(left_frame, text="Rotate", command=rotate_image_dialog, bg="#66ccff")  # Light blue color
rotate_button.pack(pady=5)

flip_button = tk.Button(left_frame, text="Flip", command=flip_image_dialog, bg="#66ccff")  # Light blue color
flip_button.pack(pady=5)

crop_button = tk.Button(left_frame, text="Crop", command=crop_image_dialog, bg="#66ccff")  # Light blue color
crop_button.pack(pady=5)

brightness_button = tk.Button(left_frame, text="Brightness", command=brightness_adjustment_dialog, bg="#66ccff")  # Light blue color
brightness_button.pack(pady=5)

contrast_button = tk.Button(left_frame, text="Contrast", command=contrast_adjustment_dialog, bg="#66ccff")  # Light blue color
contrast_button.pack(pady=5)

save_last_button = tk.Button(left_frame, text="Save Edited Image", command=save_image_dialog, bg="#66ccff")  # Light blue color
save_last_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
