import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('DASHBOARD ANALISIS DATA E-COMMERCE')
# st.write('Source Dataset: Brazilian E-Commerce Public Dataset by Olist')
# st.write('https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/code')
st.markdown("---")


# Konten sidebar
st.sidebar.title('Pofiles:')
st.sidebar.markdown('**Nama:** Darmawan Jiddan')
st.sidebar.markdown('**Email:** zdarmawan95@gmail.com')
st.sidebar.markdown('**ID Dicoding:** ziddan2808')


# Load your data
all_df = pd.read_csv(
    'https://raw.githubusercontent.com/zidan2808/submission-dashboard/main/dashboard/all_data.csv')


# Menghitung Jumlah Data Statistik Customer
total_customers = all_df['customer_id'].nunique()
total_cities = all_df['customer_city'].nunique()
total_states = all_df['customer_state'].nunique()

# Menampilkan nilai statistik dalam bentuk kolom
st.info("Customer Statistics:")

# Membuat kolom dengan st.columns()
col1, col2, col3 = st.columns(3)

# Menampilkan nilai statistik dalam kolom
with col1:
    st.write("Total Customers:", total_customers)

with col2:
    st.write("Total Cities:", total_cities)

with col3:
    st.write("Total States:", total_states)

st.write('')

# Mengelompokkan data berdasarkan negara dan menghitung jumlah pelanggan
customer_counts_by_state = all_df.groupby(
    'customer_state')['customer_id'].nunique().reset_index()
top_5_states = customer_counts_by_state.sort_values(
    by='customer_id', ascending=False).head(5)

# Mengelompokkan data berdasarkan kota dan menghitung jumlah pelanggan
customer_counts_by_city = all_df.groupby(
    'customer_city')['customer_id'].nunique().reset_index()
top_5_cities = customer_counts_by_city.sort_values(
    by='customer_id', ascending=False).head(5)

# Tampilkan informasi dalam kolom
st.header('Top 5 States and Cities by Number of Customers')

col1, col2 = st.columns(2)

with col1:
    st.subheader('Top 5 States by Number of Customers')
    st.bar_chart(top_5_states.set_index('customer_state'))

with col2:
    st.subheader('Top 5 Cities by Number of Customers')
    st.bar_chart(top_5_cities.set_index('customer_city'))

# Membuat kolom untuk informasi berikutnya
st.write('')

# Group by product category and calculate aggregated statistics
revenue_by_category_df = all_df.groupby(by='product_category_name_english').agg({
    'payment_value': ['sum', 'min', 'max', 'mean'],
    'order_item_id': 'sum'
})

# Rename columns for better understanding
revenue_by_category_df.columns = [
    'Revenue_Total', 'Revenue_Min', 'Revenue_Max', 'Revenue_Mean', 'Quantity']

# Sort the dataframe by total revenue and select top 5 categories
revenue_by_categories = revenue_by_category_df.sort_values(
    by='Revenue_Total', ascending=False).head(5)

# Tampilkan informasi dalam kolom
st.subheader('Top 5 Product Categories by Revenue')
st.bar_chart(revenue_by_categories['Revenue_Total'], use_container_width=True)

# Group by customer city and calculate aggregated statistics
revenue_by_city_df = all_df.groupby('customer_city').agg({
    'payment_value': ['sum', 'min', 'max', 'mean'],
    'order_item_id': 'sum'
})

# Rename columns for better understanding
revenue_by_city_df.columns = [
    'Revenue_Total', 'Revenue_Min', 'Revenue_Max', 'Revenue_Mean', 'Quantity']

# Sort the dataframe by total revenue and select top 5 cities
revenue_by_city_df = revenue_by_city_df.sort_values(
    by='Revenue_Total', ascending=False).head(5)

# Tampilkan informasi dalam kolom
st.subheader('Top 5 Cities by Revenue')
st.bar_chart(revenue_by_city_df['Revenue_Total'], use_container_width=True)

st.write('')

# Group by customer state and product category, and calculate total revenue
top_category_bystate_df = all_df.groupby(by=['customer_state', 'product_category_name_english']).agg({
    'payment_value': 'sum'
})

# Rename columns for better understanding
top_category_bystate_df.rename(
    columns={'payment_value': 'Total Revenue'}, inplace=True)

# Find the top category for each state
idx = top_category_bystate_df.groupby('customer_state')[
    'Total Revenue'].idxmax()
top_categories_by_state = top_category_bystate_df.loc[idx].sort_values(
    by='Total Revenue', ascending=False).head(5)

# Prepare data for the bar chart
categories = top_categories_by_state.index.get_level_values(1)
states = top_categories_by_state.index.get_level_values(0)
revenue_values = top_categories_by_state['Total Revenue']

# Create a DataFrame for the bar chart
data = pd.DataFrame({'State_Category': [f'{state} - {category}' for state, category in zip(states, categories)],
                     'Revenue': revenue_values})

# Display the bar chart using Streamlit
st.subheader('Top 5 Product Categories by State')
st.bar_chart(data.set_index('State_Category'), use_container_width=True)

st.write('')

# Group by payment type and calculate transaction count
payment_type_df = all_df['payment_type'].value_counts().reset_index()
payment_type_df.columns = ['Payment Type', 'Transaction Count']

# Plot bar chart using Streamlit
st.subheader('Top Payment Types by Transaction Count')
st.bar_chart(payment_type_df.set_index(
    'Payment Type'), use_container_width=True)

st.write('')

# Ekstrak bulan dari tanggal pembelian
all_df['order_month'] = pd.to_datetime(
    all_df['order_purchase_timestamp']).dt.to_period('M')

# Hitung total pendapatan per bulan
revenue_per_month = all_df.groupby('order_month')['payment_value'].sum()

# Plot line chart menggunakan Matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(revenue_per_month.index.astype(str), revenue_per_month.values,
        marker='o', color='skyblue', linestyle='-')


plt.xticks(rotation=45)
plt.tight_layout()
plt.grid(True)

# Tampilkan plot sebagai gambar di Streamlit
st.subheader('Total Revenue per Month')
st.pyplot(fig)

st.write('')

# Hitung rata-rata skor ulasan berdasarkan pesanan
average_review_score_by_order = all_df.groupby(
    'order_id')['review_score'].mean()

# Hitung nilai rata-rata skor ulasan secara keseluruhan dan jumlah pesanan
total_average_review_score = round(average_review_score_by_order.mean(), 1)
order_count_by_order_id = len(average_review_score_by_order)

# Plot bar chart menggunakan Matplotlib
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh('score', total_average_review_score, color='skyblue')
ax.set_xlim(0, 5)
ax.set_title(
    f'Average Review Score: {total_average_review_score} out of 5 from {order_count_by_order_id} orders')

# Tampilkan plot sebagai gambar di Streamlit
st.subheader('Average Review Score')
st.pyplot(fig)
