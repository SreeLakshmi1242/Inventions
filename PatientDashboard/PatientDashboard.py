import streamlit as st
# from st_aggrid import GridOptionsBuilder,AgGrid
import plotly.express as px
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="CharmHealth CodeRx Hackathon!!!",page_icon=":bar_chart:",layout="wide")


# with col:

#     st.title(" :bar_chart: Patient Dashboard")
#     st.markdown("<style>div.block-container{padding-top:1rem;)</style>",unsafe_allow_html=True)

with st.container():
    col,colc = st.columns(2)
    with col:
        st.markdown("<style>div.block-container{padding-top:3rem;}</style>", unsafe_allow_html=True)
        st.title(":bar_chart: Patient Dashboard")


    current_dir = os.getcwd()

# Relative path to the data file
    data_file = os.path.join(current_dir, "PatientDashboard/500_Patient_Sample.csv")

    with colc:  
        with st.container():
            fl=st.file_uploader(":file_folder: upload a file",type=(["csv","txt","xlsx","xls"]))
            if fl is not None:
                filename=fl.name
                st.write(filename)
                df= pd.read_csv(filename)
            else:
                # os.chdir(r"/Users/sree/Hackathon")
                df = pd.read_csv(data_file)

# Data cleaning
df['Appointment No']=df.groupby(['Patient ID'])['SNo'].rank().astype(int)
last_app= df.iloc[df.groupby(['Patient ID','Gender'])['Appointment No'].idxmax()]

# create filter box

st.sidebar.header("Patients: ")
patient = st.sidebar.selectbox("Pick your Patient ID",df['Patient ID'].unique())

if not patient:
    df2 = last_app.copy()
else:
    df2 = last_app[last_app['Patient ID'].isin([patient])]
    
filter_df = df2.copy()

total_appointment = filter_df['Appointment No'].fillna('Not Available').max()
gender =  filter_df['Gender'].fillna('Not Available').max().capitalize()
age = filter_df['Age'].fillna('Not Available').max()
weight = filter_df['Weight'].fillna('Not Available').max()
height = filter_df['Height'].fillna('Not Available').max()

st.sidebar.header("Appointment: ")
app_no = st.sidebar.selectbox("Pick the appointment",df[df['Patient ID'].isin([patient])]['Appointment No'].unique()[::-1])

if not patient:
    df3 = df[df['Patient ID'].isin([patient])].copy()
else:
    df3 = df[(df['Patient ID'].isin([patient])) & (df['Appointment No'].isin([app_no]))]
    
app_df = df3.copy()

temp = app_df['Temperature'].max()
disys = app_df['BP DISYS'].max()
sys = app_df['BP SYS'].max()
pulse_rate = app_df['Pulse Rate'].max()
resp_rate = app_df['Respiratory Rate'].max()
# pulse_vol = filter_df['Pulse Volume'].max()
# pulse_pat = filter_df['Pulse Pattern'].max()
# resp_pat = filter_df['Respiration Pattern'].max()
smok_stat = app_df['Smoking Status'].max()

# st.markdown("""
# <style>
# div[data-testid="metric-container"] {
#    background-color: rgba(90, 11, 100, 0.2);
#    border: 1px solid rgba(68, 131, 225, 0.6);
#    padding: 5% 5% 5% 5%;
#    border-radius: 10px;
#    color: rgb(17, 600, 100);
#    overflow-wrap: break-word;
# }
# }

# /* breakline for metric text         */
# div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
#    overflow-wrap: break-word;
#    white-space: break-spaces;
#    color: white;
# </style>
# """
# , unsafe_allow_html=True)


st.subheader(":blue[Patient Summary]")
col1, col2, col3,col4 = st.columns(4)
col1.metric("Patient ID",patient)
col1.metric("Gender",gender)
col2.metric("Age",age)
col2.metric("Weight",weight)
col3.metric("Height",height)
col3.metric("Total Appointments",total_appointment)


# st.subheader(":blue[Last appointment details]")

# col5, col6, col7, col8 = st.columns(4)
# col3.metric("Weight",weight)
# col4.metric("Height",height)
# col3.metric("Temperature",temp)
# col4.metric("Smoking Status",smok_stat)

