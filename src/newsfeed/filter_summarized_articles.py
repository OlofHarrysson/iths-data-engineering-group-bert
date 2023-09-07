from urllib.parse import urlparse


def sort_summaries(summaries):
    # sort summaries by published date in descending order (newest first)
    sorted_summaries = sorted(summaries, key=lambda x: x.published, reverse=True)

    return sorted_summaries


def get_source(summary):
    parsed_url = urlparse(summary.link)
    source = parsed_url.netloc  # netloc gives "https://example.com/something" -> "example.com"

    return source


def get_summary_by_source(summaries):
    summaries_dict = {}

    for summary in summaries:
        source = get_source(summary)

        if source not in summaries_dict:
            summaries_dict[source] = []

        summaries_dict[source].append(summary)

    return summaries_dict


def amount_summaries_from_each_source(summaries, n=10):
    top_summaries = []
    summaries_dict = get_summary_by_source(summaries)

    for source in summaries_dict:
        top_summaries.extend(summaries_dict[source][:n])

    return top_summaries
