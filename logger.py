import logging

logger = logging.getLogger('Pdf_viewer')
format = logging.Formatter('%(asctime)s %(message)s')
stream = logging.StreamHandler()
file = logging.FileHandler("./logs.log")
stream.setFormatter(format)
stream.setLevel(logging.INFO)
file.setFormatter(format)
file.setLevel(logging.INFO)
logger.setLevel(logging.INFO)
logger.addHandler(stream)
logger.addHandler(file)
