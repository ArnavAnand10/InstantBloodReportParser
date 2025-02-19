import fitz  # PyMuPDF
import re
import spacy
import json
from langchain_google_vertexai import ChatVertexAI
from langchain_core.prompts import PromptTemplate
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/arnav-anand/Downloads/daring-atrium-448311-p9-bb3f69b98364.json"

# Load spaCy model for NLP
nlp = spacy.load("en_core_web_sm")
llm = ChatVertexAI(model="gemini-1.5-flash")

# Predefined list of medical terms to help standardize the test names
medical_terms = [
    "Hemoglobin", "WBC Count", "RBC", "Platelet Count", "Mean Cell Hb Conc (MCHC)", 
    "Red Cell Dist Width (RDW)", "Mean Platelet Volume", "WBC Differential", 
    "Neutrophil", "Lymphocyte", "Monocyte", "Eosinophil", "Basophil", 
    "Neutrophil, Absolute", "Lymphocyte, Absolute", "Monocyte, Absolute", 
    "Eosinophil, Absolute", "Basophil, Absolute", "Glucose", "Cholesterol", 
    "Creatinine", "Urea", "Sodium", "Potassium"
]

# Regex pattern for medical values with optional units (including g/dL, %)
medical_value_pattern = re.compile(
    r"([\w\s\(\)-]+?)\s*[:\-]?\s*([\d.,]+)\s*([a-zA-Z/%µμK/mcLfL]*)"
)

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF using PyMuPDF."""
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text("text") for page in doc)
    return text

def clean_test_name(test_name):
    """Standardize the test name by matching it against predefined medical terms."""
    test_name = test_name.strip()
    
    # Match the test name with predefined medical terms
    for term in medical_terms:
        if term.lower() in test_name.lower():
            return term  # Return the correct standardized name
    
    return None  # If no match, return None to filter it out

def extract_medical_values(text):
    """Extract medical test names, values, and units from the text."""
    extracted_values = {}

    for match in medical_value_pattern.finditer(text):
        test_name, value, unit = match.groups()
        test_name = clean_test_name(test_name)  # Standardize test name

        # Skip if the test name doesn't match a medical term
        if not test_name or len(test_name) <= 2 or not value:
            continue

        # Remove non-medical or irrelevant text from values
        if test_name:
            # Filter out irrelevant medical abbreviations (e.g., units like "mm")
            unit = unit.strip().lower() if unit else "N/A"
            extracted_values[test_name] = {"value": value, "unit": unit}

    return extracted_values

def format_extracted_data(extracted_data):
    """Convert extracted data into structured JSON format."""
    return json.dumps(extracted_data, indent=4, ensure_ascii=False)

def extractRelevantDataWithStandardUnits(text: str):
    # Modify the prompt to ensure the output is strictly in JSON format with arrays and includes the "summary" key
    prompt_template = PromptTemplate.from_template("""
You are a specialized medical information extractor. Given the input text below, your task is to:
1. **Extract Relevant Data**:
   - Identify medical test names, values, and units from the input text.
   - Extract only meaningful test results while filtering out irrelevant data.

2. **Standardize Data**:
   - Convert extracted test names into their standardized medical terminology.
   - Ensure values are formatted correctly.
   - Convert measurement units into their HL7 standard equivalents.

3. **Interpret Results & Provide Summary**:
   - Analyze extracted values and indicate whether they fall within normal, low, or high ranges based on standard reference values.
   - Add a **"reference_range"** field for each test to indicate the normal range of values.
   - Add a **"status"** field with one of the following: 
     - **"Low"** (if below normal)
     - **"Normal"** (if within normal range)
     - **"High"** (if above normal)
   - Provide a brief, medically relevant summary highlighting any abnormal findings, trends, or concerns.
   - If possible, suggest potential implications based on observed deviations (e.g., high glucose may indicate diabetes risk).

4. **Strict JSON Format Output**:
   - Return the extracted data strictly in JSON format with an array of objects, each containing the following keys:
     - **"test_name"**: Standardized medical test name.
     - **"value"**: Numeric value of the test.
     - **"unit"**: Standardized HL7 unit.
     - **"reference_range"**: Normal reference range for the test.
     - **"status"**: Categorization as **"Low"**, **"Normal"**, or **"High"** based on the value.
   - Include a **"summary"** key with a brief interpretation of the overall results.
   - The output should be an array of JSON objects with each test result and a "summary" key at the end, containing the overall interpretation.

### Input Text:
{input_text}

### Expected Output:
Provide the extracted data as a valid JSON array of objects, each containing the keys above. Ensure that the final output is a single JSON array with a summary key at the end.
""")

    prompt = prompt_template.invoke({"input_text": text})
    return llm.invoke(prompt).content

def print_extracted_data(extracted_data):
    """Print the extracted data in a readable format."""
    data = json.loads(extracted_data)  # Convert the JSON string back to a Python dictionary
    for test_name, info in data.items():
        value = info.get("value", "N/A")
        unit = info.get("unit", "N/A")
        print(f"{test_name}: {value} {unit}")

# 🔹 Provide your PDF file path here


# 🔹 Extract and process the blood test report



# 🔹 Print the extracted results


