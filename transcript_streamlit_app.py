import streamlit as st
import requests
from fpdf import FPDF

# Configure page
st.set_page_config(page_title="PDF Transcript Reformatter", page_icon="📏", layout="wide")

# Function to create formatted PDF from text
def create_pdf_from_text(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    # Properly formatted line breaks
    lines = text.split('\n')
    for line in lines:
        if line.strip():
            pdf.multi_cell(0, 10, line.strip())
            pdf.ln(2)
    return pdf

# User input for URL
st.title("PDF Transcript Reformatter")
url = st.text_input("Enter the URL of the transcript JSON:")

if url:
    try:
        # Fetch JSON data from URL
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        # Extract text from JSON
        transcript_text = data.get("transcript", {}).get("text", "")
        if transcript_text:
            # Display original transcript text
            st.subheader("Original Transcript Text")
            st.text_area("Transcript Text", transcript_text, height=300)

            # Create formatted PDF from transcript text
            pdf = create_pdf_from_text(transcript_text)
            output_path = "/mnt/data/formatted_transcript.pdf"
            pdf.output(output_path)

            # Allow users to download the formatted transcript
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="Download Formatted Transcript PDF",
                    data=file,
                    file_name="formatted_transcript.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Could not extract transcript text from the provided URL.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from URL: {e}")

