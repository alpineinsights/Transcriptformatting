import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from fpdf import FPDF

# Configure page
st.set_page_config(page_title="PDF Transcript Reformatter", page_icon="📏", layout="wide")

# Load watermark image
watermark_image_path = '/mnt/data/Alpine-01.jpg'
with open(watermark_image_path, "rb") as f:
    watermark = Image.open(f)

# Function to apply watermark
def apply_watermark(base_image, watermark):
    # Resize watermark to fit the image
    base_width, base_height = base_image.size
    watermark = watermark.resize((base_width // 3, base_height // 3), Image.ANTIALIAS)

    # Apply watermark to bottom right corner
    watermark_position = (base_width - watermark.width, base_height - watermark.height)
    base_image.paste(watermark, watermark_position, mask=watermark)

    return base_image

# Function to create PDF from image
def create_pdf_from_image(image):
    pdf = FPDF()
    pdf.add_page()
    with BytesIO() as img_buffer:
        image.save(img_buffer, format="PNG")
        img_buffer.seek(0)
        pdf.image(img_buffer, x=10, y=10, w=190)
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
            # Create an image from the text
            img = Image.new('RGB', (800, 1000), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            d.text((10, 10), transcript_text, fill=(0, 0, 0), font=font)

            # Show original transcript
            st.subheader("Original Transcript Image")
            st.image(img, caption="Original Transcript", use_column_width=True)

            # Apply watermark
            watermarked_img = apply_watermark(img, watermark)

            # Display watermarked transcript
            st.subheader("Watermarked Transcript Image")
            st.image(watermarked_img, caption="Watermarked Transcript", use_column_width=True)

            # Create PDF from watermarked image
            pdf = create_pdf_from_image(watermarked_img)
            output_path = "/mnt/data/watermarked_transcript.pdf"
            pdf.output(output_path)

            # Allow users to download the modified transcript
            with open(output_path, "rb") as file:
                btn = st.download_button(
                    label="Download Watermarked Transcript PDF",
                    data=file,
                    file_name="watermarked_transcript.pdf",
                    mime="application/pdf"
                )
        else:
            st.error("Could not extract transcript text from the provided URL.")

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from URL: {e}")
