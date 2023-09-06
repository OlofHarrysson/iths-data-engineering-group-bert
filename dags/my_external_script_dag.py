from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import download_blogs_from_rss, extract_articles, summarize


@task(task_id="download_blogs_from_rss_task")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main("mit")
    download_blogs_from_rss.main("sd")
    # download_blogs_from_rss.main('openai')


@task(task_id="extract_articles_task")
def extract_articles_task() -> None:
    extract_articles.main("mit")
    extract_articles.main("sd")
    # extract_articles.main("openai")


@task(task_id="summarize_task")
def summarize_task() -> None:
    summarize.summarize_articles("nontech", "api")
    summarize.summarize_articles("tech", "api")


@dag(
    dag_id="download_blogs_from_rss_task",
    start_date=datetime(2023, 6, 2),
    schedule_interval=None,
    catchup=False,
)
def test_pipeline() -> None:
    download_blogs_from_rss_task() >> extract_articles_task() >> summarize_task()


test_pipeline()


# from airflow.models import DAG
# from airflow.operators.python_operator import PythonOperator
# from airflow.utils.dates import days_ago
# from newsfeed.my_external_script import hello


# args = {
#     'owner': 'airflow',
#     'start_date': days_ago(1) # make start date in the past
# }

# dag = DAG(
#     dag_id='crm-elastic-dag',
#     default_args=args,
#     schedule_interval=None # make this workflow happen every day
# )

# with dag:
#     hello_world = PythonOperator(
#         task_id='hello',
#         python_callable=hello,
#         # provide_context=True
#     )
