# IE 7374: Algorithmic Digital Marketing: CASE STUDY 2 
# Snowpark for Python and Streamlit

Codelabs Link: https://codelabs-preview.appspot.com/?file_id=18NJN-UiLa7trpFAQhAThFkSs_s3izobcrK1eJwga4i4#0

* Krishna Barfiwala: 002771997

* Nakul Shiledar: 002738981

* Usashi Roy: 002752872


Snowpark brings deeply integrated, DataFrame-style programming to the languages developers like to use, and functions to help them build and deploy custom programs including machine learning models. And to bring predictive insights into actions, data scientists can build interactive applications that business stakeholders can use to interact with those models using Streamlit

Covers data ingestion, data science and creation of an app using Streamlit
How to use Snowpark for Python for doing Feature Engineering
Training a Machine Learning model outside of Snowflake and to deploy it as a Python UDF
Visualizing your working model in an end user app

# Environment Setup
### Python 3.9.18

### Create and Activate Conda Environment (OR, use any other Python environment with Python 3.9.18)
* conda create --name snowpark -c https://repo.anaconda.com/pkgs/snowflake python=3.9.18
* conda activate snowpark
  
### Install Snowpark for Python, Streamlit and other libraries in Conda environment
conda install -c https://repo.anaconda.com/pkgs/snowflake snowflake-snowpark-python pandas notebook scikit-learn cachetools streamlit

### Python library packages:
* scikit-learn (version 1.3.0)
* pandas
* numpy
* matplotlib
* seaborn
* streamlit
  
Update connection.json with your Snowflake account details and credentials
NOTE: For the account parameter, specify your account identifier and do not include the snowflakecomputing.com domain name. Snowflake automatically appends this when creating the connection.

# Part 1: Forecasting + Anomaly Detection

# Part 2: Multi Page App: Customer Growth Navigator

## Data Prerpration
* Customer Lifetime Value Computation: This demo utilizes the TPC DS sample dataset that is made available via Snowflake share. It can be configured to run on either the 10 TB
* Predict Customer Spend: Download the "EcommerceCustomers.csv" file from https://github.com/Snowflake-Labs/snowpark-python-demos/tree/main/Predict%20Customer%20Spend 
* ROI Prediction: Download the "campaign_spend.csv" and “mothly_revenue.csv” file from https://github.com/Snowflake-Labs/snowpark-python-demos/tree/main/Advertising-Spend-ROI-Prediction

## Overview
This is an all-in-one application powered by Snowpark Python, designed to address a range of critical business challenges across different industries. This versatile application is equipped to predict Customer Lifetime Value (CLV) for a fictitious corporation like 'TPC,' focusing on various sales channels, all while keeping sensitive data securely within the Snowflake ecosystem. By harnessing the Snowpark Python Dataframe API for feature engineering, employing stored procedures, utilizing Snowpark Optimized Warehouses for model training, and deploying batch User-Defined Functions (UDFs), this app offers an end-to-end solution for CLV analysis.

![WhatsApp Image 2023-10-21 at 10 06 14_5620cfeb](https://github.com/AlgoDM-Fall2023-Team11/CaseStudy2/assets/69983754/b95bf6ba-15d6-47db-a337-c37757043ab1)


But that's not all; this application extends its utility to e-commerce retailers striving to comprehend user interactions with their digital platforms, specifically their website and mobile app. With the aim of enhancing user experience and ultimately increasing consumer spending, it aids in data-driven decision-making to determine the ideal allocation of resources between these platforms.

![WhatsApp Image 2023-10-21 at 10 08 39_bedc9f2d](https://github.com/AlgoDM-Fall2023-Team11/CaseStudy2/assets/69983754/88a11374-334a-4708-802f-59fb14170b33)

Furthermore, this same application serves as a valuable resource for businesses across diverse sectors looking to predict and optimize Return On Investment (ROI) from a multitude of advertising channels. Whether in e-commerce, finance, healthcare, or beyond, this application offers a flexible solution for data-driven marketing strategy improvement and efficient resource allocation. In essence, it's a comprehensive tool that empowers businesses to make informed decisions, enhance marketing campaigns, and achieve improved outcomes across a wide range of industries

![WhatsApp Image 2023-10-21 at 10 11 30_c1b4a7a4](https://github.com/AlgoDM-Fall2023-Team11/CaseStudy2/assets/69983754/ca1e6ad2-7693-498e-b9e1-2b17407157f2)
![WhatsApp Image 2023-10-21 at 10 12 00_e7af9cc4](https://github.com/AlgoDM-Fall2023-Team11/CaseStudy2/assets/69983754/b5e9f676-fadf-4353-8f31-269fdfddec72)
