# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

#######################
# Page configuration
st.set_page_config(
    page_title="Medical Insurance Premium Dashboard",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enable an Altair theme (using dark theme as in your sample)
alt.themes.enable("dark")

#######################
# CSS styling
st.markdown("""
<style>
[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}
[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}
[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}
[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}
[data-testid="stMetricDeltaIcon-Up"],
[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}
</style>
""", unsafe_allow_html=True)

#######################
# Load data
# Ensure that "Medicalpremium.csv" is in the same directory as this script.
medical = pd.read_csv("Medicalpremium.csv")
# Calculate BMI (retaining all original variables)
medical["BMI"] = medical["Weight"] / ((medical["Height"] / 100) ** 2)

#######################
# Sidebar for filtering
with st.sidebar:
    st.title("Medical Insurance Premium Dashboard")
    
    # Age range filter
    min_age = int(medical["Age"].min())
    max_age = int(medical["Age"].max())
    age_filter = st.slider("Select Age Range", min_age, max_age, (min_age, max_age))
    
    # Diabetes filter
    diabetes_option = st.selectbox("Diabetes Status", options=["All", "Yes", "No"])
    
    # Filter data based on sidebar selections
    df_filtered = medical[(medical["Age"] >= age_filter[0]) & (medical["Age"] <= age_filter[1])]
    if diabetes_option == "Yes":
        df_filtered = df_filtered[df_filtered["Diabetes"] == 1]
    elif diabetes_option == "No":
        df_filtered = df_filtered[df_filtered["Diabetes"] == 0]

#######################
# Dashboard Main Panel Layout: Three Columns
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Key Metrics")
    avg_premium = df_filtered["PremiumPrice"].mean()
    median_premium = df_filtered["PremiumPrice"].median()
    min_premium = df_filtered["PremiumPrice"].min()
    max_premium = df_filtered["PremiumPrice"].max()
    
    st.metric("Average Premium", f"${avg_premium:,.2f}")
    st.metric("Median Premium", f"${median_premium:,.2f}")
    st.metric("Minimum Premium", f"${min_premium:,.2f}")
    st.metric("Maximum Premium", f"${max_premium:,.2f}")

with col2:
    st.markdown("#### Premium vs. BMI Scatter Plot")
    scatter_chart = alt.Chart(df_filtered).mark_circle(size=60).encode(
        x=alt.X("BMI:Q", title="BMI"),
        y=alt.Y("PremiumPrice:Q", title="Premium Price"),
        tooltip=["Age", "PremiumPrice", "BMI"]
    ).properties(
        width=400,
        height=300,
        title="Scatter Plot of BMI vs Premium Price"
    ).interactive()
    st.altair_chart(scatter_chart, use_container_width=True)

with col3:
    st.markdown("#### Average Premium by Diabetes Status")
    # Group data by Diabetes status and calculate average premium
    df_grouped = df_filtered.groupby("Diabetes")["PremiumPrice"].mean().reset_index()
    df_grouped["Diabetes"] = df_grouped["Diabetes"].replace({0:"No", 1:"Yes"})
    bar_chart = alt.Chart(df_grouped).mark_bar().encode(
        x=alt.X("Diabetes:N", title="Diabetes"),
        y=alt.Y("PremiumPrice:Q", title="Average Premium"),
        color=alt.Color("Diabetes:N", scale=alt.Scale(scheme="blues"))
    ).properties(
        width=400,
        height=300,
        title="Average Premium by Diabetes"
    )
    st.altair_chart(bar_chart, use_container_width=True)

#######################
# Additional Visualizations

# Dataset preview table
st.markdown("### Dataset Preview")
st.dataframe(df_filtered.head())

# Histogram of Premium Price
st.markdown("#### Premium Price Distribution")
fig = px.histogram(df_filtered, x="PremiumPrice", nbins=30, 
                   title="Distribution of Premium Price", template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)
