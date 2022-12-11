# GUI for Line detection by Hough Transform
# DIP semester project
# Branduse, Malin-Dorin and Jimon, Lucian-Daniel
import cv2 as cv
import tkinter as tk
import tkinter.font as tkFont

# Import filedialog explicitly, because of faulty behaviour
from tkinter import filedialog

# Import ttk explicitly, because of faulty behaviour
from tkinter import ttk
from tkinter import Toplevel
import sys
import PIL
from PIL import Image, ImageTk
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
photo = ImageTk.PhotoImage(file="src\\logo.bmp")
root.iconphoto(False, photo)
# Set geometry
root.geometry(alignstr)
root.resizable(width=False, height=False)

# Flag for process done phase
wasItProcessed = 0
# Flag for browsing done phase
wasItChosen = 0
# Input image variable
global in_img
# Edge detected image
global edges

# Hough transform function called
def doTransform():
    global wasItProcessed
    global in_img
    global edges
    global wasItChosen

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    if wasItProcessed:
        lines = transformer.extractLinesFromAccumulator(int(getCurrentSliderValue()))
    else:
        lines = transformer.hough_transform(edges, int(getCurrentSliderValue()))

    print("Hough Lines:", lines)
    output = cv.cvtColor(in_img, cv.COLOR_GRAY2RGB)
    output = transformer.plotLinesToImage(output, lines)
    # Open the image file using PIL
    inputImage = Image.fromarray(output)
    inputImage = inputImage.resize((initImage.winfo_width(), initImage.winfo_height()))
    # Convert the image to a Tkinter-compatible photo image
    inputPhoto = ImageTk.PhotoImage(inputImage)
    # Update the label's image attribute with the new photo image
    initImage.config(image=inputPhoto)
    initImage.image = inputPhoto

    wasItProcessed = 1
    print("Hough transform:" + str(wasItProcessed))


# Function for opening the file explorer window
def browseFiles():
    global openedfile
    openedfile = filedialog.askopenfilename(
        initialdir="/",
        title="Select an Image",
        filetypes=(("Image files", "*.png"), ("Image files", "*.jpg")),
    )
    # Open the image file using PIL
    inputImage = Image.open(openedfile)
    # Resize the image to fit the dimensions of the label
    inputImage = inputImage.resize((initImage.winfo_width(), initImage.winfo_height()))
    # Convert the image to a Tkinter-compatible photo image
    inputPhoto = ImageTk.PhotoImage(inputImage)
    # Update the label's image attribute with the new photo image
    initImage.config(image=inputPhoto)
    initImage.image = inputPhoto
    global in_img
    in_img = cv.imread(openedfile, cv.IMREAD_GRAYSCALE)
    # Adjust the layout of the label to fit the resized image
    # initImage.pack(side="left", fill="both", expand=True)
    global edges
    canny_thresholds = [250, 300]
    edges = cv.Canny(in_img, canny_thresholds[0], canny_thresholds[1])

    # Setting flags to corresponding values
    global wasItChosen
    wasItChosen = 1
    global wasItProcessed
    wasItProcessed = 0


# inImg = image.open(path)


def transformOpenCV():
    global wasItProcessed
    global edges
    global in_img
    global wasItChosen

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    if wasItProcessed:
        lines = transformer.extractLinesFromAccumulator(int(getCurrentSliderValue()))
    else:
        lines = transformer.hough_transform_cv(edges, int(getCurrentSliderValue()))

    print("Hough Lines with OpenCV:", lines)
    output = cv.cvtColor(in_img, cv.COLOR_GRAY2BGR)
    output = transformer.plotLinesToImageOpenCV(output, lines)
    plt.figure(figsize=(15, 10))
    plt.imshow(output)
    plt.title("Hough Transform with OpenCV")
    plt.show()

    wasItProcessed = 1
    print("Hough transform with OpencV:" + str(wasItProcessed))


def showHistograms():
    global wasItProcessed
    global in_img
    global edges
    global wasItChosen

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    # Compute the histogram for the grayscale image
    hist = cv.calcHist([in_img], [0], None, [256], [0, 256])
    print(hist)

    plt.figure()
    plt.hist(in_img.ravel(), 256, [0, 255])
    plt.suptitle("The histogram of the input grayscale image")
    if wasItProcessed == 1:
        plt.hist(edges.ravel(), 256, [0, 255])
        plt.suptitle("The histogram of the Canny edge detected image")
    plt.show()


