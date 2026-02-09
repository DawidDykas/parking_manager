import os                        
import cv2                       
import numpy as np               
from ultralytics import YOLO
from typing import List, Tuple
import easyocr
from log_config.logger_config import logger


class DetectModels:
    """
    DetectModels - A class for detecting and recognizing vehicle license plates.
    
    This class combines YOLO-based license plate detection with EasyOCR-based
    text recognition to extract plate numbers from images.
    
    Attributes:
        model_car_plates (YOLO): YOLO model for license plate detection
        reader (easyocr.Reader): EasyOCR reader for text recognition
    
    Example:
        >>> detector = DetectModels("models/plate_detector.pt")
        >>> image = cv2.imread("car.jpg")
        >>> plates, plate_images = detector.detection(image)
    """
    
    def __init__(self, detect_car_plates_model_path: str):
        """
        Initialize DetectModels with a YOLO model for plate detection.
        
        Args:
            detect_car_plates_model_path (str): Path to YOLO model weights file
        
        Raises:
            FileNotFoundError: If the specified model file does not exist
        
        Notes:
            - Initializes both YOLO detector and EasyOCR reader
            - Configures logging through the application's logger
        """
        
        logger.info("Initializing DetectModels...")

        if not os.path.exists(detect_car_plates_model_path):
            logger.critical(f"YOLO model for car plates not found at {detect_car_plates_model_path}")
            raise FileNotFoundError(detect_car_plates_model_path)

        self.model_car_plates = YOLO(detect_car_plates_model_path)
        self.reader = easyocr.Reader(['en'])
        logger.info("DetectModels initialized successfully")

    def detect_plates(self, image: np.array) -> Tuple[object, List[np.array], List[float]]:
        """
        Detect license plates in an image using YOLO.
        
        Args:
            image (np.array): Input image in BGR format
            
        Returns:
            Tuple[object, List[np.array], List[float]]: A tuple containing:
                - results: YOLO detection results object
                - plates: List of cropped plate images
                - scores: List of confidence scores for each detection
            
        Notes:
            - Uses confidence threshold of 0.7 and IoU threshold of 0.7
            - Applies preprocessing to each detected plate
            - Returns empty lists if no plates are detected
        """

        logger.debug("Starting plate detection")

        try:
            results = self.model_car_plates.predict(image, conf=0.7, iou=0.7)
        except Exception as e:
            logger.error(f"Failed to run YOLO prediction: {e}")
            return None, [], []

        if results is None or len(results[0].boxes) == 0:
            logger.warning("No plates detected in the image")
            return None, [], [] 

        plates = []
        scores = []

        for idx, box in enumerate(results[0].boxes):
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            
            h, w = image.shape[:2]
            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(w, x2)
            y2 = min(h, y2)

            score = float(box.conf[0])
            logger.debug(f"Box {idx}: ({x1},{y1},{x2},{y2}) with confidence {score:.3f}")

            cropped_plate = self.preprocessing(
                image[y1:y2, x1:x2],
                sigma=3.0,
                erosion_iter=0,
                threshold=0.7
            )
            plates.append(cropped_plate)
            scores.append(score)

        logger.info(f"Detected {len(plates)} plates in the image")
        return results, plates, scores

    def detect_digits_plates(self, image: np.array) -> str:
        """
        Extract text from a license plate image using OCR.
        
        Args:
            image (np.array): Cropped license plate image
            
        Returns:
            str: Extracted plate number as a string
            
        Raises:
            ValueError: If input image does not have 3 channels
            
        Notes:
            - Uses EasyOCR configured for English text
            - Returns empty string if OCR fails
            - Concatenates all detected text segments
        """

        if len(image.shape) != 3:
            logger.error("Wrong image shape for OCR: expected 3 channels")
            raise ValueError("Wrong shape image")

        try:
            result = self.reader.readtext(image)
            plate_number = ''.join([r[1] for r in result])
            logger.debug(f"OCR result: {plate_number}")
            return plate_number
        except Exception as e:
            logger.error(f"OCR failed: {e}")
            return ""

    @staticmethod
    def preprocessing(image: np.array, 
                      kernel_size: Tuple[int, int] = (3,3), 
                      sigma: float = 2.0, 
                      amount: float = 1.5, 
                      threshold: float = 0.7, 
                      erosion_iter: int = 1) -> np.array:
        """
        Preprocess plate image for better OCR results.
        
        Args:
            image (np.array): Input plate image
            kernel_size (Tuple[int, int]): Gaussian blur kernel size (default: (3,3))
            sigma (float): Gaussian blur sigma value (default: 2.0)
            amount (float): Sharpening amount (default: 1.5)
            threshold (float): Low-contrast mask threshold (default: 0.7)
            erosion_iter (int): Number of erosion iterations (default: 1)
            
        Returns:
            np.array: Preprocessed image
            
        Notes:
            - Applies Gaussian blur and unsharp masking
            - Processes each color channel separately
            - Converts grayscale images to BGR if needed
        """

        logger.debug("Starting preprocessing of plate image")

        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        sharpened = np.zeros_like(image)
        for c in range(image.shape[2]):
            channel = image[:, :, c]

            blurred = cv2.GaussianBlur(channel, kernel_size, sigma)
            channel_sharp = float(amount + 1) * channel - float(amount) * blurred
            channel_sharp = np.clip(channel_sharp, 0, 255).astype(np.uint8)

            if threshold > 0:
                low_contrast_mask = np.abs(channel - blurred) < threshold
                np.copyto(channel_sharp, channel, where=low_contrast_mask)

            if erosion_iter > 0:
                kernel = np.ones(kernel_size, np.uint8)
                channel_sharp = cv2.erode(channel_sharp, kernel, iterations=erosion_iter)

            sharpened[:, :, c] = channel_sharp

        logger.debug("Preprocessing completed")
        return sharpened

    def detection(self, image: np.array) -> Tuple[List[str], List[np.array]]:
        """
        Complete pipeline for plate detection and recognition.
        
        Args:
            image (np.array): Input vehicle image
            
        Returns:
            Tuple[List[str], List[np.array]]: A tuple containing:
                - List of recognized plate numbers (strings)
                - List of cropped plate images
                
        Notes:
            - Executes both detection and recognition steps
            - Returns empty lists if pipeline fails
            - Handles exceptions for individual plate recognition
        """

        logger.info("Starting full detection pipeline")
        try:
            results, plates_images, scores = self.detect_plates(image=image)
        except Exception as e:
            logger.error(f"Detection pipeline failed: {e}")
            return [], []

        plates_list = []
        for idx, plate in enumerate(plates_images):
            try:
                plate_number = self.detect_digits_plates(plate)
                plates_list.append(plate_number)
            except Exception as e:
                logger.warning(f"Failed to recognize plate {idx}: {e}")
                plates_list.append("")

        logger.info(f"Detection pipeline completed: {len(plates_list)} plates processed")
        return plates_list, plates_images