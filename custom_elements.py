import math
from dataclasses import dataclass, field
from tkinter import END, Frame, Label, PhotoImage, Scrollbar, StringVar, Text
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
        value = percentage * 100
        if math.floor(value * 10) % 3 == 0:
            logger.info(f"Progress: {percentage:.2%}")
        self.loading['value'] = value
        self.text.set(f"Please wait!, your pdf is loading {percentage:.2%}")


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
    """dimensions of the parent frame (width, height)"""
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
