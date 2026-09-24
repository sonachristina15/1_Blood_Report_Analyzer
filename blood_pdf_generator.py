import json
import argparse
from datetime import datetime
from fpdf import FPDF
import os
from blood_report_analyser import analyze_blood_report


class BloodReportPDF(FPDF):

    def header(self):
        # Set font
        self.set_font('Arial', 'B', 16)

        # Move to the right
        self.cell(80)

        # Title
        self.cell(30, 10, 'Blood Test Report Analysis', 0, 0, 'C')

        # Line break
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)

        # Arial italic 8
        self.set_font('Arial', 'I', 8)

        # Page number
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 6, title, 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 5, body)
        self.ln()

    def add_patient_details(self, patient_details):
        self.chapter_title("Patient Details")

        if patient_details.get("name"):
            self.set_font('Arial', 'B', 10)
            self.cell(30, 6, "Name:", 0, 0)

            self.set_font('Arial', '', 10)
            self.cell(
                0,
                6,
                patient_details.get("name", "N/A"),
                0,
                1
            )

        if patient_details.get("age") or patient_details.get("gender"):
            self.set_font('Arial', 'B', 10)
            self.cell(30, 6, "Age/Gender:", 0, 0)

            self.set_font('Arial', '', 10)

            age_gender = (
                f"{patient_details.get('age', 'N/A')} / "
                f"{patient_details.get('gender', 'N/A')}"
            )

            self.cell(0, 6, age_gender, 0, 1)

        if patient_details.get("id"):
            self.set_font('Arial', 'B', 10)
            self.cell(30, 6, "Patient ID:", 0, 0)

            self.set_font('Arial', '', 10)
            self.cell(
                0,
                6,
                patient_details.get("id", "N/A"),
                0,
                1
            )

        self.ln(4)

    def add_test_date(self, test_date):
        if test_date:
            self.set_font('Arial', 'B', 10)
            self.cell(30, 6, "Test Date:", 0, 0)

            self.set_font('Arial', '', 10)
            self.cell(0, 6, test_date, 0, 1)

            self.ln(4)

    def add_blood_parameters(self, blood_parameters):
        self.chapter_title("Blood Parameters")

        # Table header
        self.set_font('Arial', 'B', 10)

        self.cell(60, 7, "Parameter", 1, 0, 'C')
        self.cell(30, 7, "Value", 1, 0, 'C')
        self.cell(60, 7, "Reference Range", 1, 0, 'C')
        self.cell(40, 7, "Status", 1, 1, 'C')

        # Table data
        self.set_font('Arial', '', 10)

        for param in blood_parameters:

            # Handle possible line breaks in parameter names
            if len(param["parameter"]) > 30:
                self.cell(
                    60,
                    7,
                    param["parameter"][:30] + "...",
                    1,
                    0
                )
            else:
                self.cell(
                    60,
                    7,
                    param["parameter"],
                    1,
                    0
                )

            self.cell(
                30,
                7,
                param.get("value", "N/A"),
                1,
                0,
                'C'
            )

            self.cell(
                60,
                7,
                param.get("reference_range", "N/A"),
                1,
                0,
                'C'
            )

            # Color-code the status
            status = param.get("status", "").lower()

            if status == "abnormal":
                self.set_text_color(255, 0, 0)

                self.cell(
                    40,
                    7,
                    "ABNORMAL",
                    1,
                    1,
                    'C'
                )

                self.set_text_color(0, 0, 0)

            else:
                self.set_text_color(0, 128, 0)

                self.cell(
                    40,
                    7,
                    "NORMAL",
                    1,
                    1,
                    'C'
                )

                self.set_text_color(0, 0, 0)

        self.ln(4)

    def add_summary(self, summary):
        self.chapter_title("Summary")

        for idx, point in enumerate(summary, 1):
            self.set_font('Arial', '', 10)

            bullet_point = f"{idx}. {point}"

            # Explicit width to prevent FPDF horizontal-space error
            self.multi_cell(180, 6, bullet_point)

        self.ln(4)

    def add_disclaimer(self, disclaimer):
        self.chapter_title("Disclaimer")

        self.set_font('Arial', 'I', 10)
        self.set_text_color(128, 128, 128)

        for idx, point in enumerate(disclaimer, 1):

            # Explicit width to prevent FPDF horizontal-space error
            self.multi_cell(
                180,
                5,
                f"{idx}. {point}"
            )

        self.set_text_color(0, 0, 0)

        self.ln(4)


def blood_pdf(json_data, output_path=None):
    """Generate a PDF report from the blood test analysis JSON data"""

    # Parse JSON if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data

    # Create PDF
    pdf = BloodReportPDF()

    pdf.alias_nb_pages()

    pdf.add_page()

    # Add generation time
    pdf.set_font('Arial', 'I', 10)

    pdf.cell(
        0,
        10,
        f"Generated on: "
        f"{datetime.now().strftime('%B %d, %Y, %H:%M')}",
        0,
        1
    )

    pdf.ln(4)

    # Add patient details
    if "patient_details" in data:
        pdf.add_patient_details(
            data["patient_details"]
        )

    # Add test date
    if "test_date" in data:
        pdf.add_test_date(
            data["test_date"]
        )

    # Add blood parameters
    if "blood_parameters" in data:
        pdf.add_blood_parameters(
            data["blood_parameters"]
        )

    # Add summary
    if "summary" in data:
        pdf.add_summary(
            data["summary"]
        )

    # Add disclaimer
    if "disclaimer" in data:
        pdf.add_disclaimer(
            data["disclaimer"]
        )

    # Output PDF
    if output_path:

        pdf.output(output_path)

        return output_path

    else:

        # Generate default filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

        output_file = (
            f"blood_report_analysis_{timestamp}.pdf"
        )

        pdf.output(output_file)

        return output_file


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description='Generate PDF for blood test report analysis'
    )

    parser.add_argument(
        '--image',
        help='Path to blood test report image'
    )

    parser.add_argument(
        '--json',
        help='Path to JSON analysis file (alternative to image)'
    )

    parser.add_argument(
        '--output',
        '-o',
        help='Output PDF file path'
    )

    args = parser.parse_args()

    if args.image:

        # Analyze image and generate JSON
        json_data = analyze_blood_report(
            args.image
        )

    elif args.json:

        # Load existing JSON file
        with open(args.json, 'r') as f:
            json_data = f.read()

    else:

        print(
            "Error: Either --image or --json must be provided"
        )

        parser.print_help()

        exit(1)

    # Generate PDF
    output_file = blood_pdf(
        json_data,
        args.output
    )

    print(
        f"PDF report generated: {output_file}"
    )