import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the data from the same directory as the script
@st.cache
def load_data():
    county_df = pd.read_csv('county.csv')
    filtered_data_df = pd.read_csv('filtered_data.csv')
    return county_df, filtered_data_df

county_df, filtered_data_df = load_data()

# Streamlit app
st.title("Environmental Measurements Dashboard")

# Filters for State, Material, and County
state = st.selectbox("Select State", county_df['State'].unique())
material = st.selectbox("Select Material", ['PM2.5', 'CO', 'Ozone', 'NO2'])
county = st.selectbox("Select County", county_df[county_df['State'] == state]['County'].unique())

# Select graph type
graph_type = st.radio("Select Graph Type", ['Bar Graph', 'Line Graph'])

# Filter data
filtered_data = filtered_data_df[
    (filtered_data_df['State'] == state) &
    (filtered_data_df['County'] == county) &
    (filtered_data_df['Material'] == material)
]

if filtered_data.empty:
    st.warning("No data available for the selected options.")
else:
    # Bar Graph
    if graph_type == 'Bar Graph':
        st.subheader(f"Bar Graph on {material} in {county}, {state}")
        filtered_data['Year'] = pd.to_datetime(filtered_data['Date']).dt.year
        filtered_data['Month'] = pd.to_datetime(filtered_data['Date']).dt.month
        monthly_data = filtered_data.groupby(['Year', 'Month'])['Measurement'].mean().unstack()

        # Calculate yearly average
        yearly_avg = filtered_data.groupby('Year')['Measurement'].mean()

        # Plot bar graph
        fig, ax = plt.subplots(figsize=(12, 6))
        monthly_data.plot(kind='bar', stacked=False, ax=ax)
        ax.axhline(y=yearly_avg.mean(), color='red', linestyle='--', label='Yearly Average')
        ax.set_xlabel('Year')
        ax.set_ylabel(f"Monthly {material} ({'µg/m³' if material == 'PM2.5' else 'ppm' if material in ['CO', 'Ozone'] else 'ppb'})")
        ax.set_title(f"Bar Graph on {material} in {county}, {state}")
        ax.legend()
        st.pyplot(fig)

    # Line Graph
    else:
        st.subheader(f"Line Graph on {material} in {county}, {state}")
        filtered_data['Date'] = pd.to_datetime(filtered_data['Date'])
        line_data = filtered_data.groupby('Date')['Measurement'].mean()

        # Plot line graph
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(line_data.index, line_data.values, label=f"{material} Measurements", marker='o')
        ax.set_xlabel('Year')
        ax.set_ylabel(f"Monthly {material} ({'µg/m³' if material == 'PM2.5' else 'ppm' if material in ['CO', 'Ozone'] else 'ppb'})")
        ax.set_title(f"Line Graph on {material} in {county}, {state}")
        ax.legend()
        st.pyplot(fig)
