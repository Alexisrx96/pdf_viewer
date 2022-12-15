import math
from dataclasses import dataclass, field
from tkinter import Label, StringVar
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
