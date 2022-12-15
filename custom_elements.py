import math
from dataclasses import dataclass, field
from tkinter import Frame, Label, PhotoImage, Scrollbar, StringVar, Text
from tkinter.ttk import Progressbar

from logger import logger


@dataclass
class ProgressbarElement:
    """Progressbar with its own Progress label."""
    text: StringVar
    """Text to display progress"""
    label: Label
    """Label to display progress"""
    loading: Progressbar
    """Progressbar"""
    progress: int = field(default=0, init=False)
    """Progress counter"""

    def forget(self):
        """Remove progressbar and label."""
        logger.info("Removing progressbar")
        self.loading.pack_forget()
        self.label.pack_forget()

    def update(self, percentage: float):
        """Update the progressbar percentage values and update the label."""
        if int(percentage * 10) % 100 == 0:
            logger.info(f"Progress: {percentage:.2f}%")
        self.loading['value'] = percentage
        self.text.set("Please wait!, your pdf is loading "
                      f"{math.floor(percentage)}%")


@dataclass
class PDFViewerFrame:

    frame: Frame
    """Parent frame"""
    pdf_location: str
    """Path to PDF file"""
    has_loading_bar: bool = field(default=True)
    """Displays loading bar at the top of the parent frame"""

    pdf_container: Text = field(init=False, default=None)
    """Container for the PDF images"""
    scrolls: tuple[Scrollbar, Scrollbar] = field(init=False,
                                                 default_factory=tuple)
    """Scroll bars for the PDF container"""
    dimensions: tuple[int, int] = field(init=False)
    """dimensions of the parent frame"""
    progressbar: ProgressbarElement = field(init=False, default=None)
    """Progressbar element"""
    pages: list[PhotoImage] = field(default_factory=list, init=False)
    """Store pdf images"""

    def __post_init__(self):
        self.dimensions = self.frame['width'], self.frame['height']

    def forget(self):
        """Remove progressbar and label."""
        logger.info("Removing progressbar")
        for scroll in self.scrolls:
            scroll.destroy()
        if self.pdf_container:
            self.pdf_container.destroy()
        if self.progressbar:
            self.progressbar.forget()
