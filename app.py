import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------

st.set_page_config(page_title="E-commerce Dashboard", layout="wide")

st.title("📊 E-commerce Sales Overview")
st.write("Monitor revenue, orders, and product performance in one place.")

# ---------------- LOAD DATA ----------------

df = pd.read_csv("ecommerce_sales.csv")

df["Date"] = pd.to_datetime(df["Date"])
df["Revenue"] = df["Price"] * df["Quantity"]

# ---------------- SIDEBAR FILTER ----------------

st.sidebar.header("Filters")

country = st.sidebar.selectbox(
    "🌍 Select Country",
    ["All"] + list(df["Country"].unique())
)

if country == "All":
    filtered_df = df.copy()
else:
    filtered_df = df[df["Country"] == country]

# ---------------- KPI CARDS ----------------

total_revenue = filtered_df["Revenue"].sum()
total_orders = len(filtered_df)
avg_order = filtered_df["Revenue"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Revenue", f"${total_revenue:,.0f}")
col2.metric("📦 Total Orders", total_orders)
col3.metric("🛒 Avg Order Value", f"${avg_order:,.2f}")

st.divider()

# ---------------- SALES TREND ----------------

st.subheader("📈 Sales Trend")

sales_trend = filtered_df.groupby("Date")["Revenue"].sum().reset_index()

fig1 = px.line(
    sales_trend,
    x="Date",
    y="Revenue",
    markers=True,
    title="Revenue Over Time"
)

# ---------------- TOP PRODUCTS ----------------

st.subheader("🏆 Top 5 Products")

top_products = (
    filtered_df.groupby("Product")["Revenue"]
    .sum()
    .reset_index()
    .sort_values(by="Revenue", ascending=False)
    .head(5)
)

fig2 = px.bar(
    top_products,
    x="Product",
    y="Revenue",
    title="Top Performing Products"
)

# ---------------- CATEGORY SALES ----------------

st.subheader("🥧 Category Sales Distribution")

category_sales = filtered_df.groupby("Category")["Revenue"].sum().reset_index()

fig3 = px.pie(
    category_sales,
    values="Revenue",
    names="Category",
    title="Revenue by Category"
)

# ---------------- MONTHLY SALES ----------------

st.subheader("📅 Monthly Revenue")

filtered_df["Month"] = filtered_df["Date"].dt.to_period("M").astype(str)

monthly_sales = (
    filtered_df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    monthly_sales,
    x="Month",
    y="Revenue",
    title="Monthly Sales"
)

# ---------------- DASHBOARD LAYOUT ----------------

col4, col5 = st.columns(2)

with col4:
    st.plotly_chart(fig1, use_container_width=True)

with col5:
    st.plotly_chart(fig2, use_container_width=True)

st.plotly_chart(fig3, use_container_width=True)
st.plotly_chart(fig4, use_container_width=True)

# ---------------- DATASET ----------------

with st.expander("📂 View Dataset"):
    st.dataframe(filtered_df)