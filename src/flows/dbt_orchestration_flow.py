from prefect import Flow
from prefect.tasks.prefect import create_flow_run, wait_for_flow_run
from utils import config

# DBT Job Flow
from flows import dbt_job_flow

# Downstream Flows: To run after DBT Job completes
from flows import prereview_engagement_feature_store_flow
from flows import postreview_engagement_feature_store_flow

FLOW_NAME = "DBT Orchestration Flow"

with Flow(FLOW_NAME) as flow:

    dbt_job_flow_id = create_flow_run(flow_name=dbt_job_flow.FLOW_NAME, project_name=config.PREFECT_PROJECT_NAME)
    dbt_job_wait_task = wait_for_flow_run(dbt_job_flow_id, raise_final_state=True)

    prereview_flow_id = create_flow_run(flow_name=prereview_engagement_feature_store_flow.FLOW_NAME, project_name=config.PREFECT_PROJECT_NAME)
    prereview_wait_task = wait_for_flow_run(prereview_flow_id, raise_final_state=True)

    postreview_flow_id = create_flow_run(flow_name=postreview_engagement_feature_store_flow.FLOW_NAME, project_name=config.PREFECT_PROJECT_NAME)
    postreview_wait_task = wait_for_flow_run(postreview_flow_id, raise_final_state=True)

    prereview_flow_id.set_upstream(dbt_job_wait_task)
    postreview_flow_id.set_upstream(dbt_job_wait_task)

# for execution in development only
if __name__ == "__main__":
    # flow.visualize()
    flow.run()