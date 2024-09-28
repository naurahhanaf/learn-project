import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Menyiapkan function untuk analisis data 1
def create_df_year_month_order(df):
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['order_purchase_month'] = pd.Categorical(df['order_purchase_month'], categories=month_order, ordered=True)

    df_year_month_order = df.groupby(by=["order_purchase_year", "order_purchase_month"]).order_id.nunique().reset_index() \
        .sort_values(by=["order_purchase_year", "order_purchase_month"]).reset_index(drop=True) \
        .rename(columns={"order_id": "order_count"}) \
        .query('order_count > 0')

    return df_year_month_order

# Menyiapkan function untuk analisis data 2
def create_df_delivery_status(df):
    df_delivery_status = df.groupby(by="delivery_status").agg({
    "order_id" : "nunique"
    })
    df_delivery_status.rename(columns={
        "order_id": "order_count"
    }, inplace=True)

    return df_delivery_status

# Menyiapkan function untuk analisis data 3
def create_df_order_score(df):
    df_order_score = df.groupby(by=["review_score", "delivery_status"]).agg({
    "order_id" : "nunique"
    })
    df_order_score = df_order_score.reset_index()

    return df_order_score





# DATA WRANGLING
## Gathering Data
df_orders = pd.read_csv("data/olist_orders_dataset.csv")
df_reviews = pd.read_csv("data/olist_order_reviews_dataset.csv")

## Cleaning Data
datetime_columns_orders = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
df_orders[datetime_columns_orders] = df_orders[datetime_columns_orders].apply(pd.to_datetime)

datetime_columns_reviews = ["review_creation_date", "review_answer_timestamp"]
df_reviews[datetime_columns_reviews] = df_reviews[datetime_columns_reviews].apply(pd.to_datetime)


# MEMBUAT KOLOM BARU UNTUK MEMBANTU ANALISIS
## Membagi kolom order_purchase_timestamp menjadi kolom hari, bulan, tahun, dan waktu
df_orders['order_purchase_day'] = df_orders['order_purchase_timestamp'].dt.day_name()           # Nama hari
df_orders['order_purchase_date'] = df_orders['order_purchase_timestamp'].dt.day                 # Tanggal
df_orders['order_purchase_month'] = df_orders['order_purchase_timestamp'].dt.month_name()       # Nama bulan
df_orders['order_purchase_year'] = df_orders['order_purchase_timestamp'].dt.year                # Tahun
df_orders['order_purchase_time'] = df_orders['order_purchase_timestamp'].dt.time                # Waktu

## Membuat kolom delivery status
delivery_status = (df_orders["order_estimated_delivery_date"] - df_orders["order_delivered_customer_date"]).dt.days
df_orders['delivery_status'] = delivery_status.apply(lambda x: 'On Time' if x > 0 else 'Late')

## Merge df_orders dengan df_reviews
df_order_review = pd.merge(
    left=df_orders,
    right=df_reviews,
    how="left",
    left_on="order_id",
    right_on="order_id"
)

## Filter
df_order_review['order_purchase_year'] = df_order_review['order_purchase_timestamp'].dt.year
df_order_review['order_purchase_month'] = df_order_review['order_purchase_timestamp'].dt.month_name()

df_order_review_filtered = df_order_review[
    ((df_order_review['order_purchase_year'] == 2017) & (df_order_review['order_purchase_month'].isin(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']))) |
    ((df_order_review['order_purchase_year'] == 2018) & (df_order_review['order_purchase_month'].isin(['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August'])))
]





# DASHBOARD
st.header("Delivery Order Performance of Brazilian E-Commerce Dashboard")
st.write("Proyek Analisis Data Dicoding oleh Naurahhana Firdaustsabita")

with st.expander('Tentang Dataset Brazilian E-Commerce'):
    st.write(
        "Dataset ini disediakan oleh Olist, perusahaan e-commerce terbesar di Brasil yang memfasilitasi bisnis kecil. Olist berperan sebagai penghubung antara toko-toko kecil dengan berbagai marketplace, sehingga mempermudah mereka untuk menjual produk secara online. Produk yang dijual langsung dikirim dari toko ke konsumen melalui mitra logistik Olist. Selebihnya tentang Olist dapat mengunjungi [Website Olist](www.olist.com)."
    )

col1, col2 = st.columns([3,2])

with col1: 
    # Data viz 1 : Tren Jumlah Order
    ## Membuat dataframe
    df_year_month_order = create_df_year_month_order(df_order_review_filtered)
    total_orders_2017 = df_year_month_order[df_year_month_order["order_purchase_year"] == 2017]["order_count"].sum()
    total_orders_2018 = df_year_month_order[df_year_month_order["order_purchase_year"] == 2018]["order_count"].sum()

    st.subheader("Jumlah Order per Bulan (2017 - 2018)")

    ## Membuat chart
    fig, ax = plt.subplots()
    sns.lineplot(
        x="order_purchase_month",   #sumbu x
        y="order_count",            #sumbu y
        hue="order_purchase_year",
        data=df_year_month_order, 
        marker="o", 
        palette=["#72BCD4", "#FF6F61"]
    )
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(
        handles=handles, # objek grafis dari legend (misalnya, garis).
        labels=[f"2017 (Total: {total_orders_2017})", f"2018 (Total: {total_orders_2018})"], 
        title="Tahun"
    )
    plt.xlabel("Bulan", fontsize=12)
    plt.ylabel("Jumlah Order", fontsize=12)
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    # Data viz 2 : Presentase status pengiriman
    ## Membuat dataframe
    df_delivery_status = create_df_delivery_status(df_order_review_filtered)

    st.subheader("Persentase Status Pengiriman")
    col3, col4 = st.columns(2)
    with col3:
        late_orders = df_delivery_status.loc['Late', 'order_count']
        st.metric(label="Late Orders", value=late_orders)
    
    with col4:
        on_time_orders = df_delivery_status.loc['On Time', 'order_count']
        st.metric(label="On Time Orders", value=on_time_orders)

    ## Membuat chart
    fig, ax = plt.subplots()
    plt.pie(
        df_delivery_status["order_count"], 
        explode= (0.1, 0) , 
        labels= df_delivery_status.index, 
        colors= ["#FF6F61", "#72BCD4"], 
        autopct='%1.1f%%', 
        startangle=140
    )
    st.pyplot(fig)

# Data viz 3 : Hubungan antara rating ulasan dan ketepatan waktu pengiriman
## Membuat dataframe
df_order_score = create_df_order_score(df_order_review_filtered)
st.subheader("Hubungan antara Rating Ulasan dan Ketepatan Waktu Pengiriman")

## Membuat chart
fig, ax = plt.subplots()
sns.barplot(
    x="review_score", 
    y="order_id", 
    hue="delivery_status", 
    data=df_order_score,
    palette=['#FF6F61', '#72BCD4']  # Pastikan jumlah warna sesuai dengan kategori
)

for patch in ax.patches:
    height = patch.get_height()
    ax.annotate(
        f'{int(height)}',  # Label nilai
        (patch.get_x() + patch.get_width() / 2, height),  # Posisi label
        ha='center',  # Horizontal alignment
        va='bottom',  # Vertical alignment
        fontsize=10
    )
    
plt.xlabel("Rating Ulasan", fontsize=12)
plt.ylabel("Jumlah Pesanan", fontsize=12)
plt.legend(title='Status Pengiriman')
st.pyplot(fig)
