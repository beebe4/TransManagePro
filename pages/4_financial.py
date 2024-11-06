import streamlit as st
import pandas as pd
import plotly.express as px
from database import execute_query

def revenue_analysis():
    st.subheader("Revenue Analysis")
    
    # Time period filter
    period = st.selectbox("Select Period", ["Last 7 days", "Last 30 days", "Last 90 days"])
    
    days = {
        "Last 7 days": 7,
        "Last 30 days": 30,
        "Last 90 days": 90
    }[period]
    
    query = """
        SELECT DATE(created_at) as date,
               SUM(rate_customer) as revenue,
               SUM(rate_carrier) as cost,
               SUM(rate_customer - rate_carrier) as profit
        FROM loads
        WHERE created_at >= CURRENT_DATE - INTERVAL '%s days'
        GROUP BY DATE(created_at)
        ORDER BY date
    """
    
    data = execute_query(query, (days,))
    
    if data:
        df = pd.DataFrame(data)
        
        # Revenue Chart
        fig1 = px.line(df, x='date', y=['revenue', 'cost', 'profit'],
                      title="Revenue, Cost, and Profit Over Time")
        st.plotly_chart(fig1)
        
        # Summary metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Revenue", f"${df['revenue'].sum():,.2f}")
        with col2:
            st.metric("Total Cost", f"${df['cost'].sum():,.2f}")
        with col3:
            st.metric("Total Profit", f"${df['profit'].sum():,.2f}")

def carrier_performance():
    st.subheader("Carrier Performance")
    
    query = """
        SELECT c.company_name,
               COUNT(l.id) as total_loads,
               AVG(l.rate_carrier) as avg_rate,
               SUM(l.rate_carrier) as total_paid
        FROM carriers c
        LEFT JOIN loads l ON c.id = l.carrier_id
        GROUP BY c.id, c.company_name
        ORDER BY total_loads DESC
    """
    
    data = execute_query(query)
    
    if data:
        df = pd.DataFrame(data)
        
        fig = px.bar(df, x='company_name', y='total_loads',
                    title="Loads per Carrier")
        st.plotly_chart(fig)
        
        st.dataframe(df)

def customer_analysis():
    st.subheader("Customer Analysis")
    
    query = """
        SELECT c.company_name,
               COUNT(l.id) as total_loads,
               AVG(l.rate_customer) as avg_rate,
               SUM(l.rate_customer) as total_revenue,
               SUM(l.rate_customer - l.rate_carrier) as total_profit
        FROM customers c
        LEFT JOIN loads l ON c.id = l.customer_id
        GROUP BY c.id, c.company_name
        ORDER BY total_revenue DESC
    """
    
    data = execute_query(query)
    
    if data:
        df = pd.DataFrame(data)
        
        fig = px.pie(df, values='total_revenue', names='company_name',
                    title="Revenue Distribution by Customer")
        st.plotly_chart(fig)
        
        st.dataframe(df)

def main():
    st.title("Financial Reports")
    
    tab1, tab2, tab3 = st.tabs([
        "Revenue Analysis",
        "Carrier Performance",
        "Customer Analysis"
    ])
    
    with tab1:
        revenue_analysis()
    
    with tab2:
        carrier_performance()
    
    with tab3:
        customer_analysis()

if __name__ == "__main__":
    main()
