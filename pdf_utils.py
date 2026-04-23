from fpdf import FPDF
from io import BytesIO

def generate_pdf(patient_id, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(0, 10, text=f"ClinicalView System - {title}", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font("Helvetica", style="I", size=12)
    pdf.cell(0, 10, text=f"Patient Reference: {patient_id}", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=11)
    
    # Very basic markdown stripping for PDF display
    clean_content = content.replace('**', '').replace('### ', '')
    
    # multi_cell automatically handles word wrapping
    pdf.multi_cell(0, 8, text=clean_content)
    
    # Return as raw bytes for Streamlit st.download_button
    return bytes(pdf.output())
