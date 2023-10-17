
import streamlit as st
import PyPDF2
from reportlab.lib.pagesizes import letter,A4
from reportlab.pdfgen import canvas
import os

CRF_VERSION = '5.0.3'
CRF = f'ddi_crf_baseline_{CRF_VERSION}.pdf'


def create_watermark(output_pdf_path, watermark_text):
    c = canvas.Canvas(output_pdf_path, pagesize=A4)
    width, height = A4
    c.drawString(420, 45, watermark_text)  # Draws watermark text at x, y position 100, 100
    c.save()

def add_watermark(input_pdf_path, output_pdf_path, watermark_text, pages_to_watermark, progress_bar):
    # Create watermark
    watermark_path = "watermark.pdf"
    create_watermark(watermark_path, watermark_text)
    
    # Create PdfReader object
    pdf_reader = PyPDF2.PdfReader(input_pdf_path)
    pdf_writer = PyPDF2.PdfWriter()

    # Create PdfReader object for the watermark
    watermark_reader = PyPDF2.PdfReader(watermark_path)
    watermark_page = watermark_reader.pages[0]

    # Apply the watermark
    num_pages = len(pdf_reader.pages)
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        
        if i in pages_to_watermark:
            page.merge_page(watermark_page)
        
        pdf_writer.add_page(page)
        # Update the progress bar
        # set progress bar text
        # progress_bar.text(f"Processing page {i + 1} of {num_pages}...")
        progress = (i + 1) / num_pages
        progress_bar.progress(progress)
        

    # Write the watermarked pages to the new file
    with open(output_pdf_path, "wb") as f_out:
        pdf_writer.write(f_out)

def pdf_tool():
    
    st.title(f"DDI CRF {CRF_VERSION}")
    st.write(f"This service stamps and generate a PDF of the DDI CRF {CRF_VERSION} for printing and use in a subject visit.")

    # Internal PDF path
    internal_pdf_path = CRF

    # Text input for watermark
    subject_id = st.text_input("Enter subject ID")

    # Submit button
    if st.button("Submit"):
        # Output path for new PDF
        output_path = f'DDI_CRF_{subject_id}.pdf'

        # Progress bar
        progress_bar = st.progress(0)

        # pages to watermark in 5.0.3
        pages = list(range(0, 25)) + list(range(39, 46)) + list(range(49 , 60))

        # Add watermark to internal PDF
        add_watermark(internal_pdf_path, output_path, subject_id, pages, progress_bar)

        download_button = st.download_button(
            label="Download PDF",
            data=open(output_path, "rb"),
            file_name=output_path,
            mime="application/pdf",
        )
        # remove the output file after download
        os.remove(output_path)

pdf_tool()