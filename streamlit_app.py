import os
import streamlit as st
import plotly.graph_objects as go  
from streamlit_option_menu import option_menu
import pandas as pd
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

def fetch_data_db(db_name, collection_name, timestamp, local=True): 
    """Fetch data from the MongoDB database
    
    Args:
        db (MongoClient): the database connection
        collection_name (str): the name of the collection
        timestamp (str): the timestamp of the data to fetch
        local (bool): whether to connect to the local database or the cloud database

    Returns:
        item_details (dict): the data from the collection
    """
    data_list = []

    client = database_connection(local=local)

    # Access a specific database
    db = client[db_name]

    # Access a specific collection (i.e Table)
    collection = db[collection_name]

    item_details = collection.find({'timeStamp': timestamp})

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
st.title(page_title + " " + page_icon)


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

# --- INPUT & SAVE PERIODS ---
if selected == "Machine Information":
    st.header(f"Asset Information", divider=True)
    st.image('artifacts/bearing.png', caption='Asset: Four Bearings', use_column_width=True)
    st.subheader('Asset Details:')
    st.text('Four bearings were installed on a shaft. The rotation speed was kept constant at\n2000 RPM by an AC motor coupled to the shaft via rub belts. A radial load of \n6000 lbs is applied onto the shaft and bearing by a spring mechanism.\nAll bearings are force lubricated.')
    st.write('Credits: [link](https://www.nasa.gov/intelligent-systems-division/discovery-and-systems-health/pcoe/pcoe-data-set-repository/)')


# --- PLOT PERIODS ---
if selected == "Machine Health Status":
    st.header("Machine Health Status")
    with st.form("saved_periods"):
        bearing_num = st.selectbox("Select Bearing Number:", ['1', '2', '3', '4'])
        timestamp   = st.selectbox("Select Timestamp:", ['17-Jan-2024', '12-Feb', '13-Feb', '14-Feb', '15-Feb', '16-Feb', '17-Feb', '18-Feb', '19-Feb'])
        submitted = st.form_submit_button("Plot Health Status")
        if submitted:
            # Get data from database
            data_list = fetch_data_db(db_name='test', collection_name='collection', timestamp=timestamp, local=True)

            df = pd.DataFrame(data_list)

            st.title('RMS')
            st.line_chart(df['rmsAccel'])
            # period_data = db.get_period(period)
            # comment = period_data.get("comment")
            # expenses = period_data.get("expenses")
            # incomes = period_data.get("incomes")

            # # Create metrics
            # total_income = sum(incomes.values())
            # total_expense = sum(expenses.values())
            # remaining_budget = total_income - total_expense
            # col1, col2, col3 = st.columns(3)
            # col1.metric("Total Income", f"{total_income} {currency}")
            # col2.metric("Total Expense", f"{total_expense} {currency}")
            # col3.metric("Remaining Budget", f"{remaining_budget} {currency}")
            # st.text(f"Comment: {comment}")

            # # Create sankey chart
            # label = list(incomes.keys()) + ["Total Income"] + list(expenses.keys())
            # source = list(range(len(incomes))) + [len(incomes)] * len(expenses)
            # target = [len(incomes)] * len(incomes) + [label.index(expense) for expense in expenses.keys()]
            # value = list(incomes.values()) + list(expenses.values())

            # # Data to dict, dict to sankey
            # link = dict(source=source, target=target, value=value)
            # node = dict(label=label, pad=20, thickness=30, color="#E694FF")
            # data = go.Sankey(link=link, node=node)

            # # Plot it!
            # fig = go.Figure(data)
            # fig.update_layout(margin=dict(l=0, r=0, t=5, b=5))
            # st.plotly_chart(fig, use_container_width=True)