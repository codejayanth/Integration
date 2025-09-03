# Apache Airflow
I am using the Apache Airflow for building the ETL pipelines.
## Setting up the virtual environment and ensure to have python version lesson than 3.13. 
1. brew install python@3.12
2. brew info python@3.12
3. There will be path looks like: **/opt/homebrew/bin/python3.12**
4. Take the above path and create the virtual env: **/opt/homebrew/bin/python3.12 -m venv airflow_venv**
5. Activate the virtual environment: **source airflow_venv/bin/activate**

## Installing the airflow
### Make sure the docker is installed and open
1. Run this from the root of your directory - **curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.0.6/docker-compose.yaml'**
2. **mkdir -p ./dags ./logs ./plugins ./config**
3. **echo -e "AIRFLOW_UID=$(id -u)" > .env**
4. **AIRFLOW_UID=50000**
5. **docker compose up airflow-init**
6. **docker compose up**
7. **docker compose down**
