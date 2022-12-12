# GUI for Line detection by Hough Transform
# DIP semester project
# Branduse, Malin-Dorin and Jimon, Lucian-Daniel
import tkinter as tk

# Import filedialog explicitly, because of faulty behaviour
from tkinter import filedialog

# Import ttk explicitly, because of faulty behaviour
from tkinter import ttk

import cv2 as cv
import numpy as np
from PIL import Image, ImageTk
from matplotlib import pyplot as plt

from src.hough_transformer import HoughTransformer

transformer = HoughTransformer()

# Create the root window
root = tk.Tk()
# Setting title
root.title("Line detection by Hough Transform")
# Setting window size and characteristics
width = 800
height = 475
screenwidth = root.winfo_screenwidth()
screenheight = root.winfo_screenheight()
alignstr = "%dx%d+%d+%d" % (
    width,
    height,
    (screenwidth - width) / 2,
    (screenheight - height) / 2,
)
# Set the window's icon to the specified image file
photo = ImageTk.PhotoImage(file="src/logo.bmp")
root.iconphoto(False, photo)
# Set geometry
root.geometry(alignstr)
root.resizable(width=False, height=False)

app_font = ("Arial", 10)

canny_threshold_delta = 50
# Flag for process done phase
wasItProcessed = 0
# Flag for browsing done phase
wasItChosen = 0
# Input image variable
global in_img
# Edge detected image
global edges

# Hough transform function called
def transform():
    global wasItProcessed
    global in_img
    global edges
    global wasItChosen

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    if edges is None:
        cannyTransform()

    if wasItProcessed:
        lines = transformer.extractLinesFromAccumulator(int(getHoughThreshold()))
    else:
        lines = transformer.hough_transform(edges, int(getHoughThreshold()))

    print("Hough Lines:", lines)
    output = cv.cvtColor(in_img, cv.COLOR_BGR2RGB)
    output = transformer.plotLinesToImage(output, lines)
    # Open the image file using PIL
    displayImage(Image.fromarray(output, mode="RGB"))

    wasItProcessed = 1
    print("Hough transform:" + str(wasItProcessed))


def displayImage(inputImage):
    global initImage
    inputImage.thumbnail((initImage.winfo_width(), initImage.winfo_height()))
    # Convert the image to a Tkinter-compatible photo image
    inputPhoto = ImageTk.PhotoImage(inputImage)
    # Update the label's image attribute with the new photo image
    initImage.config(image=inputPhoto)
    initImage.image = inputPhoto


# Function for opening the file explorer window
def browseFiles():
    global openedfile
    openedfile = filedialog.askopenfilename(
        initialdir="/",
        title="Select an Image",
        filetypes=(
            ("Image files", "*.png"),
            ("Image files", "*.jpg"),
            ("Image files", "*.jpeg"),
        ),
    )
    # Open the image file using PIL
    inputImage = Image.open(openedfile)
    displayImage(inputImage)

    global in_img
    in_img = cv.imread(openedfile)
    # Adjust the layout of the label to fit the resized image
    # initImage.pack(side="left", fill="both", expand=True)

    cannyTransform()

    # Setting flags to corresponding values
    global wasItChosen
    wasItChosen = 1
    global wasItProcessed
    wasItProcessed = 0


def cannyTransform():
    global in_img
    global wasItChosen
    global edges

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    edges = cv.Canny(
        in_img,
        int(getCannyThreshold() - canny_threshold_delta / 2),
        int(getCannyThreshold() + canny_threshold_delta / 2),
    )


def transformOpenCV():
    global wasItProcessed
    global edges
    global in_img
    global wasItChosen

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    if edges is None:
        cannyTransform()

    lines = transformer.hough_transform_cv(edges, int(getHoughThreshold()))

    print("Hough Lines with OpenCV:", lines)
    output = cv.cvtColor(in_img, cv.COLOR_BGR2RGB)
    output = transformer.plotLinesToImage(output, lines, 2, (0, 0, 255))
    # Open the image file using PIL
    displayImage(Image.fromarray(output))

    print("Hough transform with OpencV")


