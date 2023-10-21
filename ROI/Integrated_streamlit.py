import streamlit as st
import pandas as pd
from snowflake.connector import connect
from snowflake.ml.modeling.preprocessing import OneHotEncoder
import json
import altair as alt
import pandas as pd
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import streamlit as st
from snowflake.snowpark.functions import *
from numpy import round
APP_ICON_URL = "https://i.imgur.com/dBDOHH3.png"


def app1():
    # Streamlit interface
    st.title("Customer Sales Prediction")

    connection = connect(
        user='NAKULSHILEDAR',
        password='13April1998$',
        account='zaplmed-dqb37133',
        warehouse='FE_AND_INFERENCE_WH',
        database='tpcds_xgboost',
        schema='demo'
    )

    # Input fields
    gender = st.selectbox("Gender", ["M", "F"])
    marital_status = st.selectbox("Marital Status", ["D", "M", "S", "U", "W"])
    credit_rating = st.selectbox("Credit Rating", ["Good", "High Risk", "Low Risk", 'Unknown'])
    education_status = st.selectbox("Education Status", ["2 yr Degree", "4 yr Degree", "Advanced Degree", "College", "Primary", "Secondary", "Unknown"])
    birth_year = st.number_input("Birth Year", value=1990)
    dependency_count = st.number_input("Dependency Count", value=1)
    

    if st.button("Predict"):
    # Create a dictionary for one-hot encoding
        input_data_dict = {
        "CD_GENDER_F": [1.0 if gender == "F" else 0.0],
        "CD_GENDER_M": [1.0 if gender == "M" else 0.0],
        "CD_MARITAL_STATUS_D": [1.0 if marital_status == "D" else 0.0],
        "CD_MARITAL_STATUS_M": [1.0 if marital_status == "M" else 0.0],
        "CD_MARITAL_STATUS_S": [1.0 if marital_status == "S" else 0.0],
        "CD_MARITAL_STATUS_U": [1.0 if marital_status == "U" else 0.0],
        "CD_MARITAL_STATUS_W": [1.0 if marital_status == "W" else 0.0],
        "CD_CREDIT_RATING_GOOD": [1.0 if credit_rating == "Good" else 0.0],
        "CD_CREDIT_RATING_HIGHRISK": [1.0 if credit_rating == "High Risk" else 0.0],
        "CD_CREDIT_RATING_LOWRISK": [1.0 if credit_rating == "Low Risk" else 0.0],
        "CD_CREDIT_RATING_UNKNOWN": [1.0 if credit_rating == "Unknown" else 0.0],
        "CD_EDUCATION_STATUS_2YRDEGREE": [1.0 if education_status == "2 yr Degree" else 0.0],
        "CD_EDUCATION_STATUS_4YRDEGREE": [1.0 if education_status == "4 yr Degree" else 0.0],
        "CD_EDUCATION_STATUS_ADVANCEDDEGREE": [1.0 if education_status == "Advanced Degree" else 0.0],
        "CD_EDUCATION_STATUS_COLLEGE": [1.0 if education_status == "College" else 0.0],
        "CD_EDUCATION_STATUS_PRIMARY": [1.0 if education_status == "Primary" else 0.0],
        "CD_EDUCATION_STATUS_SECONDARY": [1.0 if education_status == "Secondary" else 0.0],
        "CD_EDUCATION_STATUS_UNKNOWN": [1.0 if education_status == "Unknown" else 0.0],
        "C_BIRTH_YEAR": [birth_year],
        "CD_DEP_COUNT": [dependency_count]
    }

    # Create a DataFrame from the input data
        input_data_df = pd.DataFrame(input_data_dict)


    # Connect to Snowflake

    # Call Snowflake UDF
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT TPCDS_PREDICT_CLV({','.join(map(str, input_data_df.values[0]))})")
            prediction = cursor.fetchone()[0]

        st.write(f"Predicted Total Sales: {prediction}")

def app3():
    from snowflake.snowpark.functions import col
    from numpy import round


