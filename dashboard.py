import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Load your data (replace with the correct path to your dataset)
netflix_data = pd.read_csv('netflix_content_2023.csv')

# Convert 'Release Date' to datetime format
netflix_data['Release Date'] = pd.to_datetime(netflix_data['Release Date'])

# Extract Month and Day information from 'Release Date'
netflix_data['Release Month'] = netflix_data['Release Date'].dt.month
netflix_data['Release Day'] = netflix_data['Release Date'].dt.day_name()

# Set up the Streamlit page title and layout
st.title('Netflix Content and Viewership Dashboard')
st.sidebar.title("Filter Options")

# Provide options for the selectbox
month_options = netflix_data['Release Month'].unique()
weekday_options = netflix_data['Release Day'].unique()

# Sidebar filters for interactivity
month_filter = st.sidebar.selectbox('Select Month', month_options)
weekday_filter = st.sidebar.selectbox('Select Weekday', weekday_options)

# Filter data based on selected month and weekday
filtered_data = netflix_data[(netflix_data['Release Month'] == month_filter) & 
                             (netflix_data['Release Day'] == weekday_filter)]

# Display filtered data
st.write(f"Filtered Data for Month: {month_filter} - Weekday: {weekday_filter}")
st.dataframe(filtered_data)

# --- Monthly Release Pattern and Viewership ---
monthly_releases = netflix_data['Release Month'].value_counts().sort_index()
monthly_viewership = netflix_data.groupby('Release Month')['Hours Viewed'].sum()

fig1 = go.Figure()

# Bar plot for number of releases by month
fig1.add_trace(
    go.Bar(
        x=monthly_releases.index,
        y=monthly_releases.values,
        name='Number of Releases',
        marker_color='goldenrod', 
        opacity=0.7,
        yaxis='y1'
    )
)

# Line plot for total viewership hours by month
fig1.add_trace(
    go.Scatter(
        x=monthly_viewership.index,
        y=monthly_viewership.values,
        name='Viewership Hours',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(color='red'),
        yaxis='y2'
    )
)

fig1.update_layout(
    title='Monthly Release Patterns and Viewership Hours (2023)',
    xaxis=dict(
        title='Month',
        tickmode='array',
        tickvals=list(range(1, 13)),
        ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    ),
    yaxis=dict(
        title='Number of Releases',
        showgrid=False,
        side='left'
    ),
    yaxis2=dict(
        title='Total Hours Viewed (in billions)',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(
        x=1.05,  
        y=1,
        orientation='v',
        xanchor='left'
    ),
    height=600,
    width=1000
)

st.plotly_chart(fig1)

# --- Weekly Release Patterns and Viewership ---
weekday_releases = netflix_data['Release Day'].value_counts().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

weekday_viewership = netflix_data.groupby('Release Day')['Hours Viewed'].sum().reindex(
    ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
)

fig2 = go.Figure()

# Bar plot for number of releases by weekday
fig2.add_trace(
    go.Bar(
        x=weekday_releases.index,
        y=weekday_releases.values,
        name='Number of Releases',
        marker_color='blue',
        opacity=0.6,
        yaxis='y1'
    )
)

# Line plot for total viewership hours by weekday
fig2.add_trace(
    go.Scatter(
        x=weekday_viewership.index,
        y=weekday_viewership.values,
        name='Viewership Hours',
        mode='lines+markers',
        marker=dict(color='red'),
        line=dict(color='red'),
        yaxis='y2'
    )
)

fig2.update_layout(
    title='Weekly Release Patterns and Viewership Hours (2023)',
    xaxis=dict(
        title='Day of the Week',
        categoryorder='array',
        categoryarray=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ),
    yaxis=dict(
        title='Number of Releases',
        showgrid=False,
        side='left'
    ),
    yaxis2=dict(
        title='Total Hours Viewed (in billions)',
        overlaying='y',
        side='right',
        showgrid=False
    ),
    legend=dict(
        x=1.05,  
        y=1,
        orientation='v',
        xanchor='left'
    ),
    height=600,
    width=1000
)

st.plotly_chart(fig2)

# --- Filtered Data Insights ---
st.write(f"Showing the total number of releases and viewership hours for {month_filter} month and {weekday_filter}:")
st.write(f"Total Releases: {len(filtered_data)}")
st.write(f"Total Hours Viewed: {filtered_data['Hours Viewed'].sum()} hours")

# Add a footer or conclusion section if needed
st.write("Dashboard created to visualize Netflix release and viewership data trends over 2023.")