def showAccumulator():
    global wasItProcessed
    global wasItChosen
    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    if not wasItProcessed:
        return

    transformer.plotAccumulator()


def showCannyEdge():
    global in_img
    global wasItChosen
    global edges

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    if edges is None:
        cannyTransform()

    displayImage(Image.fromarray(edges))


# Buttons

# Browse for image button
browseImageButton = tk.Button(
    root,
    font=app_font,
    text="Browse Images",
    command=browseFiles,
    padx=8,
    pady=4,
)
browseImageButton.place(x=20, y=100)

# Do Line detection button
performTransformButton = tk.Button(
    root,
    font=app_font,
    text="Apply Hough Transform",
    command=transform,
    padx=8,
    pady=4,
)
performTransformButton.place(x=20, y=240)

# Perform OpenCV-based Line detection
compareOpenCVButton = tk.Button(
    root,
    font=app_font,
    text="Compare with OpenCV",
    command=transformOpenCV,
    padx=8,
    pady=4,
)
compareOpenCVButton.place(x=20, y=280)

# Show Canny edge detected image button
showCanny = tk.Button(
    root,
    font=app_font,
    text="Show Canny edge detection",
    command=showCannyEdge,
    padx=8,
    pady=4,
)
showCanny.place(x=20, y=320)

# Show accumulator button
accumulatorButton = tk.Button(
    root,
    font=app_font,
    text="Show Accumulator",
    command=showAccumulator,
    padx=8,
    pady=4,
)
accumulatorButton.place(x=20, y=360)

# Exit GUI
exitButton = tk.Button(
    root,
    font=app_font,
    text="Exit",
    command=exit,
    padx=8,
    pady=4,
)
exitButton.place(x=20, y=420)

# Labels
# Title label
titleLabel = tk.Label(
    root,
    font=("Arial", 20, "bold"),
    text="Hough Transform",
)
titleLabel.place(x=20, y=20)

# Choose an image label
chooseImageLabel = tk.Label(
    root,
    font=app_font,
    text="Choose an image in jpg/png format",
)
chooseImageLabel.place(x=20, y=70)

houghThresholdLabel = tk.Label(
    root,
    font=app_font,
    bg="#f0f0f0",
    fg="black",
    text="Hough Threshold",
)
houghThresholdLabel.place(x=20, y=140)

# Internal methods for slider event
def houghThresholdChanged(event):
    houghThresholdLabel.configure(
        text="Hough Threshold = " + str(int(getHoughThreshold()))
    )


def cannyThresholdChanged(event):
    cannyThresholdLabel.configure(
        text="Canny Threshold = " + str(int(getCannyThreshold()))
    )
    # Force the canny edge detection to be performed again
    global edges
    edges = None
    global wasItProcessed
    wasItProcessed = 0


# Slider current value
houghThresholdValue = tk.DoubleVar(value=100)

# Function to get the slider's current value
def getHoughThreshold():
    return houghThresholdValue.get()


def getCannyThreshold():
    return cannyThresholdValue.get()


# Hough Threshold Slider
houghThresholdSlider = ttk.Scale(
    root,
    from_=50,
    to=500,
    orient="horizontal",
    variable=houghThresholdValue,
    command=houghThresholdChanged,
)
houghThresholdSlider.place(x=20, y=160, width=228, height=30)

cannyThresholdLabel = tk.Label(
    root, font=app_font, fg="#333333", text="Canny Threshold"
)
cannyThresholdLabel.place(x=20, y=190)

cannyThresholdValue = tk.DoubleVar(value=100)

# Canny Threshold Slider
cannyThresholdSlider = ttk.Scale(
    root,
    from_=50,
    to=500,
    orient="horizontal",
    variable=cannyThresholdValue,
    command=cannyThresholdChanged,
)
cannyThresholdSlider.place(x=20, y=210, width=228, height=30)

# Frame labels
# Initial image
initImage = tk.Label(root, borderwidth=2)
initImage.place(x=280, y=20, width=500, height=440)

# Display initial slider values in labels
houghThresholdChanged(None)
cannyThresholdChanged(None)

# Starting GUI
if __name__ == "__main__":
    root.mainloop()