# Function to create Snowflake Session to connect to Snowflake
    def create_session():
        if "snowpark_session" not in st.session_state:
            session = Session.builder.configs(json.load(open("connection.json"))).create()
            session.use_warehouse("SNOWPARK_DEMO_WH")
            session.use_database("SNOWPARK_ROI_DEMO")
            session.use_schema("AD_DATA")
            st.session_state['snowpark_session'] = session
        else:
            session = st.session_state['snowpark_session']
        return session

    # Function to load last six months' budget allocations and ROI
    @st.cache_data(show_spinner=False)
    def load_data():
        historical_data = session.table("BUDGET_ALLOCATIONS_AND_ROI").unpivot("Budget", "Channel", ["SearchEngine", "SocialMedia", "Video", "Email"]).filter(col("MONTH") != "July")
        df_last_six_months_allocations = historical_data.drop("ROI").to_pandas()
        df_last_six_months_roi = historical_data.drop(["CHANNEL", "BUDGET"]).distinct().to_pandas()
        df_last_months_allocations = historical_data.filter(col("MONTH") == "June").to_pandas()
        return historical_data.to_pandas(), df_last_six_months_allocations, df_last_six_months_roi, df_last_months_allocations

    # Streamlit config
    
    st.write("<style>[data-testid='stMetricLabel'] {min-height: 0.5rem !important}</style>", unsafe_allow_html=True)
    st.image(APP_ICON_URL, width=80)
    st.title("SportsCo Ad Spend Optimizer")

    # Call functions to get Snowflake session and load data
    session = create_session()
    historical_data, df_last_six_months_allocations, df_last_six_months_roi, df_last_months_allocations = load_data()

    # Display advertising budget sliders and set their default values
    st.header("Advertising budgets")
    col1, _, col2 = st.columns([4, 1, 4])
    channels = ["Search engine", "Social media", "Email", "Video"]
    budgets = []
    for channel, default, col in zip(channels, df_last_months_allocations["BUDGET"].values, [col1, col1, col2, col2]):
        with col:
            budget = st.slider(channel, 0, 100, int(default), 5)
            budgets.append(budget)

    # Function to call "predict_roi" UDF that uses the pre-trained model for inference
    # Note: Both the model training and UDF registration is done in Snowpark_For_Python.ipynb
    st.header("Predicted revenue")
    @st.cache_data(show_spinner=False)
    def predict(budgets):
        df_predicted_roi = session.sql(f"SELECT predict_roi(array_construct({budgets[0]*1000},{budgets[1]*1000},{budgets[2]*1000},{budgets[3]*1000})) as PREDICTED_ROI").to_pandas()
        predicted_roi, last_month_roi = df_predicted_roi["PREDICTED_ROI"].values[0] / 100000, df_last_six_months_roi["ROI"].iloc[-1]
        change = round((predicted_roi - last_month_roi) / last_month_roi * 100, 1)
        return predicted_roi, change

    # Call predict function upon user interaction -- i.e. everytime the sliders are changed -- to get a new predicted ROI
    predicted_roi, change = predict(budgets)
    st.metric("", f"$ {predicted_roi:.2f} million", f"{change:.1f} % vs last month")
    months = ["January", "February", "March", "April", "May", "June", "July"]
    july = pd.DataFrame({"MONTH": ["July", "July", "July", "July"], "CHANNEL": ["SEARCHENGINE", "SOCIALMEDIA", "VIDEO", "EMAIL"], "BUDGET": budgets, "ROI": [predicted_roi] * 4})
    chart_data = pd.concat([historical_data,july]).reset_index(drop=True)
    chart_data = chart_data.replace(["SEARCHENGINE", "EMAIL", "SOCIALMEDIA", "VIDEO"], ["Search engine", "Email", "Social media", "Video"])

    # Display allocations and ROI charts
    # Note: Streamlit docs on charts can be found here: https://docs.streamlit.io/library/api-reference/charts
    base = alt.Chart(chart_data).encode(alt.X("MONTH", sort=months, title=None))
    bars = base.mark_bar().encode(
        y=alt.Y("BUDGET", title="Budget", scale=alt.Scale(domain=[0, 400])),
        color=alt.Color("CHANNEL", legend=alt.Legend(orient="top", title=" ")),
        opacity=alt.condition(alt.datum.MONTH == "July", alt.value(1), alt.value(0.3)),
    )
    lines = base.mark_line(size=3).encode(
        y=alt.Y("ROI", title="Revenue", scale=alt.Scale(domain=[0, 25])),
        color=alt.value("#808495"),
        tooltip=["ROI"],
    )
    points = base.mark_point(strokeWidth=3).encode(
        y=alt.Y("ROI"),
        stroke=alt.value("#808495"),
        fill=alt.value("white"),
        size=alt.condition(alt.datum.MONTH == "July", alt.value(300), alt.value(70)),
    )
    chart = alt.layer(bars, lines + points).resolve_scale(y="independent")
    chart = chart.configure_view(strokeWidth=0).configure_axisY(domain=False).configure_axis(labelColor="#808495", tickColor="#e6eaf1", gridColor="#e6eaf1", domainColor="#e6eaf1", titleFontWeight=600, titlePadding=10, labelPadding=5, labelFontSize=14).configure_range(category=["#FFE08E", "#03C0F2", "#FFAAAB", "#995EFF"])
    st.altair_chart(chart, use_container_width=True)

    # Setup the ability to save user-entered allocations and predicted value back to Snowflake
    submitted = st.button("❄️ Save to Snowflake")
    if submitted:
        with st.spinner("Making snowflakes..."):
            df = pd.DataFrame({"MONTH": ["July"], "SEARCHENGINE": [budgets[0]], "SOCIALMEDIA": [budgets[1]], "VIDEO": [budgets[2]], "EMAIL": [budgets[3]], "ROI": [predicted_roi]})
            session.write_pandas(df, "BUDGET_ALLOCATIONS_AND_ROI")
            st.success("✅ Successfully wrote budgets & prediction to your Snowflake account!")
            st.snow()

    
    

    
   


