import streamlit as st
import plotly.express as px
import pandas as pd
import seaborn as sns 
import matplotlib.pyplot as plt

file_path = "adsl.xlsx"
data = pd.read_excel(file_path)

age_group=['<65','65-80','>80']
data['AGEGR1']=pd.Categorical(data['AGEGR1'],categories=age_group,ordered=True)
def create_disposition_donut_plots(data,variable):
    figs = {}
    for group in data['ARM'].unique():
        filtered_data = data[data['ARM'] == group]
        fig = px.pie(filtered_data, names=variable, hole=0.5, 
                     title=f'Disposition Summary in {group} Group')
        fig.update_layout(margin=dict(t=50, b=0, l=0, r=0), height=300)  
        figs[group] = fig
    return figs

def create_distribution_plots(data, parameter):
    figs = {}
    for group in data['ARM'].unique():
        filtered_data = data[data['ARM'] == group]
        fig = px.box(filtered_data, x='SEX', y=parameter, 
                     title=f'{parameter} Distribution by Gender in {group} Group')
        fig.update_layout(margin=dict(t=50, b=0, l=0, r=0), height=300)
        figs[group] = fig
    return figs

def create_subject_count_bar_plot(data):
    figs = {}
    for group in data['ARM'].unique():
        filtered_data = data[data['ARM'] == group]
        subject_count = filtered_data.groupby(by=['AGEGR1','SEX'])['SUBJID'].nunique().reset_index()  
        fig = px.bar(subject_count, x='AGEGR1', y='SUBJID', color='SEX',barmode='group',title=f'Number of Subjects by AGE Group in {group} Group')
        fig.update_layout(xaxis_title='AGE Group', yaxis_title='Number of Subjects', margin=dict(t=50, b=0, l=0, r=0), height=300)
        figs[group] = fig
    return figs

st.set_page_config(layout="wide")  
st.title("DEMOGRAPHICS")

st.write("Select a variable to display donut plot:")
col1, col2, col3 = st.columns(3)

with col1:
    demographic_option=st.selectbox('Select a Variable to view Demographics',('Race','Ethinicity','Disposition'))
    if demographic_option=='Disposition':
        selected_variable='DCDECOD'
    elif demographic_option=='Ethinicity':
        selected_variable='ETHNIC'
    elif demographic_option=='Race':
        selected_variable='RACE'


with col2:
    distribution_option=st.selectbox('Select type of Distribution',('BMI','Weight','Height'))
    if distribution_option=='BMI':
        selected_characteristic='BMIBL'
    elif distribution_option=='Weight':
        selected_characteristic='WEIGHTBL'
    elif distribution_option=='Height':
        selected_characteristic='HEIGHTBL'

with col3:
    treatment_option=st.selectbox('Select type of Treatment',('Placebo','Xanomelline Low Dose','Xanomelline High Dose'))
    if treatment_option=='Placebo':
        selected_treatment='Placebo'
    elif treatment_option=='Xanomelline Low Dose':
        selected_treatment='Xanomeline Low Dose'
    elif treatment_option=='Xanomelline High Dose':
        selected_treatment='Xanomeline High Dose'

disposition_plots = create_disposition_donut_plots(data,selected_variable)

with col1:
    st.plotly_chart(disposition_plots[selected_treatment], use_container_width=True)

distribution_plots = create_distribution_plots(data, selected_characteristic)

with col2:
    st.plotly_chart(distribution_plots[selected_treatment], use_container_width=True)

subject_count_plots = create_subject_count_bar_plot(data)

with col3:
    st.plotly_chart(subject_count_plots[selected_treatment], use_container_width=True)


