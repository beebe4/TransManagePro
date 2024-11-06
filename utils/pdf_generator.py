import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from database import execute_query

def generate_rate_confirmation(load_id):
    # Get load details
    query = """
        SELECT l.*, c.company_name as customer_name,
        cr.company_name as carrier_name,
        cr.contact_name as carrier_contact,
        cr.contact_phone as carrier_phone
        FROM loads l
        JOIN customers c ON l.customer_id = c.id
        JOIN carriers cr ON l.carrier_id = cr.id
        WHERE l.id = %s
    """
    
    load_data = execute_query(query, (load_id,))[0]
    
    # Create PDF
    filename = f"rate_confirmation_{load_id}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []
    
    # Header
    elements.append(Paragraph(f"Rate Confirmation #{load_id}", styles['Heading1']))
    elements.append(Spacer(1, 12))
    
    # Load details
    data = [
        ["Carrier:", load_data['carrier_name']],
        ["Contact:", f"{load_data['carrier_contact']} - {load_data['carrier_phone']}"],
        ["Pickup:", f"{load_data['pickup_location']} on {load_data['pickup_date']}"],
        ["Delivery:", f"{load_data['delivery_location']} on {load_data['delivery_date']}"],
        ["Rate:", f"${load_data['rate_carrier']:,.2f}"]
    ]
    
    table = Table(data, colWidths=[100, 400])
    table.setStyle([
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    
    elements.append(table)
    
    # Build PDF
    doc.build(elements)
    return filename
