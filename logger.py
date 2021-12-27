import logging

def setup_logger():
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()

    fileHandler = logging.FileHandler("plotter.log")
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.INFO)
    logger.addHandler(consoleHandler)
