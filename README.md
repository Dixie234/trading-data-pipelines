# trading-data-pipelines
Project created to test and analyse batch and streaming financial data, with some basic visual outputs.

To run this project you will need Docker installed on your machine. Once that is done, and you've cloned the repository, run this command to start the app:
`docker compose up --build`

This will start:
- Streamlit dashboard: `localhost:8501`
- pdAmin: `localhost:8080`
- dbt docs: `localhost:8081`

All components for this project are composed within docker-compose.yml - review this file for a full list of container images and their dependencies

In summary, here are the main components:
- A Postgres database which contains all the backing data for the application - running on port 5432
- A pdAdmin page to enable viewing and editing the Postgres instance - running on port 8080
- A dbt documentation page for viewing all of the models and their transformations, this is generated using run_docs.py - running on port 8081
- A Streamlit app displaying some live and static stock data pulled directly from the Postgres database - running on port 8501

Main entrypoint files for viewing the data are:
1. app.py - a Streamlit app which is hosted on localhost:8501 displaying a stocks dashboard of live cypto prices, and static US corporate data
2. stream_listener.py - a web socket responsible for getting live update data for crypto stocks and inserting them in the Postgres database

The contents of the Project folders are as follows:
./dbt - contains a dbt project for processing model transformations
./seed - contains script for fetching and inserting data from the finnhub and yfinance api's into the PostGres DB
./sql - contains all the base table models which are created when the Postgres instance is started

The project also contains 2 dockerfiles - one for managing the project as a whole, another for managing the production of the dbt docs
./seed also contains it's own dockerfile so that the commands can be executed as their own image which will depend on the Postgres instance spinning up, this way the data will always be inserted on container startup and ready to query

NOTE: The collection of sentiment data requires approximately 1000+ api requests to various news websites, all with retry logic, therefore initial container startup is slow.
