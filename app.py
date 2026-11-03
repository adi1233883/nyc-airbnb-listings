import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="NYC Airbnb Analytics",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 New York Airbnb Analytics Dashboard")
st.markdown("Explore Airbnb listings across New York City.")

@st.cache_data
def load_data():
    return pd.read_csv(
        "listings New York.gz",
        compression="gzip"
    )

try:
    df = load_data()

    st.sidebar.header("Filters")

    if "neighbourhood_group" in df.columns:
        areas = st.sidebar.multiselect(
            "Select Neighbourhood",
            df["neighbourhood_group"].dropna().unique(),
            default=list(df["neighbourhood_group"].dropna().unique())
        )
        df = df[df["neighbourhood_group"].isin(areas)]

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Listings", f"{len(df):,}")

    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        col2.metric(
            "Average Price",
            f"${df['price'].mean():,.2f}"
        )

    if "number_of_reviews" in df.columns:
        col3.metric(
            "Total Reviews",
            f"{df['number_of_reviews'].sum():,}"
        )

    st.subheader("Price Distribution")

    if "price" in df.columns:
        price_data = df[df["price"].between(0, 1000)]

        fig = px.histogram(
            price_data,
            x="price",
            title="Airbnb Price Distribution"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Room Type Analysis")

    if "room_type" in df.columns:
        fig = px.pie(
            df,
            names="room_type",
            title="Distribution of Room Types"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Neighbourhood Analysis")

    if "neighbourhood_group" in df.columns:
        fig = px.histogram(
            df,
            x="neighbourhood_group",
            title="Listings by Neighbourhood"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Dataset Preview")
    st.dataframe(df.head(100), use_container_width=True)

except Exception as e:
    st.error(f"Unable to load dataset: {e}")
