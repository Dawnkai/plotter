import cv2


class Extractor:
    """
    This module extracts contours from image for later drawing.
    :param @limit_x: Amount of pixels in X axis
    :param @limit_y: Amount of pixels in Y axis
    :param @filepath: Filepath of the image to extract from
    :param @thresh_low: Lower threshold of pixels to extract
    :param @thresh_high: Upper threshold of pixels to extract
    """

    def __init__(self, limit_x = 220, limit_y = 130, filepath = "", thresh_low = 100, thresh_high = 200):
        self.thresh_hi = thresh_high
        self.thresh_low = thresh_low
        self.limit_x = limit_x
        self.limit_y = limit_y
        self.filepath = filepath
    

    def set_filepath(self, filepath):
        self.filepath = filepath


    def load_image(self):
        """
        Load image from specified file. Resize it to match the X and Y axis limits,
        convert it to grayscale and apply Canny filtering to extract initial lines based
        on the thresholds supplied to the constructor.
        """
        self.image = cv2.imread(self.filepath)
        self.image = cv2.resize(self.image, (self.limit_x, self.limit_y), interpolation=cv2.INTER_AREA)
        self.gray_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        self.edges = cv2.Canny(self.gray_image, self.thresh_low, self.thresh_hi)
    

    def get_contours(self):
        """
        Find contours in the image and return it as an 2d array of contours.
        """
        self.load_image()
        contours, _ = cv2.findContours(image=self.edges, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        return contours

