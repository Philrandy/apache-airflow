
from __future__ import annotations

import time
from datetime import datetime, timedelta
from typing import Any

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsGenericHook
from airflow.providers.amazon.aws.sensors.glue import GlueJobSensor


AWS_CONN_ID = "aws_s3_conn"
GLUE_REGION = "us-west-2"
GLUE_JOB_NAME = "s3_upload_to_redshift_gluejob"


def _glue_client(aws_conn_id: str = AWS_CONN_ID, region_name: str = GLUE_REGION):
    """Create a boto3 Glue client using Airflow's AWS connection."""
    hook = AwsGenericHook(aws_conn_id=aws_conn_id)
    boto3_session = hook.get_session(region_name=region_name)
    return boto3_session.client("glue")


def trigger_glue_job(job_name: str, aws_conn_id: str = AWS_CONN_ID, region_name: str = GLUE_REGION, **_: Any) -> None:
    """Trigger an AWS Glue job run."""
    client = _glue_client(aws_conn_id=aws_conn_id, region_name=region_name)
    client.start_job_run(JobName=job_name)


def fetch_latest_glue_run_id(
    job_name: str,
    aws_conn_id: str = AWS_CONN_ID,
    region_name: str = GLUE_REGION,
    delay_seconds: int = 8,
    **_: Any,
) -> str:
    """
    Wait briefly, then fetch the most recent Glue job run_id.
    Returns the run_id (stored in XCom automatically by PythonOperator).
    """
    time.sleep(delay_seconds)

    client = _glue_client(aws_conn_id=aws_conn_id, region_name=region_name)
    resp = client.get_job_runs(JobName=job_name)

    # Same behavior as your original: take the newest run in JobRuns[0]
    return resp["JobRuns"][0]["Id"]


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2023, 8, 1),
    "email": ["myemail@domain.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(seconds=15),
}

with DAG(
    dag_id="my_dag",
    default_args=default_args,
    schedule_interval="@weekly",
    catchup=False,
    tags=["aws", "glue", "redshift", "s3"],
) as dag:

    glue_job_trigger = PythonOperator(
        task_id="tsk_glue_job_trigger",
        python_callable=trigger_glue_job,
        op_kwargs={"job_name": GLUE_JOB_NAME},
    )

    grab_glue_job_run_id = PythonOperator(
        task_id="tsk_grab_glue_job_run_id",
        python_callable=fetch_latest_glue_run_id,
        op_kwargs={"job_name": GLUE_JOB_NAME},
    )

    is_glue_job_finish_running = GlueJobSensor(
        task_id="tsk_is_glue_job_finish_running",
        job_name=GLUE_JOB_NAME,
        run_id='{{ ti.xcom_pull(task_ids="tsk_grab_glue_job_run_id") }}',
        verbose=True,  # prints Glue job logs in Airflow logs
        aws_conn_id=AWS_CONN_ID,
        poke_interval=60,
        timeout=3600,
    )

    glue_job_trigger >> grab_glue_job_run_id >> is_glue_job_finish_running
```
