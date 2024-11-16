import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load data
final_data_file = "https://raw.githubusercontent.com/<your-repo>/main/final_data.csv"
site_county_file = "https://raw.githubusercontent.com/<your-repo>/main/site_county_materials.csv"

final_data = pd.read_csv(final_data_file)
site_county_data = pd.read_csv(site_county_file)

# Define states (only North Dakota for now)
states = ["North Dakota", "Montana", "Minnesota", "Michigan", "Wisconsin"]

# Define materials
materials = ["PM2.5", "NO2", "Ozone", "CO", "AQI"]

# Streamlit app layout
st.title("Air Quality Data Visualization")

# User inputs
state = st.selectbox("Select a State:", states)
material = st.selectbox("Select Material:", materials)
graph_type = st.radio("Select Graph Type:", ["Bar", "Line"])
county_option = st.radio("View Data For:", ["All Counties", "Individual County"])

# Filter data by state (currently only North Dakota)
filtered_data = final_data[final_data["State"] == state]

# Filter data by material
filtered_data = filtered_data[filtered_data["Material"] == material]

# Extract county names for the state
counties = site_county_data[site_county_data["Material"] == material]["County"].unique()

# Select county if "Individual County" is chosen
if county_option == "Individual County":
    county = st.selectbox("Select a County:", counties)
    filtered_data = filtered_data[filtered_data["County"] == county]

# Process data for visualization
filtered_data["Year"] = pd.to_datetime(filtered_data["Date"]).dt.year

# Compute state average for the chosen material
state_avg = (
    filtered_data.groupby("Year")["Daily Measurements"].mean().reset_index(name="State Average")
)

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
if graph_type == "Line":
    if county_option == "All Counties":
        # Plot multiple lines for all counties
        for county in counties:
            county_data = filtered_data[filtered_data["County"] == county]
            county_avg = county_data.groupby("Year")["Daily Measurements"].mean()
            ax.plot(county_avg.index, county_avg.values, label=county)
        # Add state average line
        ax.plot(state_avg["Year"], state_avg["State Average"], label="State Average", linestyle="--")
    else:
        # Plot line for the selected county and state average
        county_data = filtered_data[filtered_data["County"] == county]
        county_avg = county_data.groupby("Year")["Daily Measurements"].mean()
        ax.plot(county_avg.index, county_avg.values, label=county)
        ax.plot(state_avg["Year"], state_avg["State Average"], label="State Average", linestyle="--")
elif graph_type == "Bar":
    if county_option == "All Counties":
        # Plot bars for all counties with state average
        for county in counties:
            county_data = filtered_data[filtered_data["County"] == county]
            county_avg = county_data.groupby("Year")["Daily Measurements"].mean()
            ax.bar(county_avg.index, county_avg.values, label=county, alpha=0.7)
        ax.axhline(y=state_avg["State Average"].mean(), color="red", linestyle="--", label="State Average")
    else:
        # Plot bars for the selected county and state average
        county_data = filtered_data[filtered_data["County"] == county]
        county_avg = county_data.groupby("Year")["Daily Measurements"].mean()
        ax.bar(county_avg.index, county_avg.values, label=county, alpha=0.7)
        ax.axhline(y=state_avg["State Average"].mean(), color="red", linestyle="--", label="State Average")

# Customize the plot
y_label = "Daily Measurements (units)"  # Adjust unit dynamically if needed
ax.set_xlabel("Year")
ax.set_ylabel(y_label)
if county_option == "All Counties":
    title = f"{material} Measurements Overview in {state}"
else:
    title = f"{material} Measurements for {county}, {state}"
ax.set_title(title)
ax.legend()
ax.grid(True)

# Display the plot
st.pyplot(fig)
