from flask import Flask, render_template, request, jsonify, send_file
from pathlib import Path
from datetime import datetime
import tempfile
import os
import traceback

from blood_report_analyser import analyze_blood_report
from blood_pdf_generator import blood_pdf


app = Flask(__name__)

# Folder to store generated PDF reports
PDF_FOLDER = Path("generated_reports")
PDF_FOLDER.mkdir(exist_ok=True)


@app.route("/")
def home():
    return render_template("blood_report.html")


@app.route("/blood-report")
def blood_report():
    return render_template("blood_report.html")


@app.route("/process-blood", methods=["POST"])
def process_blood():
    # Check whether a file was uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Blood analyzer currently works with image files
    allowed_extensions = {".jpg", ".jpeg", ".png"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        return jsonify({
            "error": "Unsupported file type. Please upload JPG, JPEG, or PNG."
        }), 400

    temp_path = None

    try:
        # Save uploaded image temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension
        ) as temp_file:
            file.save(temp_file.name)
            temp_path = temp_file.name

        # Analyze blood report using Gemini
        analysis = analyze_blood_report(temp_path)

        print("\n--- GEMINI ANALYSIS ---")
        print(analysis)
        print("--- END ANALYSIS ---\n")

        # Create PDF filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_filename = f"blood_report_analysis_{timestamp}.pdf"
        pdf_path = PDF_FOLDER / pdf_filename

        # Generate PDF
        print("PDF GENERATION START")

        blood_pdf(
            analysis,
            output_path=str(pdf_path)
        )
    

        print("PDF GENERATION SUCCESS")
        print("PDF PATH:", pdf_path)
        print("RETURNING JSON RESPONSE")

        # Send analysis + PDF filename to frontend
        return jsonify({
            "analysis_data": analysis,
            "pdf_filename": pdf_filename
        })

    except Exception as e:
        print("\n--- ERROR TRACEBACK ---")
        traceback.print_exc()
        print("--- END TRACEBACK ---")
        return jsonify({"error": str(e)}), 500

    finally:
        # Delete temporary uploaded image
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@app.route("/download/<filename>")
def download_report(filename):
    pdf_path = PDF_FOLDER / filename

    if not pdf_path.exists():
        return jsonify({
            "error": "PDF report not found."
        }), 404

    return send_file(
        pdf_path,
        as_attachment=True,
        download_name=pdf_path.name
    )


if __name__ == "__main__":
    app.run(debug=True)