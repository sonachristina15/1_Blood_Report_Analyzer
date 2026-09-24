# Blood Report Analyzer

An AI-powered web application that analyzes blood report images and generates a structured analysis and downloadable PDF report.

## Overview

The Blood Report Analyzer allows a user to upload a blood report image through a Flask web application. The uploaded report is analyzed using the Gemini API, and the extracted information is displayed in the browser.

The application also generates a PDF report containing the analyzed information.

## Features

- Upload blood report images in JPG, JPEG, or PNG format
- AI-based blood report analysis using Gemini
- Extract patient details and blood parameters
- Display analysis results through a web interface
- Generate a downloadable PDF report
- Temporary processing of uploaded images
- API key stored using environment variables

## How It Works

```text
User
  ↓
Upload Blood Report Image
  ↓
Flask Web Application
  ↓
Gemini API
  ↓
Structured Analysis
  ↓
Display Results
  ↓
Generate PDF Report
  ↓
Download PDF