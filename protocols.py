from tkinter import PhotoImage
from typing import Protocol

from fitz import Page


class ViewerHelperProtocol(Protocol):

    def get_percentage(self, current_page_num: int, total: int) -> float:
        ...

    def extract_image(self,
                      page: Page,
                      zoom_x: float,
                      zoom_y: float,
                      offsets: tuple[float, float] = ...) -> PhotoImage:
        ...

    def get_zoom_ratio(self, width: int, page: Page) -> float:
        ...
