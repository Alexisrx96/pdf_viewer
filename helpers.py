from tkinter import PhotoImage

from fitz import Matrix, Page, Pixmap


class ViewerHelper:
    """Utils class for viewer"""

    @staticmethod
    def get_percentage(current_page_num: int, total: int) -> float:
        """Given a page number and a total number of pages,
        return the percentage"""
        return current_page_num / float(total)

    @staticmethod
    def extract_image(page: Page, zoom_x: float, zoom_y: float) -> PhotoImage:
        """Converts a page to a photo image and adds transparency
        if necessary"""
        mat = Matrix(zoom_x, zoom_y)
        _pix: Pixmap = page.get_pixmap(matrix=mat)
        pix = Pixmap(_pix, 0) if _pix.alpha else _pix
        return PhotoImage(data=pix.tobytes("ppm"))

    @classmethod
    def get_zoom_ratio(cls, width: int, page: Page) -> float:
        image = cls.extract_image(page, 1, 1)
        return width / image.width()
