import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
@st.cache
def load_data():
    return pd.read_csv('filtered_data.csv')

filtered_data_df = load_data()

# Streamlit app
st.title("Environmental Measurements Dashboard")

# Cascading Filters
state = st.selectbox("Select State", filtered_data_df['State'].unique())
county_options = filtered_data_df[filtered_data_df['State'] == state]['County'].unique()
county = st.selectbox("Select County", county_options)
material_options = filtered_data_df[
    (filtered_data_df['State'] == state) & (filtered_data_df['County'] == county)
]['Material'].unique()
material = st.selectbox("Select Material", material_options)

# Select graph type
graph_type = st.radio("Select Graph Type", ['Bar Graph', 'Line Graph'])

# Filter data based on selections
filtered_data = filtered_data_df[
    (filtered_data_df['State'] == state) &
    (filtered_data_df['County'] == county) &
    (filtered_data_df['Material'] == material)
]

if filtered_data.empty:
    st.warning("No data available for the selected options.")
else:
    # Handle the Month/Year column
    st.write("Preview of Month/Year Column:", filtered_data['Month/Year'].unique())
    filtered_data['Month/Year'] = pd.to_datetime(filtered_data['Month/Year'], errors='coerce')

    # Drop rows with invalid or missing Month/Year values
    filtered_data = filtered_data.dropna(subset=['Month/Year'])

    # Extract Year and Month for graphing
    filtered_data['Year'] = filtered_data['Month/Year'].dt.year
    filtered_data['Month'] = filtered_data['Month/Year'].dt.month

    # Bar Graph
    if graph_type == 'Bar Graph':
        st.subheader(f"Bar Graph on {material} in {county}, {state}")
        monthly_data = filtered_data.pivot(index='Year', columns='Month', values='Monthly Measurements')

        # Yearly average
        yearly_avg = filtered_data['Yearly Measurement Average'].mean()

        # Plot bar graph
        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_data.plot(kind='bar', stacked=False, ax=ax)
        ax.axhline(y=yearly_avg, color='red', linestyle='--', label='Yearly Average')
        ax.set_xlabel('Year')
        ax.set_ylabel(f"Monthly {material} ({'µg/m³' if material == 'PM2.5' else 'ppm' if material in ['CO', 'Ozone'] else 'ppb'})")
        ax.set_title(f"Bar Graph on {material} in {county}, {state}")
        ax.legend()
        st.pyplot(fig)

    # Line Graph
    else:
        st.subheader(f"Line Graph on {material} in {county}, {state}")
        line_data = filtered_data.groupby('Month/Year')['Monthly Measurements'].mean()

        # Plot line graph
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(line_data.index, line_data.values, label=f"{material} Measurements", marker='o')
        ax.set_xlabel('Year')
        ax.set_ylabel(f"Monthly {material} ({'µg/m³' if material == 'PM2.5' else 'ppm' if material in ['CO', 'Ozone'] else 'ppb'})")
        ax.set_title(f"Line Graph on {material} in {county}, {state}")
        ax.legend()
        st.pyplot(fig)
