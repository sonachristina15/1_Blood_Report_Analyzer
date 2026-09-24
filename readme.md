# Blood Report Analyzer

## Overview

This repository contains an **AI-powered web application for structured blood report processing** developed using Flask and the Google Gemini API.

The application accepts a blood report image, sends the image to a multimodal AI model for information extraction, processes the returned response into structured data, displays the extracted information through a web interface, and generates a downloadable PDF report.

The primary focus of the project is **AI application integration and structured document processing**, rather than medical diagnosis.

The project demonstrates:

* Multimodal AI API integration
* Image-based document processing
* Structured JSON extraction
* Flask backend development
* Frontend and backend integration
* Automated PDF report generation
* Temporary file handling
* Environment-based API key management

---

## Project Architecture

```text
Blood Report Image
        ↓
Flask Web Application
        ↓
File Validation & Temporary Processing
        ↓
Google Gemini API
        ↓
Structured JSON Response
        ↓
Application-Level Processing
        ↓
Web Interface
        ↓
PDF Report Generation
        ↓
Downloadable Report
```

---

## Problem Statement

Blood reports contain structured and semi-structured information that can be difficult to process programmatically when provided as images.

The project explores how a multimodal AI model can be integrated into a web application to convert information from a blood report image into a structured format that can then be processed and presented consistently.

Instead of treating the application as a diagnostic system, the project focuses on the **engineering workflow required to connect image input, AI processing, structured output, web presentation, and document generation**.

---

## Input

The application accepts blood report images in the following formats:

* JPG
* JPEG
* PNG

The uploaded image is temporarily stored during processing and removed after the analysis is completed.

---

## AI Processing

The uploaded blood report image is processed using the **Google Gemini API**.

A structured prompt is used to request information in JSON format.

The extracted information includes:

* Patient details
* Test date
* Blood parameters
* Summary
* Disclaimer

The application parses the model response and converts it into structured JSON data before returning it to the frontend.

---

## Structured Output

The AI response is processed into a structured format containing fields such as:

```text
patient_details
test_date
blood_parameters
summary
disclaimer
analysis_timestamp
```

This structured approach allows the application to use the model response programmatically rather than displaying an unprocessed text response.

---

## Web Application

The application is built using **Flask**.

The backend handles:

* Blood report image uploads
* File type validation
* Temporary file creation
* Gemini API processing
* Structured response handling
* PDF generation
* PDF download

The frontend uses **HTML, CSS, and JavaScript** to provide the upload interface, display the processed results, and initiate PDF downloads.

---

## PDF Report Generation

The structured analysis is converted into a PDF report using **FPDF2**.

The generated report contains:

* Patient details
* Test date
* Blood parameters
* Analysis summary
* Disclaimer
* Report generation timestamp

Generated PDF files are stored temporarily in the `generated_reports/` directory.

This directory is excluded from version control using `.gitignore`.

---

## Technologies Used

* Python
* Flask
* Google Gemini API
* HTML
* CSS
* JavaScript
* FPDF2
* python-dotenv

---

## Requirements

* Python
* Flask
* Google Gemini API access
* `google-generativeai`
* `python-dotenv`
* `Pillow`
* `fpdf2`

---

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root and configure the Gemini API key:

```text
GOOGLE_API_KEY=your_api_key_here
```

The `.env` file is excluded from Git using `.gitignore`.

---

## Running the Application

Start the Flask application:

```powershell
python app.py
```

The application runs locally at:

```text
http://127.0.0.1:5000
```

Open the address in a web browser and upload a supported blood report image.

---

## Repository Files

```text
.
├── static/
│   ├── css/
│   │   └── blood_report.css
│   └── js/
│       └── blood_report.js
├── templates/
│   └── blood_report.html
├── .gitignore
├── app.py
├── blood_pdf_generator.py
├── blood_report_analyser.py
├── requirements.txt
└── readme.md
```

---

## Security

The Gemini API key is stored using an environment variable rather than directly in the source code.

The following files and directories are excluded from Git:

```text
.env
.venv/
__pycache__/
generated_reports/
*.pdf
```

---

## Project Scope

This repository focuses on the **AI and application-integration layer** of the project:

1. Accept a blood report image
2. Validate the uploaded file
3. Temporarily process the image
4. Send the image to a multimodal AI model
5. Extract structured information from the model response
6. Display the structured results through the web interface
7. Generate a PDF report
8. Provide the generated report for download

The project does **not** attempt to replace medical professionals or provide medical diagnosis.

---

## Limitations

The application depends on the capabilities and responses of the external Gemini API.

The extracted information may require verification against the original report.

The project currently focuses on image-based blood report processing and does not implement an independent medical reasoning or diagnostic engine.

---

## Disclaimer

This application is intended for **educational and demonstration purposes only**.

The generated information is not medical advice and should not be considered a medical diagnosis.

Users should consult a qualified healthcare professional for interpretation of medical reports and medical decisions.

---

## Project Status

**Completed**

The Flask-based Blood Report Analyzer has been implemented and tested.

The application successfully:

* Accepts supported blood report images
* Validates uploaded files
* Performs AI-based information extraction using the Gemini API
* Processes the response into structured JSON
* Displays the extracted information through the web interface
* Generates PDF reports
* Provides generated PDF reports for download

This project demonstrates the integration of a multimodal AI API into an end-to-end web application for structured document processing.
