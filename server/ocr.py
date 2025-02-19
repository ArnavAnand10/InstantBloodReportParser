import re
import spacy
import pandas as pd
import pytesseract
import numpy as np
from PIL import Image
import cv2
from typing import Dict, List, Optional
from spacy.matcher import Matcher, PhraseMatcher

class BloodTestImageExtractor:
    def __init__(self):
        # Load spaCy English model
        self.nlp = spacy.load('en_core_web_sm')
        
        # Initialize matchers
        self.matcher = Matcher(self.nlp.vocab)
        
        # Updated test components based on the image
        self.test_components = {
            'Hemoglobin': ['g/dL'],
            'RBC': ['10^6/uL'],
            'HCT': ['%'],
            'MCV': ['fl'],
            'MCH': ['pg'],
            'MCHC': ['g/dL'],
            'RDW-CV': ['%'],
            'RDW-SD': ['fl'],
            'WBC': ['10^3/uL'],
            'NEU%': ['%'],
            'LYM%': ['%'],
            'MON%': ['%'],
            'EOS%': ['%'],
            'BAS%': ['%'],
            'LYM#': ['10^3/uL'],
            'GRA#': ['10^3/uL'],
            'PLT': ['10^3/uL'],
            'ESR': ['mm/hr']
        }
        
        self._add_patterns()

    def _add_patterns(self):
        """Add patterns for matching test components and their values"""
        for component in self.test_components.keys():
            # Pattern to match test name followed by number
            pattern = [
                {'LOWER': component.lower()},
                {'IS_SPACE': True, 'OP': '?'},
                {'IS_PUNCT': True, 'OP': '?'},
                {'IS_SPACE': True, 'OP': '?'},
                {'LIKE_NUM': True}
            ]
            self.matcher.add(f"pattern_{component}", [pattern])

    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess the image for better OCR results
        """
        # Read image
        image = cv2.imread(image_path)
        
        # Convert to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Apply thresholding
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Apply denoising
        denoised = cv2.fastNlMeansDenoising(binary)
        
        return denoised

    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from image using OCR with custom configuration
        """
        # Preprocess image
        preprocessed_image = self.preprocess_image(image_path)
        
        # Custom OCR configuration
        custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
        
        # Extract text
        text = pytesseract.image_to_string(preprocessed_image, config=custom_config)
        
        return text

    def extract_values(self, text: str) -> Dict[str, Dict]:
        """
        Extract test values and ranges from the text
        """
        results = {}
        
        # Split text into lines
        lines = text.split('\n')
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
                
            # Look for test components
            for component in self.test_components.keys():
                if component.lower() in line.lower():
                    # Extract numeric values using regex
                    numbers = re.findall(r'-?\d*\.?\d+', line)
                    if numbers:
                        try:
                            value = float(numbers[0])
                            
                            # Extract range if available
                            range_values = None
                            if len(numbers) >= 3:
                                range_values = f"{numbers[1]}-{numbers[2]}"
                            elif len(numbers) >= 2:
                                range_values = numbers[1]
                                
                            results[component] = {
                                'value': value,
                                'range': range_values,
                                'unit': self.test_components[component][0]
                            }
                        except ValueError:
                            continue
        
        return results

    def process_image(self, image_path: str) -> pd.DataFrame:
        """
        Process a blood test report image and return formatted results
        """
        # Extract text from image
        text = self.extract_text_from_image(image_path)
        
        # Extract values and ranges
        results = self.extract_values(text)
        
        # Create DataFrame
        df = pd.DataFrame(columns=['Component', 'Value', 'Normal Range', 'Units', 'Status'])
        
        for component, data in results.items():
            value = data['value']
            range_str = data['range']
            unit = data['unit']
            
            # Determine status
            status = 'Normal'
            if range_str:
                try:
                    range_parts = range_str.split('-')
                    if len(range_parts) == 2:
                        low, high = map(float, range_parts)
                        if value < low:
                            status = 'Low'
                        elif value > high:
                            status = 'High'
                except ValueError:
                    status = 'Unknown'
            
            # Add to DataFrame
            df = pd.concat([df, pd.DataFrame({
                'Component': [component],
                'Value': [value],
                'Normal Range': [range_str],
                'Units': [unit],
                'Status': [status]
            })])
        
        return df.reset_index(drop=True)

def main():
    # Initialize extractor
    extractor = BloodTestImageExtractor()
    
    # Process image
    image_path = "sample.jpg"  # Replace with your image path
    
    try:
        results = extractor.process_image(image_path)
        
        # Display results
        print("\nBlood Test Results:")
        print(results.to_string(index=False))
        
        # Save results to CSV
        results.to_csv("blood_test_results.csv", index=False)
        
    except Exception as e:
        print(f"Error processing image: {str(e)}")

if __name__ == "__main__":
    main()