def app2():
    # %%



    # %%
    # Create a session to Snowflake with credentials
    with open("creds.json") as f:
        connection_parameters = json.load(f)
    session = Session.builder.configs(connection_parameters).create()

    # %%
    # Header
    head1, head2 = st.columns([8, 1])

    with head1:
        st.header("Customer Spend Prediction Model")
    with head2:
        st.markdown(
            f' <img src="https://api.nuget.org/v3-flatcontainer/snowflake.data/0.1.0/icon" width="50" height="50"> ',
            unsafe_allow_html=True)

    st.markdown('##')
    st.markdown('##')

    # %%
    # Customer Spend Slider Column
    col1, col2, col3 = st.columns([4, 1, 10])

    session.use_warehouse('COMPUTE_WH')
    session.use_database('predict_customer_spend')
    session.use_schema('data')

    customer_df = session.table('PREDICT_CUSTOMER_SPEND.DATA.PREDICTED_CUSTOMER_SPEND')

    # Read Data
    minasl, maxasl, mintoa, maxtoa, mintow, maxtow, minlom, maxlom = customer_df.select(
        floor(min(col("Avg. Session Length"))),
        ceil(max(col("Avg. Session Length"))),
        floor(min(col("Time on App"))),
        ceil(max(col("Time on App"))),
        floor(min(col("Time on Website"))),
        ceil(max(col("Time on Website"))),
        floor(min(col("Length of Membership"))),
        ceil(max(col("Length of Membership")))
    ).toPandas().iloc[0, ]

    minasl = int(minasl)
    maxasl = int(maxasl)
    mintoa = int(mintoa)
    maxtoa = int(maxtoa)
    mintow = int(mintow)
    maxtow = int(maxtow)
    minlom = int(minlom)
    maxlom = int(maxlom)

    # Column 1
    with col1:
        st.markdown("#### Search Criteria")
        st.markdown('##')
        asl = st.slider("Session Length", minasl, maxasl, (minasl, minasl+5), 1)
        #st.write("Session Length ", asl)
        toa = st.slider("Time on App", mintoa, maxtoa, (mintoa, mintoa+5), 1)
        #st.write("Time on App ", toa)
        tow = st.slider("Time on Website", mintow, maxtow, (mintow, mintow+5), 1)
        #st.write("Time on Website ", tow)
        lom = st.slider("Length of Membership", minlom,
                        maxlom, (minlom, minlom+4), 1)
        #st.write("Length of Membership ", lom)

    # Column 2 (3)
    with col3:
        #avg_sess_len = st.slider("Avg. Session Length", min_sess_len, max_sess_len, (min_sess_len,min_sess_len+1), 1)
        st.markdown("#### Customer Predicted Spend")
        st.markdown('##')

        minspend, maxspend = customer_df.filter(
            (col("Avg. Session Length") <= asl[1]) & (
                col("Avg. Session Length") > asl[0])
            & (col("Time on App") <= toa[1]) & (col("Time on App") > toa[0])
            & (col("Time on Website") <= tow[1]) & (col("Time on Website") > tow[0])
            & (col("Length of Membership") <= lom[1]) & (col("Length of Membership") > lom[0])
        ).select(trunc(min(col('PREDICTED_SPEND'))), trunc(max(col('PREDICTED_SPEND')))).toPandas().iloc[0, ]

        st.write(f'This customer is likely to spend between ')
        st.metric(label="", value=f"${minspend}")
        #st.write("and")
        st.metric(label="and", value=f"${maxspend}")

        st.markdown("---")
        st.write("\nThe biggest drivers of customer spend are:")
        st.markdown('* **Length of Membership** \n * **Time on App**')
        st.write("You can see spend range change much more when one of these two variables is changed.")


# Create a multipage layout
def main():
    st.sidebar.title("Navigation")
    app_selection = st.sidebar.radio("Go to", ["Customer Sales Prediction", "Customer Spend Prediction Model", "SportsCo Ad Spend Optimizer"])

    if app_selection == "Customer Sales Prediction":
        app1()
    elif app_selection == "Customer Spend Prediction Model":
        app2()
    elif app_selection == "SportsCo Ad Spend Optimizer":
        app3()

if __name__ == "__main__":
    main()


