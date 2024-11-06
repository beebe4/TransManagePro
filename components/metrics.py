import streamlit as st
import pandas as pd
from database import execute_query

def display_revenue_metrics():
    """Display revenue metrics component."""
    query = """
        SELECT 
            SUM(rate_customer) as total_revenue,
            SUM(rate_carrier) as total_cost,
            SUM(rate_customer - rate_carrier) as total_profit,
            AVG(rate_customer - rate_carrier) as avg_profit_per_load
        FROM loads
        WHERE status != 'cancelled'
    """
    
    data = execute_query(query)[0]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Revenue", f"${data['total_revenue']:,.2f}")
    with col2:
        st.metric("Total Cost", f"${data['total_cost']:,.2f}")
    with col3:
        st.metric("Total Profit", f"${data['total_profit']:,.2f}")
    with col4:
        st.metric("Avg Profit/Load", f"${data['avg_profit_per_load']:,.2f}")

def display_load_metrics():
    """Display load metrics component."""
    query = """
        SELECT 
            COUNT(*) FILTER (WHERE status = 'in_transit') as active_loads,
            COUNT(*) FILTER (WHERE status = 'pending') as pending_loads,
            COUNT(*) FILTER (WHERE status = 'completed') as completed_loads
        FROM loads
    """
    
    data = execute_query(query)[0]
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Active Loads", data['active_loads'])
    with col2:
        st.metric("Pending Loads", data['pending_loads'])
    with col3:
        st.metric("Completed Loads", data['completed_loads'])
