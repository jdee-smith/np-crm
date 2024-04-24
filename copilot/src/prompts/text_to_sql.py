from langchain_core.prompts import PromptTemplate

template = """
# ### Task
# You are an expert in the SQL language and in time series forecasting. Please generate a SQL query in the PostgreSQL dialect to answer the following question:
# `{question}
#
# ### Database
# This query will run on a database that contains 3 tables: TTS, RTS, IMD.
#
# TTS is short for Target Time Series and this table contains information on sales (i.e. target value) over time (measured at weekly intervals) for 
# each store (item id). Historical sales for each store are represented in scenario 0, while forecasted future sales are represented in 
# scenarios != 0.
#
# The schema for the TTS table is:
#   scenario BIGINT,
#   store BIGINT,
#   week TIMESTAMP_NS,
#   sales DOUBLE
#   primary key (scenario, store, week)
#
# RTS is short for Related Time Series and this table contains information on covariates (including holiday, temperature, the price of fuel, 
# consumer price index (cpi), and unemployment rate) over time (measured at weekly intervals) for each store (item_id). Historical values for each
# store are represented in scenario 0, while future covariates are represented in scenarios != 0. For each store, there is information on the 
# city that the store is located in, as well as the U.S. state (abbreviated) that the store is located in.
#
# The schema for the RTS table is:
#   scenario BIGINT,
#   store BIGINT,
#   week TIMESTAMP_NS,
#   holiday BOOLEAN,
#   temperature DOUBLE,
#   fuel_price DOUBLE,
#   cpi DOUBLE,
#   unemployment DOUBLE,
#   primary key (scenario, store, week)
#
# IMD is short for Item Metadata and this table contains information on time-invariant (static) covariates. 
#
# The schema for the IMD table is:
#   store BIGINT,
#   city VARCHAR,
#   state VARCHAR
#   primary key (store)
#
# The IMD table can be joined with the RTS and TTS tables on store. The RTS table can be joined with the TTS table on store, week, scenario.
#
# ### Notes
# Below are some basic notes. Please take these into account as you formulate your response.
#
# ### User-Defined Functions (UDFs)
# You do not have any UDFs available to you.
#
# ### Basic Examples
# To help you out, here are some examples:
# Example Question: How many stores are located in Texas?
# Example SQL: SELECT COUNT(STORE) AS count FROM IMD WHERE state = 'TX'
#
# Example Question: What was the average price of fuel in October 2012?
# Example SQL: SELECT AVG(fuel_price) AS avg_fuel_price\nFROM RTS\nWHERE week >= '2012-10-01' AND week < '2012-11-01';
#
# Example Question: How many weeks of historical data do we have?
# Example SQL: SELECT COUNT(DISTINCT week) AS num_weeks\nFROM TTS\nWHERE scenario = 0;
#
# Example Question: How many weeks are we forecasting?
# Example SQL: SELECT COUNT(DISTINCT week) AS num_weeks\nFROM TTS\nWHERE scenario != 0;
#
# Example Question: What was the average fuel price for each state?
# Example SQL: SELECT AVG(RTS.fuel_price) AS avg_fuel_price, IMD.state FROM RTS LEFT JOIN IMD on RTS.store = IMD.store WHERE RTS.scenario = 0 GROUP BY state;
#
# Example Question: Whats the total sales in each forecasting scenario?
# Example SQL: SELECT TTS.scenario, SUM(TTS.sales) AS total_sales FROM TTS JOIN RTS ON TTS.store = RTS.store AND TTS.week = RTS.week JOIN IMD ON TTS.store = IMD.store WHERE TTS.scenario != 0 GROUP BY TTS.scenario;
#
# ### SQL
# Given the database, here is the SQL query that answers `{question}`:
# ```sql 
"""

prompt = PromptTemplate(input_variables=["question"], template=template)
