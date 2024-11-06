import streamlit as st
import pandas as pd
from database import execute_query
from utils.pdf_generator import generate_rate_confirmation

def create_load():
    st.subheader("Create New Load")
    
    # Get carriers and customers for dropdowns
    carriers = execute_query("SELECT id, company_name FROM carriers")
    customers = execute_query("SELECT id, company_name FROM customers")
    
    with st.form("load_form"):
        customer_id = st.selectbox(
            "Customer",
            options=[c['id'] for c in customers],
            format_func=lambda x: next(c['company_name'] for c in customers if c['id'] == x)
        )
        
        carrier_id = st.selectbox(
            "Carrier",
            options=[c['id'] for c in carriers],
            format_func=lambda x: next(c['company_name'] for c in carriers if c['id'] == x)
        )
        
        pickup_location = st.text_input("Pickup Location")
        delivery_location = st.text_input("Delivery Location")
        pickup_date = st.date_input("Pickup Date")
        delivery_date = st.date_input("Delivery Date")
        rate_customer = st.number_input("Customer Rate ($)", min_value=0.0)
        rate_carrier = st.number_input("Carrier Rate ($)", min_value=0.0)
        
        if st.form_submit_button("Create Load"):
            if rate_carrier >= rate_customer:
                st.error("Carrier rate must be less than customer rate")
                return
            
            query = """
                INSERT INTO loads (customer_id, carrier_id, pickup_location,
                delivery_location, pickup_date, delivery_date, rate_customer,
                rate_carrier)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            result = execute_query(query, (customer_id, carrier_id, pickup_location,
                                         delivery_location, pickup_date, delivery_date,
                                         rate_customer, rate_carrier))
            
            if result:
                st.success(f"Load created successfully! Load ID: {result[0]['id']}")
                generate_rate_confirmation(result[0]['id'])

def update_load_status():
    st.subheader("Update Load Status")
    
    loads = execute_query("""
        SELECT l.id, c.company_name as customer, cr.company_name as carrier,
               l.pickup_location, l.delivery_location, l.status
        FROM loads l
        JOIN customers c ON l.customer_id = c.id
        JOIN carriers cr ON l.carrier_id = cr.id
        WHERE l.status != 'completed'
    """)
    
    if loads:
        load_id = st.selectbox(
            "Select Load",
            options=[l['id'] for l in loads],
            format_func=lambda x: f"Load {x} - {next(l['customer'] for l in loads if l['id'] == x)}"
        )
        
        status = st.selectbox(
            "Update Status",
            options=['pending', 'in_transit', 'completed', 'cancelled']
        )
        
        location = st.text_input("Current Location")
        
        if st.button("Update Status"):
            query = """
                UPDATE loads SET status = %s WHERE id = %s;
                INSERT INTO load_tracking (load_id, status_update, location)
                VALUES (%s, %s, %s)
            """
            execute_query(query, (status, load_id, load_id, status, location))
            st.success("Load status updated successfully!")

def main():
    st.title("Load Management")
    
    tab1, tab2, tab3 = st.tabs(["View Loads", "Create Load", "Update Status"])
    
    with tab1:
        st.subheader("Active Loads")
        loads = execute_query("""
            SELECT l.*, c.company_name as customer, cr.company_name as carrier
            FROM loads l
            JOIN customers c ON l.customer_id = c.id
            JOIN carriers cr ON l.carrier_id = cr.id
            ORDER BY l.created_at DESC
        """)
        if loads:
            df = pd.DataFrame(loads)
            st.dataframe(df)
    
    with tab2:
        create_load()
    
    with tab3:
        update_load_status()

if __name__ == "__main__":
    main()
