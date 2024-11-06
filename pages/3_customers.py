import streamlit as st
import pandas as pd
from database import execute_query
from utils.validators import validate_phone, validate_email

def add_customer():
    st.subheader("Add New Customer")
    
    with st.form("customer_form"):
        company_name = st.text_input("Company Name")
        contact_name = st.text_input("Contact Name")
        contact_email = st.text_input("Contact Email")
        contact_phone = st.text_input("Contact Phone")
        billing_address = st.text_area("Billing Address")
        
        if st.form_submit_button("Add Customer"):
            if not validate_phone(contact_phone):
                st.error("Invalid phone number format")
                return
            
            if not validate_email(contact_email):
                st.error("Invalid email format")
                return
            
            query = """
                INSERT INTO customers (company_name, contact_name, contact_email,
                contact_phone, billing_address)
                VALUES (%s, %s, %s, %s, %s)
            """
            execute_query(query, (company_name, contact_name, contact_email,
                                contact_phone, billing_address))
            st.success("Customer added successfully!")

def view_customers():
    st.subheader("Customer List")
    
    customers = execute_query("""
        SELECT c.*, COUNT(l.id) as total_loads,
        SUM(l.rate_customer) as total_revenue
        FROM customers c
        LEFT JOIN loads l ON c.id = l.customer_id
        GROUP BY c.id
        ORDER BY c.company_name
    """)
    
    if customers:
        df = pd.DataFrame(customers)
        st.dataframe(df)

def main():
    st.title("Customer Management")
    
    tab1, tab2 = st.tabs(["View Customers", "Add Customer"])
    
    with tab1:
        view_customers()
    
    with tab2:
        add_customer()

if __name__ == "__main__":
    main()
