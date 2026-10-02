import streamlit as st
import pandas as pd
import os

# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="Uber Trip Analysis",
    page_icon="🚕",
    layout="wide"
)

# -------------------------------------------------
# TITLE
# -------------------------------------------------

st.title("🚕 Uber Trip Data Analysis")
st.subheader("Analysis of Uber Trips Using Apache Spark")

st.write(
    "This dashboard presents the results of Uber trip data "
    "analysis performed using PySpark."
)

# -------------------------------------------------
# FILE PATH
# -------------------------------------------------

OUTPUT_FOLDER = "output"

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------

cleaned_file = os.path.join(
    OUTPUT_FOLDER,
    "cleaned_uber_data.csv"
)

category_file = os.path.join(
    OUTPUT_FOLDER,
    "category_analysis.csv"
)

purpose_file = os.path.join(
    OUTPUT_FOLDER,
    "purpose_analysis.csv"
)

start_file = os.path.join(
    OUTPUT_FOLDER,
    "start_location_analysis.csv"
)

stop_file = os.path.join(
    OUTPUT_FOLDER,
    "stop_location_analysis.csv"
)

monthly_file = os.path.join(
    OUTPUT_FOLDER,
    "monthly_analysis.csv"
)

miles_file = os.path.join(
    OUTPUT_FOLDER,
    "miles_analysis.csv"
)

duration_file = os.path.join(
    OUTPUT_FOLDER,
    "duration_analysis.csv"
)

# -------------------------------------------------
# CHECK FILES
# -------------------------------------------------

if not os.path.exists(cleaned_file):
    st.error(
        "Output files not found. Please run "
        "uber_analysis.py first."
    )
    st.stop()

# -------------------------------------------------
# READ CSV FILES
# -------------------------------------------------

df = pd.read_csv(cleaned_file)

category_df = pd.read_csv(category_file)
purpose_df = pd.read_csv(purpose_file)
start_df = pd.read_csv(start_file)
stop_df = pd.read_csv(stop_file)
monthly_df = pd.read_csv(monthly_file)
miles_df = pd.read_csv(miles_file)
duration_df = pd.read_csv(duration_file)

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------

st.sidebar.header("Filters")

categories = ["All"] + sorted(
    df["CATEGORY"].dropna().unique().tolist()
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories
)

purposes = ["All"] + sorted(
    df["PURPOSE"].dropna().unique().tolist()
)

selected_purpose = st.sidebar.selectbox(
    "Select Trip Purpose",
    purposes
)

# -------------------------------------------------
# APPLY FILTERS
# -------------------------------------------------

filtered_df = df.copy()

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["CATEGORY"] == selected_category
    ]

if selected_purpose != "All":
    filtered_df = filtered_df[
        filtered_df["PURPOSE"] == selected_purpose
    ]

# -------------------------------------------------
# CALCULATE DASHBOARD METRICS
# -------------------------------------------------

total_trips = len(filtered_df)

total_miles = filtered_df["MILES"].sum()

average_miles = filtered_df["MILES"].mean()

average_duration = filtered_df[
    "DURATION_MINUTES"
].mean()

# -------------------------------------------------
# KPI CARDS
# -------------------------------------------------

st.header("📊 Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Trips",
    f"{total_trips:,}"
)

col2.metric(
    "Total Miles",
    f"{total_miles:,.2f}"
)

col3.metric(
    "Average Trip Miles",
    f"{average_miles:.2f}"
)

col4.metric(
    "Average Duration",
    f"{average_duration:.2f} min"
)

# -------------------------------------------------
# CATEGORY ANALYSIS
# -------------------------------------------------

st.header("🚗 Trip Category Analysis")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Business vs Personal")

    category_chart = category_df.set_index(
        "CATEGORY"
    )

    st.bar_chart(category_chart["count"])

with col2:

    st.subheader("Category Data")

    st.dataframe(
        category_df,
        use_container_width=True
    )

# -------------------------------------------------
# PURPOSE ANALYSIS
# -------------------------------------------------

st.header("🎯 Trip Purpose Analysis")

col1, col2 = st.columns(2)

with col1:

    purpose_chart = purpose_df.set_index(
        "PURPOSE"
    )

    st.bar_chart(purpose_chart["count"])

with col2:

    st.dataframe(
        purpose_df,
        use_container_width=True
    )

# -------------------------------------------------
# LOCATION ANALYSIS
# -------------------------------------------------

st.header("📍 Location Analysis")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Top 10 Start Locations")

    start_chart = start_df.set_index(
        "START"
    )

    st.bar_chart(start_chart["count"])

with col2:

    st.subheader("Top 10 Stop Locations")

    stop_chart = stop_df.set_index(
        "STOP"
    )

    st.bar_chart(stop_chart["count"])

# -------------------------------------------------
# MONTHLY ANALYSIS
# -------------------------------------------------

st.header("📅 Monthly Trip Analysis")

monthly_chart = monthly_df.set_index(
    "MONTH"
)

st.line_chart(
    monthly_chart["count"]
)

# -------------------------------------------------
# MILES ANALYSIS
# -------------------------------------------------

st.header("📏 Miles Analysis")

miles_data = miles_df.iloc[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Miles",
    f"{miles_data['TOTAL_MILES']:,.2f}"
)

col2.metric(
    "Average Miles",
    f"{miles_data['AVERAGE_MILES']:.2f}"
)

col3.metric(
    "Minimum Miles",
    f"{miles_data['MINIMUM_MILES']:.2f}"
)

col4.metric(
    "Maximum Miles",
    f"{miles_data['MAXIMUM_MILES']:.2f}"
)

# -------------------------------------------------
# DURATION ANALYSIS
# -------------------------------------------------

st.header("⏱️ Trip Duration Analysis")

duration_data = duration_df.iloc[0]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Duration",
    f"{duration_data['TOTAL_DURATION_MINUTES']:,.0f} min"
)

col2.metric(
    "Average Duration",
    f"{duration_data['AVERAGE_DURATION_MINUTES']:.2f} min"
)

col3.metric(
    "Minimum Duration",
    f"{duration_data['MINIMUM_DURATION_MINUTES']:.2f} min"
)

col4.metric(
    "Maximum Duration",
    f"{duration_data['MAXIMUM_DURATION_MINUTES']:.2f} min"
)

# -------------------------------------------------
# DATA PREVIEW
# -------------------------------------------------

st.header("📋 Cleaned Uber Data")

st.dataframe(
    filtered_df.head(100),
    use_container_width=True
)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.success(
    "Dashboard created using PySpark analysis and Streamlit."
)