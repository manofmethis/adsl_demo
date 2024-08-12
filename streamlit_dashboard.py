import streamlit as st
import pandas as pd
import plotly.express as px

file_path = 'C:\\Users\\chira\\OneDrive\\Documents\\decode\\decode_final_round_prog\\adsl.xlsx'
data = pd.read_excel(file_path)

def create_donut_plot(data, variable):
    figs = {}
    for group in data['ARM'].unique():
        filtered_data = data[data['ARM'] == group]
        fig = px.pie(filtered_data, names=variable, hole=0.5, 
                     title=f'{variable} Distribution in {group} Group')
        fig.update_layout(margin=dict(t=50, b=0, l=0, r=0), height=300)  
        figs[group] = fig
    return figs

st.set_page_config(layout="wide")  
st.title("DEMOGRAPHICS")


st.write("Select a variable to display donut plots:")

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button('DISPOSITION'):
        selected_variable = 'DCDECOD'
with col2:
    if st.button('ETHNICITY'):
        selected_variable = 'ETHNIC'
with col1:
    if st.button('RACE'):
        selected_variable = 'RACE'
with col2:
    if st.button('GENDER'):
        selected_variable = 'SEX'

if 'selected_variable' not in locals():
    selected_variable = 'RACE'

with col3: 
    if st.button('BMI'):
        selected_baseline_value='BMIBL'
    if st.button('Height'):
        selected_baseline_value='HEIGHTBL'
    if st.button('Weight'):
        selected_baseline_value='WEIGHTBL'

if 'selected_baseline_value' not in locals():
    selected_baseline_value='BMIBL'

donut_plots = create_donut_plot(data, selected_variable)

col1, col2, col3 = st.columns([1, 1, 1])

def create_box_plot(data, variable,parameter):
    figs = {}
    for group in data['ARM'].unique():
        filtered_data = data[data['ARM'] == group]
        fig = px.box(filtered_data,x=variable,y=parameter,title=f'{variable} distribution in {group} Treatment')
        #fig.update_layout(margin=dict(t=50, b=0, l=0, r=0), height=300)  
        figs[group] = fig
    return figs
def create_bar_plots(data,variable):
    figs={}

    for group in data['ARM'].unique():
        filtered_data=pd.DataFrame(data[data['ARM']==group])
        filtered_data=filtered_data.groupby([variable,'AGEGR1'])['STUDYID'].count().reset_index()
        fig=px.bar(filtered_data,x='AGEGR1',y='STUDYID',color=variable,barmode='group',title=f'AGE distribution in the {variable} in each {group} Treatment')
        figs[group]=fig
    return figs


box_plots=create_box_plot(data,selected_variable,selected_baseline_value)
with col1:
    st.plotly_chart(donut_plots['Placebo'], use_container_width=True)
with col2:
    st.plotly_chart(donut_plots['Xanomeline Low Dose'], use_container_width=True)
with col3:
    st.plotly_chart(donut_plots['Xanomeline High Dose'], use_container_width=True)


with col1:
    st.plotly_chart(box_plots['Placebo'],use_container_width=True)
with col2:
    st.plotly_chart(box_plots['Xanomeline Low Dose'],use_container_width=True)
with col3:
    st.plotly_chart(box_plots['Xanomeline High Dose'],use_container_width=True)
bar_plots=create_bar_plots(data,selected_variable)

with col1:
    st.plotly_chart(bar_plots['Placebo'],use_container_width=True)
with col2:
    st.plotly_chart(bar_plots['Xanomeline Low Dose'],use_container_width=True)
with col3: 
    st.plotly_chart(bar_plots['Xanomeline High Dose'],use_container_width=True)
