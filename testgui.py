# GUI for Line detection by Hough Transform
# DIP semester project
# Branduse, Malin-Dorin and Jimon, Lucian-Daniel

import tkinter as tk
import tkinter.font as tkFont

# Import filedialog explicitly, because of faulty behaviour
from tkinter import filedialog

# Import ttk explicitly, because of faulty behaviour
from tkinter import ttk


class App:
    def __init__(self, root):
        # Setting title
        root.title("Line detection by Hough Transform")
        # Setting window size and characteristics
        width = 800
        height = 600
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = "%dx%d+%d+%d" % (
            width,
            height,
            (screenwidth - width) / 2,
            (screenheight - height) / 2,
        )
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # Buttons

        # Do Line detection button
        performTransformButton = tk.Button(root)
        performTransformButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        performTransformButton["font"] = ft
        performTransformButton["fg"] = "#000000"
        performTransformButton["justify"] = "center"
        performTransformButton["text"] = "Action!"
        performTransformButton.place(x=20, y=200, width=70, height=25)
        performTransformButton["command"] = self.doTransform

        # Browse for image button
        browseImageButton = tk.Button(root)
        browseImageButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        browseImageButton["font"] = ft
        browseImageButton["fg"] = "#000000"
        browseImageButton["justify"] = "center"
        browseImageButton["text"] = "Browse"
        browseImageButton.place(x=20, y=100, width=120, height=25)
        browseImageButton["command"] = self.browseFiles

        # Perform OpenCV-based Line detection
        compareOpenCVButton = tk.Button(root)
        compareOpenCVButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        compareOpenCVButton["font"] = ft
        compareOpenCVButton["fg"] = "#000000"
        compareOpenCVButton["justify"] = "center"
        compareOpenCVButton["text"] = "OpenCV"
        compareOpenCVButton.place(x=20, y=360, width=70, height=25)
        compareOpenCVButton["command"] = self.tranformOpenCV

        # Show histograms button
        histogramButton = tk.Button(root)
        histogramButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        histogramButton["font"] = ft
        histogramButton["fg"] = "#000000"
        histogramButton["justify"] = "center"
        histogramButton["text"] = "Show histograms"
        histogramButton.place(x=100, y=360, width=150, height=25)
        histogramButton["command"] = self.showHistograms

        # Exit GUI
        exitButton = tk.Button(root)
        exitButton["bg"] = "#f0f0f0"
        ft = tkFont.Font(family="Times", size=10)
        exitButton["font"] = ft
        exitButton["fg"] = "#000000"
        exitButton["justify"] = "center"
        exitButton["text"] = "Close application"
        exitButton.place(x=260, y=360, width=120, height=25)
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
        tresholdLabel.place(x=20, y=130, width=231, height=30)

        # Slider current value
        currentSliderValue = tk.DoubleVar()

        # Internal methods for slider event
        def slider_changed(event):
            tresholdLabel.configure(
                text="Hough Treshold = " + str(int(getCurrentSliderValue()))
            )

        def getCurrentSliderValue():
            return currentSliderValue.get()

        #  Slider
        slider = ttk.Scale(
            root,
            from_=50,
            to=700,
            orient="horizontal",  # vertical
            variable=currentSliderValue,
            command=slider_changed,
        )
        slider.place(x=20, y=160, width=228, height=30)

        # Frame labels
        # Initial image
        initImage = tk.Label(root)
        ft = tkFont.Font(family="Times", size=10)
        initImage["font"] = ft
        initImage["fg"] = "#333333"
        initImage["justify"] = "center"
        initImage["text"] = "init1"
        initImage.place(x=380, y=70, width=222, height=165)

        # Result image
        resultImage = tk.Label(root)
        ft = tkFont.Font(family="Times", size=10)
        resultImage["font"] = ft
        resultImage["fg"] = "#333333"
        resultImage["justify"] = "center"
        resultImage["text"] = "result2"
        resultImage.place(x=380, y=240, width=222, height=165)

    # Events for buttons
    # to dos
    def doTransform(self):
        # to do
        print("Hough transform")

    # Function for opening the file explorer window
    def browseFiles(self):
        global openedfile
        openedfile = filedialog.askopenfilename(
            initialdir="/",
            title="Select an Image",
            filetypes=(("Image files", "*.png*"), ("Image files", "*.jpg*")),
        )

        # Change label contents
        # label_file_explorer.configure(text="File Opened: "+ openedfile)
        # Show chosen image
        path = openedfile
        print(path)

    # inImg = image.open(path)

    def tranformOpenCV(self):
        # to do
        print("opencv")

    def showHistograms(self):
        # to do
        print("histograms")


# Starting GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
