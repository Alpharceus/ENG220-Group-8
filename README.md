# Environmental Measurements Dashboard

## Overview
This project is a **Streamlit-based web application** designed to visualize environmental measurement data collected from the **EPA (Environmental Protection Agency)** website. The app provides interactive visualizations for monthly environmental measurements across various materials, counties, and states. Users can explore the data through bar graphs and line graphs, helping them understand trends and yearly averages.

You can access the application [here](https://finalproject220group8-afsm9rca8d9fa4g9jagzmv.streamlit.app/).

## Features
- **Interactive Filters**: Select data by state, county, and material.
- **Visualization Options**:
  - **Bar Graph**: Displays monthly measurements for each year with a horizontal line showing the yearly average. The legend indicates the months corresponding to the bars.
  - **Line Graph**: Plots the trend of monthly measurements over time.
- **Dynamic Labels and Titles**: Graphs automatically adjust to the selected material and location.
- **Units of Measurement**:
  - PM2.5: µg/m³
  - CO and Ozone: ppm
  - NO2: ppb

## Data Source
The raw data was obtained from the **EPA website**, containing information about:
- Measurement values for various materials like PM2.5, CO, Ozone, and NO2.
- Geographic details including state, county, and local site.
- Monthly and yearly averages.

## Data Processing
1. **Initial Dataset**:
   - The raw data consisted of approximately 300,000 rows, covering multiple states and counties with detailed environmental measurements.
   - It included various fields such as date (`Month/Year`), geographic details, material types, measurement values, and AQI data.

2. **Preprocessing Steps**:
   - Filtered out incomplete or invalid data, keeping only rows with 100% complete records.
   - Combined the datasets for **five states** to create a unified dataset for analysis.
   - Calculated **averages** for each state, county, and local site for all materials and AQI:
     - Averages for the **line graph** represent trends over time.
     - Actual data for the **bar graph** reflects monthly measurements.
   - Reduced the dataset to about **15,000 rows** after filtering and preprocessing.

3. **Final Dataset**:
   - The processed dataset includes the following columns:
     - `Local Site Name`
     - `County`
     - `State`
     - `Material`
     - `Monthly Measurements`
     - `Yearly Measurement Average`
     - `Year` (numeric)
     - `Month` (numeric)

## How the App Works
1. **Filtering Options**:
   - Users can select a **state**, **county**, and **material** to focus on specific data.
   - Filters dynamically adjust based on available data combinations.

2. **Visualization Options**:
   - **Bar Graph**:
     - X-axis: Years, with bars representing each month's measurements.
     - Y-axis: Monthly measurement values.
     - A horizontal red dashed line indicates the yearly average measurement.
     - **Legend**: Displays the months corresponding to the bars for each year.
   - **Line Graph**:
     - X-axis: Time (monthly granularity).
     - Y-axis: Monthly measurement values.
     - The graph includes a legend indicating the material being displayed.

3. **Graph Titles**:
   - Automatically reflect the selected state, county, and material for context.

## Acknowledgments
- Data sourced from the **Environmental Protection Agency (EPA)**.
- Built with **Streamlit**, **Pandas**, and **Matplotlib**.
