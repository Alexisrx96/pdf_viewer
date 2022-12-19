from threading import Thread
from tkinter import (BOTH, BOTTOM, DISABLED, HORIZONTAL, LEFT, RIGHT, TOP,
                     VERTICAL, PhotoImage, StringVar, Text, X, Y)
from tkinter.ttk import Label, Progressbar, Scrollbar

from fitz import Document, Page

from custom_elements import PDFViewerFrame, ProgressbarElement
from protocols import ViewerHelperProtocol
from logger import logger


class PDFViewerFrameBuilder:
    """Builder for creating a 'PDFViewerFrame'"""

    def __init__(self, viewer_helper: ViewerHelperProtocol) -> None:
        self.helper = viewer_helper

    def __update_progressbar(self, viewer: PDFViewerFrame, total: int):
        """Determinate progress bar progress"""
        if not viewer.progressbar:
            return
        viewer.progressbar.progress += 1
        percentage = self.helper.get_percentage(viewer.progressbar.progress,
                                                total)
        if percentage > 100:
            logger.warning(f'More than 100 ({percentage:.2%})')
            return
        viewer.progressbar.update(percentage)

    def add_scrollbar(self, viewer: PDFViewerFrame):
        """Add scroll bars to the viewer"""
        if viewer.scrolls:
            return self
        logger.info("getting scroll bars...")
        scroll_y = Scrollbar(viewer.frame, orient=VERTICAL)
        scroll_x = Scrollbar(viewer.frame, orient=HORIZONTAL)

        scroll_x.pack(fill=X, side=BOTTOM)
        scroll_y.pack(fill=Y, side=RIGHT)
        viewer.scrolls = scroll_x, scroll_y
        return self

    def add_progressbar(self, viewer: PDFViewerFrame):
        if not viewer.has_loading_bar or viewer.progressbar:
            return self
        logger.info("creating variable...")
        percentage_str = StringVar()

        logger.info("creating label...")
        display_msg = Label(textvariable=percentage_str)
        display_msg.pack(pady=10)

        logger.info("creating progress bar...")
        loading = Progressbar(
            viewer.frame,
            orient=HORIZONTAL,
            length=100,
            mode='determinate',
        )
        loading.pack(side=TOP, fill=X)
        logger.info("returning progressbar element...")
        viewer.progressbar = ProgressbarElement(percentage_str, display_msg,
                                                loading)
        return self

    def add_container(self, viewer: PDFViewerFrame):
        if viewer.pdf_container:
            return self
        width, height = viewer.dimensions
        scroll_x, scroll_y = viewer.scrolls
        logger.info("creating pdf container...")
        container = Text(
            viewer.frame,
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            width=width,
            height=height,
        )

        container.configure(state=DISABLED, cursor='arrow')
        scroll_x.config(command=container.xview)
        scroll_y.config(command=container.yview)
        container.pack(
            side=LEFT,
            fill=BOTH,
        )
        viewer.pdf_container = container
        return self

    def __read_page(self,
                    viewer: PDFViewerFrame,
                    total: int,
                    page: Page,
                    zoom_ratio: float = 1) -> PhotoImage:
        viewer.dimensions
        _page = self.helper.extract_image(page,
                                          zoom_ratio,
                                          zoom_ratio,
                                          offsets=(0.05, 0))
        viewer.pages.append(_page)
        if viewer.has_loading_bar:
            self.__update_progressbar(viewer, total)
        return _page

    def __fill_container(self, viewer: PDFViewerFrame):
        open_pdf = Document(viewer.pdf_location)

        if not open_pdf:
            return
        zoom_ratio = (self.helper.get_zoom_ratio(viewer.dimensions[0],
                                                 open_pdf[0])
                      if viewer.fit_page_to_container else 1)
        total = len(open_pdf)
        for page in open_pdf:
            image = self.__read_page(viewer, total, page, zoom_ratio)
            viewer.add_image(image)

        if viewer.progressbar:
            viewer.progressbar.forget()
            viewer.progressbar = None

    def __filler(self, viewer: PDFViewerFrame):
        t1 = Thread(target=lambda: self.__fill_container(viewer))
        t1.start()

    def fill(self, viewer: PDFViewerFrame):
        if not viewer.has_loading_bar:
            self.__filler(viewer)
            return
        viewer.frame.master.after(250, lambda: self.__filler(viewer))

    def build(self, viewer: PDFViewerFrame):
        logger.info("starting...")
        logger.info("loading bar: %s" % viewer.has_loading_bar)
        self.add_scrollbar(viewer)\
            .add_progressbar(viewer)\
            .add_container(viewer)\
            .fill(viewer)
