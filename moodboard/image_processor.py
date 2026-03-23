import cv2
import numpy as np
from PIL import Image, ImageEnhance

class ImageProcessor:
    def __init__(self):
        self.supported_formats = ['.jpg', '.jpeg', '.png']

    def enhance_image(self, image_path):
        """
        Intelligently enhance image quality using adaptive filters and auto-adjustments
        """
        try:
            # Read image using PIL
            img = Image.open(image_path)
            
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Auto-enhance contrast
            enhancer = ImageEnhance.Contrast(img)
            img = enhancer.enhance(1.2)
            
            # Auto-adjust brightness
            brightness = ImageEnhance.Brightness(img)
            img = brightness.enhance(1.1)
            
            # Convert to cv2 format for advanced processing
            cv_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            
            # Apply adaptive bilateral filter for noise reduction while preserving edges
            cv_img = cv2.bilateralFilter(cv_img, 9, 75, 75)
            
            # Apply subtle unsharp mask for sharpening
            gaussian = cv2.GaussianBlur(cv_img, (0, 0), 2.0)
            unsharp_mask = cv2.addWeighted(cv_img, 1.5, gaussian, -0.5, 0)
            
            # Auto white balance
            wb_img = self._auto_white_balance(unsharp_mask)
            
            # Convert back to PIL
            enhanced = Image.fromarray(cv2.cvtColor(wb_img, cv2.COLOR_BGR2RGB))
            return enhanced
            
        except Exception as e:
            raise Exception(f'Image enhancement failed: {str(e)}')

    def _auto_white_balance(self, img):
        """
        Apply automatic white balance correction
        """
        result = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
        avg_a = np.average(result[:, :, 1])
        avg_b = np.average(result[:, :, 2])
        result[:, :, 1] = result[:, :, 1] - ((avg_a - 128) * (result[:, :, 0] / 255.0) * 1.1)
        result[:, :, 2] = result[:, :, 2] - ((avg_b - 128) * (result[:, :, 0] / 255.0) * 1.1)
        return cv2.cvtColor(result, cv2.COLOR_LAB2BGR)

    def is_valid_format(self, filepath):
        """
        Check if image format is supported
        """
        return any(filepath.lower().endswith(fmt) for fmt in self.supported_formats)

    def save_image(self, image, output_path, quality=95):
        """
        Save the processed image
        """
        try:
            image.save(output_path, quality=quality)
            return True
        except Exception as e:
            raise Exception(f'Failed to save image: {str(e)}')