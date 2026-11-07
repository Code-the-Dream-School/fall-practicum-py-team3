from pipeline.transform.transform import aqi_category


def make_template_insight(record):
    """Build the fallback sentence when the LLM can't give us a usable one."""
    # the day's average can be 2.5, but aqi_category only knows 1 through 5,
    # so round it to the nearest whole level first
    category = aqi_category(round(record["aqi_24h_avg"]))

    return (
        f"{record['city']}'s air quality on {record['timestamp']} was {category}, "
        f"with a 24-hour average AQI of {record['aqi_24h_avg']}."
    )

