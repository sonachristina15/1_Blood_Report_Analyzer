import os
import json
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get API key from .env file
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found. Please check your .env file.")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")  # Using a more widely available model

def image_format(image_path):
    """Format image for Gemini API"""
    img = Path(image_path)
    return [{
        "mime_type": "image/jpeg" if str(image_path).lower().endswith((".jpg", ".jpeg")) else "image/png",
        "data": img.read_bytes()
    }]

def analyze_blood_report(image_path):
    """Process the blood report image with Gemini API and return JSON formatted analysis"""
    
    system_prompt = "You are a hematology expert. Analyze this blood test report."
    user_prompt = """Extract the following information from this blood test report:
    
    1. Patient details (name, age, gender, ID)
    2. Test date
    3. The following blood parameters with their values and reference ranges:
       - Hemoglobin (Hb)
       - RBC Count
       - WBC Count
       - Platelet Count
       - HCT, MCV, MCH, MCHC
       - WBC Differential (Neutrophils, Lymphocytes, etc.)
    
    Summarize the findings in simple language. Mention if values are normal or abnormal.
    
    Format your response as a JSON object with the following structure:
    {
        "patient_details": {
            "name": "",
            "age": "",
            "gender": "",
            "id": ""
        },
        "test_date": "",
        "blood_parameters": [
            {"parameter": "Hemoglobin", "value": "", "reference_range": "", "status": "normal/abnormal"},
            ...
        ],
        "summary": [
            "Point 1",
            "Point 2",
            ...
        ],
        "disclaimer": [
            "This analysis is for informational purposes only and does not constitute medical advice.",
            "Please consult with a healthcare professional for proper medical diagnosis and treatment.",
            "Results may vary and this tool cannot substitute for laboratory testing.",
            "This report was generated using AI analysis of an uploaded image.",
            "Some values may not be accurately extracted if the image quality is poor.",
            "Always verify results with your original laboratory report."
        ]
    }
    
    Only return the JSON object without any additional text.
    """

    try:
        image_info = image_format(image_path)
        response = model.generate_content([system_prompt, image_info[0], user_prompt])
        
        # The response should be a JSON string, but we need to extract it
        json_start_idx = response.text.find('{')
        json_end_idx = response.text.rfind('}') + 1
        
        if json_start_idx == -1 or json_end_idx == 0:
            # If JSON format not detected, create a basic error response
            return json.dumps({
                "error": "Could not parse the blood report",
                "raw_response": response.text[:500],  # Only include first 500 chars to avoid issues
                "timestamp": datetime.now().isoformat()
            }, indent=2)
        
        # Extract the JSON portion of the response
        json_response = response.text[json_start_idx:json_end_idx]
        
        # Parse JSON to validate it and add timestamp
        try:
            result = json.loads(json_response)
            # Add timestamp
            result["analysis_timestamp"] = datetime.now().isoformat()
            # Ensure the disclaimer is present
            if "disclaimer" not in result:
                result["disclaimer"] = [
                    "This analysis is for informational purposes only and does not constitute medical advice.",
                    "Please consult with a healthcare professional for proper medical diagnosis and treatment.",
                    "Results may vary and this tool cannot substitute for laboratory testing.",
                    "This report was generated using AI analysis of an uploaded image.",
                    "Some values may not be accurately extracted if the image quality is poor.",
                    "Always verify results with your original laboratory report."
                ]
            return json.dumps(result, indent=2)
        except json.JSONDecodeError:
            return json.dumps({
                "error": "Could not parse JSON response",
                "raw_response": json_response[:500],  # Only include first 500 chars to avoid issues
                "timestamp": datetime.now().isoformat()
            }, indent=2)
            
    except Exception as e:
        return json.dumps({
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }, indent=2)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze blood test report image')
    parser.add_argument('image_path', help='Path to the blood test report image')
    parser.add_argument('--output', '-o', help='Output JSON file path')
    
    args = parser.parse_args()
    
    # Process the image
    result = analyze_blood_report(args.image_path)
    
    # Output results
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
        print(f"Analysis saved to {args.output}")
    else:
        print(result)