from fpdf import FPDF
from io import BytesIO

def sanitize_text(text):
    # Replace common unicode characters not supported by standard Helvetica
    replacements = {
        '—': '-', '–': '-', 
        '’': "'", '‘': "'", 
        '”': '"', '“': '"',
        '…': '...'
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    # Force encode to latin-1 to replace any other unsupported characters with '?'
    return text.encode('latin-1', 'replace').decode('latin-1')

def generate_pdf(patient_id, title, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", style="B", size=16)
    
    safe_title = sanitize_text(f"ClinicalView System - {title}")
    pdf.cell(0, 10, text=safe_title, new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.set_font("Helvetica", style="I", size=12)
    pdf.cell(0, 10, text=f"Patient Reference: {patient_id}", new_x="LMARGIN", new_y="NEXT", align='C')
    
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=11)
    
    # Very basic markdown stripping for PDF display
    clean_content = content.replace('**', '').replace('### ', '')
    safe_content = sanitize_text(clean_content)
    
    # multi_cell automatically handles word wrapping
    pdf.multi_cell(0, 8, text=safe_content)
    
    # Return as raw bytes for Streamlit st.download_button
    return bytes(pdf.output())