col_c1,col_c2 = st.columns(2)
with col_c1:
    st.subheader(":blue[Appointment details]")

    data={"Metrics":["BP Systolic","BP Diastolic","Pulse Rate","Respiratory Rate"],
                              "Values":[disys,sys,pulse_rate,resp_rate],
         "Min":[0,0,60,12],"Max":[120,80,100,18]}

    other_vals = pd.DataFrame(data)
    # other_vals['Values'] = other_vals['Values'].astype(int)
    other_vals['color']=np.where((other_vals['Values']>=other_vals['Min']) & (other_vals['Values']<=other_vals['Max']),"green","red")
    other_vals['Status'] = np.where(other_vals['color']=='red',"Risky","Normal")

    fig = px.bar(
        other_vals,x="Values",y="Metrics",orientation="h",
            color_discrete_sequence = [other_vals['color']]*len(other_vals),
         text=str("Status"),height = 300,width=800)

    st.plotly_chart(fig,use_container_width=True)

    # diag = app_df['Diagnosis Codes'].str.split(";").explode().fillna("Not Available")
    # prescrip = app_df['Prescriptions'].str.split(";").explode().fillna("Not Available")
    # diag_pres = pd.concat([diag[(diag.str.len()>0) & (diag.notna())],prescrip[(prescrip.str.len()>0) & (prescrip.notna())]],axis=1).fillna("Not Available")
    
    # Check for valid data
    diag = app_df['Diagnosis Codes'].str.split(";").explode().fillna("")
    prescrip = app_df['Prescriptions'].str.split(";").explode().fillna("")

    # Clean data: Remove duplicates and reset index
    diag = diag[diag.str.len() > 0].drop_duplicates().reset_index(drop=True)
    prescrip = prescrip[prescrip.str.len() > 0].drop_duplicates().reset_index(drop=True)

    # Handle unequal lengths by aligning with an index
    max_len = max(len(diag), len(prescrip))
    diag = diag.reindex(range(max_len), fill_value="")
    prescrip = prescrip.reindex(range(max_len), fill_value="")

    # Concatenate as DataFrame
    diag_pres = pd.DataFrame({
        "Diagnosis Codes": diag,
        "Prescriptions": prescrip
    })

    # Output the concatenated result
    # st.write("Combined Diagnosis and Prescriptions:", diag_pres)

    diagnosis = 'Diagnosis : ' +','.join(diag_pres["Diagnosis Codes"].unique())
    prescription = 'Prescriptions : ' + ','.join(diag_pres["Prescriptions"].unique())
    

#     st.text("Diagnosis : ")     
    st.text(diagnosis)
    st.text(prescription)


#     cola,colb = st.columns(2)
#     with cola:
#         st.dataframe(
#             diag[(diag.str.len()>0) & (diag.notna())],
#             column_config={
#                 "Diagnosis Codes": "Diagnosis",
#                 "Prescriptions": "Prescriptions"
#             },
#             hide_index=True, width = 500
#         )
#     with colb:
#         st.dataframe(
#            prescrip[(prescrip.str.len()>0) & (prescrip.notna())],
#             column_config={
#                 "Diagnosis Codes": "Diagnosis",
#                 "Prescriptions": "Prescriptions"
#             },
#             hide_index=True,width =500
#         )
    

if not patient:
    df4 = df.copy()
else:
    df4 = df[df['Patient ID'].isin([patient])]

# df4=df4.rename(columns={'Appointment No':'index'}).set_index('index').copy()

# st.line_chart(fil['Pulse Rate'])
# resp=pd.DataFrame({"Respiratory Rate":[df4['Respiratory Rate'].fillna(0).to_list()]})
# pulse=pd.DataFrame({"Pulse Rate":[df4['Pulse Rate'].fillna(0).to_list()]})
# bp_disys=pd.DataFrame({"BP Diastolic":[df4['BP SYS'].fillna(0).to_list()]})
# bp_sys=pd.DataFrame({"BP Systolic":[df4['BP DISYS'].fillna(0).to_list()]})


with col4:
    st.subheader(":blue[Over all Health]")
#     st.data_editor(
#   resp,
#     column_config={
#         "Respiratory Rate": st.column_config.BarChartColumn(
#             "Respiratory Rate"
#         ),
#     },
#     hide_index=True,
# )
#     st.data_editor(
#   pulse,
#     column_config={
#         "Pulse Rate": st.column_config.BarChartColumn(
#             "Pulse Rate"
#         ),
#     },
#     hide_index=True,
# )
  
#     st.data_editor(
#       bp_disys,
#         column_config={
#             "BP Diastolic": st.column_config.BarChartColumn(
#                 "BP Diastolic"
#             ),
#         },
#         hide_index=True,
#     )
    
    
#     st.data_editor(
#     bp_sys,
#     column_config={
#         "BP Systolic": st.column_config.BarChartColumn(
#             "BP Systolic"
#         ),
#     }
#         ,
#     hide_index=True,
# )
    st.bar_chart(df4.fillna(0),x='Appointment No',y='Pulse Rate',height=170)

    with col_c2:
        col_c2_c1,col_c2_c2 =st.columns(2)
        with col_c2_c2:
            st.bar_chart(df4.fillna(0),x='Appointment No',y='Respiratory Rate',height=170)
            st.bar_chart(df4.fillna(0),x='Appointment No',y='BP DISYS',height=170)
            st.bar_chart(df4.fillna(0),x='Appointment No',y='BP SYS',height=170)
            
            


    
