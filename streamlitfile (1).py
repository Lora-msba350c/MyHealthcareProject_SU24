import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the data
@st.cache_data
def load_data():
    data = pd.read_csv('data_diseases.csv')
    data.columns = data.columns.str.strip()
    return data

data = load_data()

# Convert disease columns to numeric, handling non-numeric values gracefully
diseases = ['Alzheimers_and_other_dementias', 'CRD', 'Diabetes_and_Kidney', 'tracheal_bronchus_lung cancer', 'CVD']
for disease in diseases:
    data[disease] = pd.to_numeric(data[disease], errors='coerce')

# Load additional data for the third visualization
@st.cache_data
def load_additional_data():
    alzheimer_healthcare_data = pd.read_csv('alzheimer_healthcare_data.csv')
    alzheimer_healthcare_data.columns = alzheimer_healthcare_data.columns.str.strip()
    return alzheimer_healthcare_data

alzheimer_healthcare_data = load_additional_data()

# Load income data
@st.cache_data
def load_income_data():
    alzheimer_income_data = pd.read_csv('alzheimer_income_data.csv')
    alzheimer_income_data.columns = alzheimer_income_data.columns.str.strip()
    return alzheimer_income_data

alzheimer_income_data = load_income_data()

# Set up the page
st.title('Air Pollution and its Impact on Cognitive Health')

# Visualization 1: PM Levels Trends Across Years
st.header('PM2.5 Air Pollution Levels by Country Over Years')
selected_countries = st.multiselect('Select countries:', data['country'].unique(), default=data['country'].unique()[:5])
fig1 = go.Figure()
for country in selected_countries:
    country_data = data[data['country'] == country]
    fig1.add_trace(go.Scatter(x=country_data['year'], y=country_data['PM2.5'], mode='lines+markers', name=country))

fig1.update_layout(xaxis_title='Year', yaxis_title='PM2.5 Levels')
st.plotly_chart(fig1, use_container_width=True)

# Visualization 2: Disease DALY Trends Across Years
st.header('Alzheimers and Other Diseases DALY Trends Over Time')
selected_diseases = st.multiselect('Select diseases:', diseases, default=['Alzheimers_and_other_dementias'])
fig2 = go.Figure()
for disease in selected_diseases:
    if disease in data.columns:
        disease_data = data.groupby('year')[disease].mean().reset_index()
        fig2.add_trace(go.Scatter(x=disease_data['year'], y=disease_data[disease], mode='lines+markers', name=disease.replace('_', ' ').title()))

fig2.update_layout(xaxis_title='Year', yaxis_title='DALY')
st.plotly_chart(fig2, use_container_width=True)

# Visualization 3: Burden of Diseases Across Locations
st.header("Impact of Healthcare Access Levels on Alzheimer's Disease Burden Over Time")
locations = alzheimer_healthcare_data['location'].unique()
selected_locations = st.multiselect('Select locations:', locations, default=locations[:3])
disease_columns = ['Alzheimer_burden']  # Modify this to add more disease columns if available
fig3 = go.Figure()
for location in selected_locations:
    location_data = alzheimer_healthcare_data[alzheimer_healthcare_data['location'] == location]
    for disease in disease_columns:
        if disease in location_data.columns:
            fig3.add_trace(go.Scatter(x=location_data['year'], y=location_data[disease], mode='lines+markers', name=f"{location} - {disease.replace('_burden', '').replace('_', ' ').title()}"))

fig3.update_layout(xaxis_title='Year', yaxis_title='Disease Burden')
st.plotly_chart(fig3, use_container_width=True)

# New Visualization: Alzheimer's Disease Cases Across Countries Over the Years
st.header("Alzheimer's Cases Trends Across Years by Country")
selected_countries_alzheimer = st.multiselect('Select countries for Alzheimer\'s cases:', data['country'].unique(), default=data['country'].unique()[:5])
filtered_data = data[data['country'].isin(selected_countries_alzheimer)]
avg_alzheimer_data = filtered_data.groupby(['country', 'year'])['Alzheimers_and_other_dementias'].mean().reset_index()

fig_new = px.line(avg_alzheimer_data, 
                  x='year', y='Alzheimers_and_other_dementias', color='country',
                  title='Alzheimer Cases Over Time by Country')

fig_new.update_layout(xaxis_title='Year', yaxis_title='Alzheimer Cases', legend_title_text='Country')
st.plotly_chart(fig_new, use_container_width=True)

# Visualization 4: Comparative Analysis of PM2.5 Levels and Alzheimer's Cases
st.header("Comparative Analysis: PM2.5 Levels vs Alzheimer's Cases")
selected_countries_comp = st.multiselect('Select countries for comparative analysis:', data['country'].unique(), default=data['country'].unique()[:5])
fig_comp = go.Figure()

for country in selected_countries_comp:
    country_data = data[data['country'] == country]
    fig_comp.add_trace(go.Scatter(x=country_data['PM2.5'], y=country_data['Alzheimers_and_other_dementias'], mode='markers', name=country))

fig_comp.update_layout(xaxis_title='PM2.5 Levels', yaxis_title="Alzheimer's Cases", title="PM2.5 Levels vs Alzheimer's Cases by Country")
st.plotly_chart(fig_comp, use_container_width=True)

# Visualization 5: Heat Map of Correlations
st.header("Correlation Between Diseases")
corr_data = data[['PM2.5', 'Alzheimers_and_other_dementias', 'CRD', 'Diabetes_and_Kidney', 'tracheal_bronchus_lung cancer', 'CVD']].corr()
fig4 = px.imshow(corr_data, text_auto=True, title="Correlation Heatmap", labels={"color": "Correlation"})
st.plotly_chart(fig4, use_container_width=True)

# Visualization 6: Alzheimer's Burden Across Income Levels
st.header("Alzheimer's Burden Across Income Levels")
income_levels = alzheimer_income_data['Location'].unique()
selected_income_levels = st.multiselect('Select income levels:', income_levels, default=income_levels[:2])
fig5 = go.Figure()
for income_level in selected_income_levels:
    income_data = alzheimer_income_data[alzheimer_income_data['Location'] == income_level]
    fig5.add_trace(go.Scatter(x=income_data['Year'], y=income_data['alzheimer_burden'], mode='lines+markers', name=income_level))

fig5.update_layout(xaxis_title='Year', yaxis_title="Alzheimer's Burden")
st.plotly_chart(fig5, use_container_width=True)
