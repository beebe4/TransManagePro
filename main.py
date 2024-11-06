import streamlit as st
import plotly.express as px
import pandas as pd
from database import execute_query

st.set_page_config(
    page_title="Freight Broker Management System",
    page_icon="🚛",
    layout="wide"
)

def get_dashboard_metrics():
    active_loads = execute_query("""
        SELECT COUNT(*) as count FROM loads 
        WHERE status NOT IN ('completed', 'cancelled')
    """)
    
    revenue_data = execute_query("""
        SELECT SUM(rate_customer - rate_carrier) as profit,
               SUM(rate_customer) as revenue
        FROM loads
        WHERE status != 'cancelled'
    """)
    
    return active_loads[0], revenue_data[0]

def main():
    st.title("🚛 Freight Broker Dashboard")
    
    # Key Metrics
    active_loads, revenue_data = get_dashboard_metrics()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Active Loads", active_loads['count'])
    with col2:
        st.metric("Total Revenue", f"${revenue_data['revenue']:,.2f}")
    with col3:
        st.metric("Total Profit", f"${revenue_data['profit']:,.2f}")
    
    # Recent Loads
    st.subheader("Recent Loads")
    recent_loads = execute_query("""
        SELECT l.id, c.company_name as customer, cr.company_name as carrier,
               l.pickup_location, l.delivery_location, l.status,
               l.rate_customer, l.rate_carrier
        FROM loads l
        JOIN customers c ON l.customer_id = c.id
        JOIN carriers cr ON l.carrier_id = cr.id
        ORDER BY l.created_at DESC
        LIMIT 5
    """)
    
    if recent_loads:
        df = pd.DataFrame(recent_loads)
        st.dataframe(df)
    
    # Profit Margin Visualization
    st.subheader("Profit Margins by Load")
    profit_data = execute_query("""
        SELECT id, rate_customer, rate_carrier,
               (rate_customer - rate_carrier) as profit_margin
        FROM loads
        WHERE status != 'cancelled'
        ORDER BY created_at DESC
        LIMIT 10
    """)
    
    if profit_data:
        df_profit = pd.DataFrame(profit_data)
        fig = px.bar(df_profit, x='id', y='profit_margin',
                    title="Profit Margins for Recent Loads")
        st.plotly_chart(fig)

if __name__ == "__main__":
    main()
