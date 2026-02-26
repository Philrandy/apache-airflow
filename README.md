# 🚀 Airflow AWS Glue → Redshift Pipeline

This project demonstrates how to orchestrate an AWS Glue job using
Apache Airflow.\
The DAG triggers a Glue job, retrieves its `run_id`, and monitors its
execution until completion using a sensor.

------------------------------------------------------------------------

## 📌 Project Overview

This Airflow pipeline:

1.  Triggers an AWS Glue job
2.  Retrieves the latest Glue job run ID
3.  Waits for the Glue job to finish
4.  Runs on a weekly schedule

It is designed for data transfer workflows such as:

-   **S3 → Redshift**
-   ETL processing using AWS Glue
-   Automated cloud data pipelines

------------------------------------------------------------------------

## 🏗️ Architecture

Airflow DAG\
⬇\
AWS Glue Job\
⬇\
Amazon S3\
⬇\
Amazon Redshift

------------------------------------------------------------------------

## ⚙️ Technologies Used

-   Apache Airflow
-   AWS Glue
-   Amazon S3
-   Amazon Redshift
-   Boto3
-   Python 3.x

------------------------------------------------------------------------

## 📂 DAG Structure

The pipeline contains three main tasks:

### 1️⃣ Trigger Glue Job

Uses a PythonOperator to start the Glue job.

### 2️⃣ Fetch Glue Run ID

Retrieves the most recent Glue job run ID using Boto3.

### 3️⃣ Monitor Glue Job

Uses `GlueJobSensor` to wait until the Glue job completes.

------------------------------------------------------------------------

## 🧠 Key Features

-   Clean modular AWS client handling
-   Uses Airflow XCom to pass run_id between tasks
-   Retry logic enabled
-   Weekly schedule
-   Sensor-based job monitoring
-   Production-ready structure

------------------------------------------------------------------------

## 🛠️ Configuration

Make sure you configure the following in Airflow:

### AWS Connection

Create an Airflow connection:

    Conn Id: aws_s3_conn
    Conn Type: Amazon Web Services

Ensure it has permissions for: - glue:StartJobRun - glue:GetJobRuns -
glue:GetJobRun

------------------------------------------------------------------------

## 🗓️ Scheduling

    schedule_interval='@weekly'

Catchup is disabled:

    catchup=False

------------------------------------------------------------------------

## 📊 Use Case

This project is ideal for:

-   Cloud Data Engineering portfolios
-   Demonstrating Airflow orchestration skills
-   AWS Glue automation examples
-   Redshift data loading pipelines

------------------------------------------------------------------------

## 🚀 How to Use

1.  Place the DAG file in your Airflow `dags/` directory.
2.  Ensure AWS credentials are configured.
3.  Enable the DAG in Airflow UI.
4.  Trigger manually or wait for scheduled run.

------------------------------------------------------------------------

## 📈 Portfolio Value

This project demonstrates:

-   Cloud orchestration
-   AWS service integration
-   Production-level Airflow DAG structuring
-   Data pipeline monitoring patterns

------------------------------------------------------------------------

## 📄 License

MIT License

------------------------------------------------------------------------

### 👨🏽‍💻 Author

Dagogo Orifama\
Data Scientist \| ML Engineer \| Cloud Data Engineer