def showCannyEdge():
    global in_img
    global wasItChosen
    global edges

    # Early bail if not the case
    if wasItChosen == 0:
        initImage.config(text="You need to choose an image", font=("Arial", 15, "bold"))
        return 0

    plt.figure(figsize=(10, 8))
    plt.imshow(edges, cmap="gray")
    plt.title("Input Image")
    plt.show()


# Buttons
# Do Line detection button
performTransformButton = tk.Button(root)
performTransformButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family="Times", size=10)
performTransformButton["font"] = ft
performTransformButton["fg"] = "#000000"
performTransformButton["justify"] = "center"
performTransformButton["text"] = "Action!"
performTransformButton.place(x=20, y=200, width=100, height=25)
performTransformButton["command"] = doTransform

# Show Canny edge detected image button
showCanny = tk.Button(root)
showCanny["bg"] = "#f0f0f0"
ft = tkFont.Font(family="Times", size=10)
showCanny["font"] = ft
showCanny["fg"] = "#000000"
showCanny["justify"] = "center"
showCanny["text"] = "Show edge image"
showCanny.place(x=20, y=235, width=130, height=25)
showCanny["command"] = showCannyEdge

# Browse for image button
browseImageButton = tk.Button(root)
browseImageButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family="Times", size=10)
browseImageButton["font"] = ft
browseImageButton["fg"] = "#000000"
browseImageButton["justify"] = "center"
browseImageButton["text"] = "Browse"
browseImageButton.place(x=20, y=100, width=120, height=25)
browseImageButton["command"] = browseFiles

# Perform OpenCV-based Line detection
compareOpenCVButton = tk.Button(root)
compareOpenCVButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family="Times", size=10)
compareOpenCVButton["font"] = ft
compareOpenCVButton["fg"] = "#000000"
compareOpenCVButton["justify"] = "center"
compareOpenCVButton["text"] = "Compare results with OpenCV line detection"
compareOpenCVButton.place(x=20, y=360, width=350, height=25)
compareOpenCVButton["command"] = transformOpenCV

# Show histograms button
histogramButton = tk.Button(root)
histogramButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family="Times", size=10)
histogramButton["font"] = ft
histogramButton["fg"] = "#000000"
histogramButton["justify"] = "center"
histogramButton["text"] = "Show histograms"
histogramButton.place(x=20, y=325, width=150, height=25)
histogramButton["command"] = showHistograms


# Exit GUI
exitButton = tk.Button(root)
exitButton["bg"] = "#f0f0f0"
ft = tkFont.Font(family="Times", size=10)
exitButton["font"] = ft
exitButton["fg"] = "#000000"
exitButton["justify"] = "center"
exitButton["text"] = "Close application"
exitButton.place(x=20, y=395, width=120, height=25)
exitButton["command"] = exit
# Labels
# Title label
titleLabel = tk.Label(root)
ft = tkFont.Font(family="Times", size=15, weight="bold")
titleLabel["font"] = ft
titleLabel["fg"] = "#333333"
titleLabel["justify"] = "center"
titleLabel["text"] = "Line Detection"
titleLabel.place(x=131, y=20, width=538, height=30)

# Choose an image label
chooseImageLabel = tk.Label(root)
ft = tkFont.Font(family="Times", size=10)
chooseImageLabel["font"] = ft
chooseImageLabel["fg"] = "#333333"
chooseImageLabel["justify"] = "center"
chooseImageLabel["text"] = "Choose an image in jpg/png format"
chooseImageLabel.place(x=20, y=60, width=240, height=30)

# Show active treshold
tresholdLabel = tk.Label(root)
ft = tkFont.Font(family="Times", size=10)
tresholdLabel["font"] = ft
tresholdLabel["fg"] = "#333333"
tresholdLabel["justify"] = "center"
tresholdLabel["text"] = "Hough Treshold = 50"
tresholdLabel.place(x=25, y=130, width=231, height=30)

# Slider current value
currentSliderValue = tk.DoubleVar()

# Internal methods for slider event
def slider_changed(event):
    tresholdLabel.configure(
        text="Hough Treshold = " + str(int(getCurrentSliderValue()))
    )


# Function to get the slider's current value
def getCurrentSliderValue():
    return currentSliderValue.get()


#  Slider
slider = ttk.Scale(
    root,
    from_=50,
    to=400,
    value=300,
    orient="horizontal",  # vertical
    variable=currentSliderValue,
    command=slider_changed,
)
slider.place(x=20, y=160, width=228, height=30)

# Frame labels
# Initial image
initImage = tk.Label(root)
initImage["borderwidth"] = 2
initImage.place(x=380, y=70, width=400, height=300)


# Starting GUI
if __name__ == "__main__":
    root.mainloop()
