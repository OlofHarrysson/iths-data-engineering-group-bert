from datetime import datetime

from airflow.decorators import dag, task

from newsfeed import (
    download_blogs_from_rss,
    extract_articles,
    send_to_discord,
    summarize,
)


@task(task_id="download_blogs_from_rss_task")
def download_blogs_from_rss_task() -> None:
    download_blogs_from_rss.main("mit")
    download_blogs_from_rss.main("sd")
    download_blogs_from_rss.main("openai")


@task(task_id="extract_articles_task")
def extract_articles_task() -> None:
    extract_articles.main("mit")
    extract_articles.main("sd")
    extract_articles.main("openai")


@task(task_id="summarize_task")
def summarize_task() -> None:
    summarize.summarize_articles(summary_type="nontech", model_type="api")
    summarize.summarize_articles(summary_type="tech", model_type="api")

    summarize.summarize_articles(summary_type="sv_tech", model_type="api")
    summarize.summarize_articles(summary_type="sv_nontech", model_type="api")


@task(task_id="send_to_discord_task")
def send_to_discord_task() -> None:
    send_to_discord.main()


# Create the dag pipeline
@dag(
    dag_id="run_pipeline",
    start_date=datetime(2023, 6, 2),
    schedule_interval="0 1 * * *",  # This schedule runs at 1 AM every day
    catchup=False,
)
def test_pipeline() -> None:
    # Run the scripts in this order
    (
        download_blogs_from_rss_task()
        >> extract_articles_task()
        >> summarize_task()
        >> send_to_discord_task()
    )


test_pipeline()
