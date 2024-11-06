import streamlit as st
import pandas as pd
from database import execute_query
from datetime import datetime
from utils.validators import validate_dot_number, validate_phone

def add_carrier():
    st.subheader("Add New Carrier")
    
    with st.form("carrier_form"):
        company_name = st.text_input("Company Name")
        dot_number = st.text_input("DOT Number")
        mc_number = st.text_input("MC Number")
        insurance_exp_date = st.date_input("Insurance Expiration Date")
        w9_status = st.checkbox("W-9 Received")
        contact_name = st.text_input("Contact Name")
        contact_email = st.text_input("Contact Email")
        contact_phone = st.text_input("Contact Phone")
        
        if st.form_submit_button("Add Carrier"):
            if not validate_dot_number(dot_number):
                st.error("Invalid DOT Number")
                return
            
            if not validate_phone(contact_phone):
                st.error("Invalid phone number format")
                return
            
            query = """
                INSERT INTO carriers (company_name, dot_number, mc_number, 
                insurance_exp_date, w9_status, contact_name, contact_email, 
                contact_phone)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            execute_query(query, (company_name, dot_number, mc_number, 
                                insurance_exp_date, w9_status, contact_name,
                                contact_email, contact_phone))
            st.success("Carrier added successfully!")

def view_carriers():
    st.subheader("Carrier List")
    
    carriers = execute_query("SELECT * FROM carriers ORDER BY company_name")
    if carriers:
        df = pd.DataFrame(carriers)
        st.dataframe(df)
        
        # Expiring Insurance Alert
        today = datetime.now().date()
        expiring_soon = df[pd.to_datetime(df['insurance_exp_date']).dt.date.between(
            today, pd.Timestamp(today) + pd.Timedelta(days=30))]
        
        if not expiring_soon.empty:
            st.warning("Carriers with insurance expiring in 30 days:")
            st.dataframe(expiring_soon[['company_name', 'insurance_exp_date']])

def main():
    st.title("Carrier Management")
    
    tab1, tab2 = st.tabs(["View Carriers", "Add Carrier"])
    
    with tab1:
        view_carriers()
    
    with tab2:
        add_carrier()

if __name__ == "__main__":
    main()
