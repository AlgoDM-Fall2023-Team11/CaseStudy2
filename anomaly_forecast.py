import json
from snowflake.snowpark.session import Session
from snowflake.snowpark.functions import col
import snowflake.snowpark.dataframe
import snowflake.connector.pandas_tools as sfpd
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
import seaborn as sns

# Ensure that your credentials are stored in creds.json
with open('connection.json') as f:
    data = json.load(f)
    USERNAME = data['user']
    PASSWORD = data['password']
    SF_ACCOUNT = data['account']
  

CONNECTION_PARAMETERS = {
   "account": SF_ACCOUNT,
   "user": USERNAME,
   "password": PASSWORD,
   "database":"AD_FORECAST_DEMO",
   "schema": "demo"
}

session = Session.builder.configs(CONNECTION_PARAMETERS).create()

# session.sql("CREATE ROLE analyst").collect()


# session.sql('USE ROLE ACCOUNTADMIN').collect()

# session.sql("GRANT USAGE ON DATABASE AD_FORECAST_DEMO TO ROLE analyst").collect()

# session.sql("GRANT USAGE ON SCHEMA AD_FORECAST_DEMO.DEMO TO ROLE analyst").collect()

# session.sql("GRANT USAGE ON WAREHOUSE AD_FORECAST_DEMO_WH TO ROLE analyst").collect()

# session.sql("GRANT CREATE TABLE ON SCHEMA AD_FORECAST_DEMO.DEMO TO ROLE analyst").collect()

# session.sql("GRANT CREATE VIEW ON SCHEMA AD_FORECAST_DEMO.DEMO TO ROLE analyst").collect()

# session.sql("GRANT CREATE SNOWFLAKE.ML.FORECAST ON SCHEMA AD_FORECAST_DEMO.DEMO TO ROLE analyst").collect()

# session.sql("GRANT CREATE SNOWFLAKE.ML.ANOMALY_DETECTION ON SCHEMA AD_FORECAST_DEMO.DEMO TO ROLE analyst").collect()

# session.sql('CREATE DATABASE AD_FORECAST_DEMO').collect()

# session.sql('CREATE SCHEMA AD_FORECAST_DEMO.DEMO;').collect()

#session.sql(' CREATE OR REPLACE SNOWFLAKE.ML.FORECAST impressions_forecast(INPUT_DATA => SYSTEM$REFERENCE("TABLE", "daily_impressions"), TIMESTAMP_COLNAME => "day",TARGET_COLNAME =>"impression_count"   );').collect()
        
# session.sql('CREATE WAREHOUSE AD_FORECAST_DEMO_WH WITH WAREHOUSE_SIZE='XSmall'  ).collect()

def app_1():
    session.sql('USE WAREHOUSE AD_FORECAST_DEMO_WH').collect()

    session.sql('CALL impressions_forecast!FORECAST(FORECASTING_PERIODS => 14)').collect()


    forecast = '''
    SELECT day AS ts, impression_count AS actual, NULL AS forecast, NULL AS lower_bound, NULL AS upper_bound 
    FROM daily_impressions 
    UNION ALL 
    SELECT ts, NULL AS actual, forecast, lower_bound, upper_bound 
    FROM TABLE(RESULT_SCAN(-1))
    '''

    result = session.sql(forecast)
    # print(type(result))
    # print(result)
    # df=result

    # Convert it to a Pandas DataFrame

    pandas_dataframe = result.toPandas()
    df1=pandas_dataframe
    df = df1.tail(14).drop(columns=['ACTUAL'])
    st.header("Forecast predictions for the next 14 days")
    st.write(df)
    df=df1
    final_data = df1
    # Set the default Seaborn style
    sns.set(style="whitegrid")

    # Create a custom color palette
    custom_palette = sns.color_palette("Set3")

    # Create a custom Streamlit style



    # Function to create the time series graph
    def create_time_series_plot(data):
        df = data
        df['TS'] = pd.to_datetime(df['TS'])

        plt.figure(figsize=(12, 6))
        ax = sns.lineplot(x='TS', y='ACTUAL', data=df, label='Actual', color='blue')
        ax = sns.lineplot(x='TS', y='FORECAST', data=df, label='Forecast', color='red')


        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.title('Time Series Graph')
        plt.xticks(rotation=45)
        plt.legend()
        plt.grid(True)

        return plt

    # Streamlit app
    st.header("Time Series Data predicrion")

    # Display the plot in Streamlit
    st.pyplot(create_time_series_plot(final_data))


def app_2():
    #Analomy

    session.sql('USE WAREHOUSE AD_FORECAST_DEMO_WH').collect()
    st.write("Anomaly dectecting for  12000 impression")
    query = '''
    CALL impression_anomaly_detector!DETECT_ANOMALIES(
    INPUT_DATA => SYSTEM$QUERY_REFERENCE('select ''2022-12-06''::timestamp as day, 12000 as impressions'),
    TIMESTAMP_COLNAME =>'day',
    TARGET_COLNAME => 'impressions'
    );
    '''
    impression_anomaly_detector = session.sql(query).collect()

    st.write(impression_anomaly_detector)

    st.write("Anomaly dectecting for  120000 impression")

    query = '''
    CALL impression_anomaly_detector!DETECT_ANOMALIES(
    INPUT_DATA => SYSTEM$QUERY_REFERENCE('select ''2022-12-06''::timestamp as day, 120000 as impressions'),
    TIMESTAMP_COLNAME =>'day',
    TARGET_COLNAME => 'impressions'
    );
    '''
    impression_anomaly_detector = session.sql(query).collect()

    st.write(impression_anomaly_detector)

    st.write("Anomaly dectecting for  60000 impression")

    query = '''
    CALL impression_anomaly_detector!DETECT_ANOMALIES(
    INPUT_DATA => SYSTEM$QUERY_REFERENCE('select ''2022-12-06''::timestamp as day, 60000 as impressions'),
    TIMESTAMP_COLNAME =>'day',
    TARGET_COLNAME => 'impressions'
    );
    '''
    impression_anomaly_detector = session.sql(query).collect()

    st.write(impression_anomaly_detector)

def main():
    st.sidebar.title("Navigation")
    app_selection = st.sidebar.radio("Go to", ["Forecasting Prediction", "Anomaly Detection"])

    if app_selection == "Forecasting Prediction":
        app_1()
    elif app_selection == "Anomaly Detection":
        app_2()

if __name__ == "__main__":
    main()