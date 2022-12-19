# Importing tkinter to make gui in python
from tkinter import Frame, Tk
from tkinter import filedialog as fd

# Importing tkPDFViewer to place pdf file in gui.
# In tkPDFViewer library there is
# an tkPDFViewer module. That I have imported as pdf
from custom_elements import PDFViewerFrame
from helpers import ViewerHelper
from viewer import PDFViewerFrameBuilder


def main():
    # Initializing tk

    root = Tk()

    width, height = int(root.winfo_screenwidth() / 2), 600

    # Set the width and height of our root window.
    root.geometry(f"{width}x{height}")

    # creating object of ShowPdf from tkPDFViewer.
    frame = Frame(root, width=width, height=height, bg="white")

    name = fd.askopenfilename(filetypes=(('pdf', '*.pdf'), ), initialdir='/')

    viewer = PDFViewerFrame(frame, pdf_location=name, has_loading_bar=False)

    # Adding pdf location and width and height.
    PDFViewerFrameBuilder(ViewerHelper).build(viewer)

    # Placing Pdf in my gui.
    viewer.frame.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
