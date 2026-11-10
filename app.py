import pandas as pd
import plotly.express as px
import streamlit as st
from database import connect, initialize, seed_demo

st.set_page_config(page_title='Retail Sales Analytics', page_icon='📊', layout='wide')
initialize()
seed_demo()

st.title('Retail Sales Analytics Dashboard')
st.caption('Original portfolio project · Fictional, deterministic sample transactions')
with connect() as con:
    sales = pd.read_sql_query('SELECT sale_date, category, product, quantity, unit_price FROM sales', con)
sales['sale_date'] = pd.to_datetime(sales['sale_date'])
sales['revenue'] = sales['quantity'] * sales['unit_price']

st.sidebar.header('Filters')
min_date, max_date = sales['sale_date'].min().date(), sales['sale_date'].max().date()
selected_dates = st.sidebar.date_input('Date range', value=(min_date, max_date), min_value=min_date, max_value=max_date)
selected_categories = st.sidebar.multiselect('Categories', sorted(sales['category'].unique()), default=sorted(sales['category'].unique()))
if len(selected_dates) != 2:
    st.info('Select both a start and an end date.')
    st.stop()
start_date, end_date = selected_dates
filtered = sales[(sales['sale_date'].dt.date >= start_date) & (sales['sale_date'].dt.date <= end_date) & sales['category'].isin(selected_categories)]
if filtered.empty:
    st.warning('No sales match your filters. Try a different date range or category.')
    st.stop()

revenue = filtered['revenue'].sum()
units = int(filtered['quantity'].sum())
transactions = len(filtered)
cols = st.columns(3)
cols[0].metric('Revenue', f'${revenue:,.2f}')
cols[1].metric('Transactions', f'{transactions:,}')
cols[2].metric('Units sold', f'{units:,}')

by_day = filtered.groupby('sale_date', as_index=False)['revenue'].sum()
by_category = filtered.groupby('category', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
by_product = filtered.groupby('product', as_index=False)['revenue'].sum().sort_values('revenue', ascending=False)
st.plotly_chart(px.line(by_day, x='sale_date', y='revenue', title='Revenue over time', markers=True), use_container_width=True)
left, right = st.columns(2)
with left:
    st.plotly_chart(px.bar(by_category, x='category', y='revenue', title='Revenue by category'), use_container_width=True)
with right:
    st.plotly_chart(px.bar(by_product, x='product', y='revenue', title='Revenue by product'), use_container_width=True)
st.subheader('Filtered sales')
st.dataframe(filtered.sort_values('sale_date', ascending=False), use_container_width=True, hide_index=True)
st.download_button('Download filtered sales (CSV)', filtered.to_csv(index=False).encode('utf-8'), file_name='filtered_sales.csv', mime='text/csv')
