import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px 
import plotly.graph_objects as go
from datetime import datetime
from streamlit_option_menu import option_menu
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()

# -------------- DB Connection Functions --------------
def database_connection(local=True):
    """Connect to the MongoDB database
    
    local (bool): whether to connect to the local database or the cloud database
    """
    if local:
        client = MongoClient("localhost", 27017)
    else:
        # Get the database URI from the environment variables
        database_uri = os.getenv("DATABASE_URL")

        # Create a new client and connect to the server
        client = MongoClient(database_uri)

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(f"Could not connect to MongoDB: Exception {e}.")
    
    return client

def fetch_data_db(db_name, collection_name, date_string, bearing_num, local=True): 
    """Fetch data from the MongoDB database
    
    Args:
        db (MongoClient): the database connection
        collection_name (str): the name of the collection

    Returns:
        item_details (dict): the data from the collection
    """
    data_list = []

    client = database_connection(local=local)

    # Access a specific database
    db = client[db_name]

    # Access a specific collection (i.e Table)
    collection = db[collection_name]

    if date_string.lower() == 'all':
        # Query with conditions
        query = {
            'bN': int(bearing_num)
        }

    else:
        # Convert input date string to timestamp
        input_date = datetime.strptime(date_string, '%d-%b-%Y')
        timestamp = int(input_date.timestamp())

        # Query with conditions
        query = {
            'tS': {'$gte': timestamp, '$lt': timestamp + 86400},
            'bN': int(bearing_num)
        }

    item_details = collection.find(query)

    for item in item_details:
        # This does not give a very readable output
        data_list.append(item)

    return data_list
# --------------------------------------------------


# -------------- SETTINGS --------------
page_title = "Machine Health Monitoring"
page_icon = ":warning:"
layout = "centered"
# --------------------------------------


st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title)


# --- HIDE STREAMLIT STYLE ---
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


# --- NAVIGATION MENU ---
selected = option_menu(
    menu_title=None,
    options=["Machine Information", "Machine Health Status"],
    icons=["info-circle", "bar-chart-fill"],  # https://icons.getbootstrap.com/
    orientation="horizontal",
)

# ----------------------------- INPUT & SAVE PERIODS -----------------
if selected == "Machine Information":
    st.header(f"Asset Information", divider=True)
    st.image('artifacts/bearing.jpg', caption='Asset: IMS bearing test rig with sensors placed on each bearing.', use_column_width=True)
    st.subheader('Asset Details:')
    st.text('Four bearings installed on a shaft run by an AC motor coupled to the shaft via rub belts.\nRotational Speed = 2000 RPM \nRadial Load = 6000 lbs (applied onto the shaft and bearing by a spring mechanism) \nAll bearings are force lubricated.')
    st.subheader('Data Details:')
    st.write('Data Type: Time Series')
    st.write('Sampling Rate: 20480/sec')
    st.write('Collection Duration: 1 sec')
    st.write('Collection Frequency: Every 10 mins')
    st.write('Data Source: NASA Prognostics Center of Excellence (PCoE) Data Repository')
    st.write('Credits: [link](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)')


# --------------------- PLOT PERIODS --------------------------------
if selected == "Machine Health Status":
    st.header("Machine Health Status")
    with st.form("saved_periods"):
        bearing_num = st.selectbox("Select Bearing Number:", ['1', '2', '3', '4'])
        timestamp   = st.selectbox("Select Timestamp:", ['15-Feb-2004', '16-Feb-2004', '17-Feb-2004', '18-Feb-2004', '19-Feb-2004', 'All'])
        submitted = st.form_submit_button("Plot Health Status")
        if submitted:
            # Get data from database
            data_list = fetch_data_db(db_name="machinehealth", collection_name="test", date_string=timestamp, bearing_num=bearing_num, local=False)

            # Convert data to a Pandas DataFrame
            df = pd.DataFrame(data_list)

            df['hS'] = df['hS'].astype(str)

            df['hS'] = df['hS'].replace({'0': 'Healthy', '1': 'Faulty'})

            # Plot the data
            line_fig = px.line(df, x=np.arange(len(df)), y='rA')
            
            # Overlay a scatter plot on the line plot
            scatter_fig = px.scatter(df, x=np.arange(len(df)), y='rA', color='hS', color_discrete_sequence=['green', 'red'], labels={'rms': f'RMS (mm/s^2)', 'healthStatus': 'Health Status'},
                         title='RMS Acceleration with Health Status Overlayed')
            
            # Overlay a line plot on the scatter plot
            combined_plots = go.Figure(data=line_fig.data + scatter_fig.data, layout=scatter_fig.layout)

            # Display both plots in Streamlit
            st.plotly_chart(combined_plots)