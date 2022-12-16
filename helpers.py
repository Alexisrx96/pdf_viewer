from tkinter import PhotoImage

from fitz import Page, Pixmap


class ViewerHelper:
    """Utils class for viewer"""

    @staticmethod
    def get_percentage(current_page_num: int, total: int) -> float:
        """Given a page number and a total number of pages,
        return the percentage"""
        return current_page_num / float(total)

    @staticmethod
    def extract_image(page: Page) -> PhotoImage:
        """Converts a page to a photo image and adds transparency
        if necessary"""
        _pix: Pixmap = page.get_pixmap()
        pix = Pixmap(_pix, 0) if _pix.alpha else _pix
        return PhotoImage(data=pix.tobytes("ppm"))
