import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Create a function for data analysis 1
def create_df_year_month_order(df):
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df['order_purchase_month'] = pd.Categorical(df['order_purchase_month'], categories=month_order, ordered=True)

    df_year_month_order = df.groupby(by=["order_purchase_year", "order_purchase_month"]).order_id.nunique().reset_index() \
        .sort_values(by=["order_purchase_year", "order_purchase_month"]).reset_index(drop=True) \
        .rename(columns={"order_id": "order_count"}) \
        .query('order_count > 0')

    return df_year_month_order

# Create a function for data analysis 2
def create_df_delivery_performa(df):
    df_delivery_performa = df.groupby(by=["order_purchase_year", "order_purchase_month", "delivery_status"]).order_id.nunique().reset_index() \
    .sort_values(by=["order_purchase_year", "order_purchase_month"]).reset_index(drop=True) \
    .rename(columns={"order_id": "order_count"}) \
    .query('order_count > 0')

    return df_delivery_performa

# Create a function for data analysis 3
def create_df_order_score(df):
    df_order_score = df.groupby(by=["review_score", "delivery_status"]).agg({
    "order_id" : "nunique"
    })
    df_order_score = df_order_score.reset_index()

    return df_order_score





# DATA WRANGLING
## Gathering Data
df_orders = pd.read_csv("brazilian-ecommerce-analysis/data/olist_orders_dataset.csv")
df_reviews = pd.read_csv("brazilian-ecommerce-analysis/data/olist_order_reviews_dataset.csv")

## Cleaning Data
datetime_columns_orders = ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"]
df_orders[datetime_columns_orders] = df_orders[datetime_columns_orders].apply(pd.to_datetime)

datetime_columns_reviews = ["review_creation_date", "review_answer_timestamp"]
df_reviews[datetime_columns_reviews] = df_reviews[datetime_columns_reviews].apply(pd.to_datetime)


## Create new column for day, month, year, and time from order_purchase_timestamp column
df_orders['order_purchase_day'] = df_orders['order_purchase_timestamp'].dt.day_name()           # Day of week
df_orders['order_purchase_date'] = df_orders['order_purchase_timestamp'].dt.day                 # Date
df_orders['order_purchase_month'] = df_orders['order_purchase_timestamp'].dt.month_name()       # Month
df_orders['order_purchase_year'] = df_orders['order_purchase_timestamp'].dt.year                # Year
df_orders['order_purchase_time'] = df_orders['order_purchase_timestamp'].dt.time                # Time

## Create delivery_status column
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





# SIDE BAR 
with st.sidebar:
    # Logo Olist
    st.image("brazilian-ecommerce-analysis/dashboard/olist_logo.png", width=270)

    # Create year filter
    years = df_order_review_filtered["order_purchase_year"].unique()
    selected_year = st.selectbox("Year:", years)

    # Create dataframe for load data after filtering
    filtered_data = df_order_review_filtered[(df_order_review_filtered)["order_purchase_year"] == (selected_year)]

    # Create dataset info
    with st.expander('About Dataset'):
        st.write(
            "This dataset is provided by Olist, Brazilian largest e-commerce company that facilitates small businesses. Olist acts as a link between small shops and various marketplaces, making it easier for them to sell products online. The products sold are shipped directly from the stores to the consumers through Olist's logistics partners. For more on this dataset, visit kaggle at [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/)."
        )





# DASHBOARD
st.title("Olist Delivery Order Dashboard")

# Data viz 1 : monthly order trend
# Create dataframe with create_df_year_month_order
df_year_month_order = create_df_year_month_order(filtered_data)
total_orders = df_year_month_order.groupby("order_purchase_year")["order_count"].sum()
st.header(f"Monthly Order Trend {selected_year}")

# Create line plot
fig, ax = plt.subplots()
sns.lineplot(
    x="order_purchase_month",   #sumbu x
    y="order_count",            #sumbu y
    hue="order_purchase_year",
    data=df_year_month_order, 
    marker="o", 
    palette=["#02735E"]
)
handles, labels = ax.get_legend_handles_labels()
# Create legend
plt.legend(
    handles=handles, # graphical objects from the legend (e.g., lines)
    labels=[f"{year} (Total: {int(total_orders.loc[year])})" for year in df_year_month_order["order_purchase_year"].unique()], 
    title="Year"
)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Total Orders", fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)





# Data viz 2 dan 3
## Create dataframe with create_df_delivery_performa
df_delivery_performa = create_df_delivery_performa(filtered_data)
st.header(f"Delivery Orders Performa in {selected_year}")

## Create a metric
col3, col4 = st.columns([3,2])
if not df_delivery_performa.empty:
    ## Create dataset for total delivery_status by order_count
    df_delivery_status = df_delivery_performa.groupby("delivery_status")["order_count"].sum()
        
    with col3:
        ## Metric for late orders status
        late_orders = df_delivery_status.get("Late", 0)
        st.metric(label="Late Orders", value=late_orders)

    with col4:
        ## Metric for on-time orders status
        on_time_orders = df_delivery_status.get("On Time", 0)
        st.metric(label="On Time Orders", value=on_time_orders)
else:
    st.write("No data in selected year.")

col5, col6 = st.columns([3,2])
with col5:
    # Data viz 2 : comparison delivery status per month
    if not df_delivery_performa.empty:
        plt.figure(figsize=(12, 6))
        plt.subplot(1, 1, 1)
        sns.barplot(data=df_delivery_performa, 
                    x="order_purchase_month", 
                    y="order_count", 
                    hue="delivery_status", 
                    palette=["#F27457", "#04BF9D"])
        
        plt.title("Comparison of Number of On-Time and Late Orders per Month", fontsize=18)
        plt.xlabel("Month")
        plt.ylabel("Total Orders")
        plt.xticks(rotation=45)
        plt.legend(title="Delivery Status")
        
        st.pyplot(plt)

    else:
        st.write("No data in selected year.")

with col6: 
    # Data viz 3 : precentage of delivery status
    ## Membuat pie chart
    if not filtered_data.empty:
        # Pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(
            df_delivery_status, 
            explode=(0.1, 0),  # Make the “Late” section slightly separated from the others
            labels=df_delivery_status.index, 
            colors=["#F27457", "#04BF9D"],
            autopct='%1.1f%%', 
            startangle=140
        )
        plt.title("Percentage of Delivery Status", fontsize=22)
        plt.tight_layout()
        st.pyplot(plt)

    else:
        st.write("No data in selected year.")





# Data viz 4 : Relationship between Review Score and Delivery Status
## Create dataset with create_df_order_score
df_order_score = create_df_order_score(filtered_data)
st.header(f"Relationship between Review Score and Delivery Status in {selected_year}")

## Membuat chart
fig, ax = plt.subplots()
sns.barplot(
    x="review_score", 
    y="order_id", 
    hue="delivery_status", 
    data=df_order_score,
    palette=["#F27457", "#04BF9D"]
)

for patch in ax.patches:
    height = patch.get_height()
    ax.annotate(
        f'{int(height)}',  # label
        (patch.get_x() + patch.get_width() / 2, height),  # position
        ha='center',  # Horizontal alignment
        va='bottom',  # Vertical alignment
        fontsize=10
    )
    
plt.xlabel("Review Score", fontsize=12)
plt.ylabel("Total Orders", fontsize=12)
plt.legend(title="Delivery Status")
st.pyplot(fig)

st.caption('Copyright (c) Naurahhana Firdaustsabita')
