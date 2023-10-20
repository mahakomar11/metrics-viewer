from typing import Literal

import pandas as pd
import streamlit as st

TIME_PERIODS_MAP = {
    "10 minutes": "10T",
    "30 minutes": "30T",
    "1 hour": "H",
    "5 hours": "5H",
    "1 day": "D",
    "5 days": "5D",
    "1 month": "M",
}


@st.cache_data
def get_joined_impressions() -> pd.DataFrame:
    print("Load and join tables")
    impression_log = pd.read_csv("raw_data/interview.X.csv").set_index("uid")
    events_log = pd.read_csv("raw_data/interview.y.csv").set_index("uid")
    return impression_log.join(events_log)


@st.cache_data
def get_event_types(impressions_with_tags: pd.DataFrame) -> list[str]:
    print("Load event types")
    unique_tags = impressions_with_tags["tag"].unique()
    return [
        tag for tag in unique_tags if not pd.isna(tag) and not str(tag).startswith("v")
    ]


@st.cache_data
def get_aggregation(
    df: pd.DataFrame,
    event_type: str,
    by_field: Literal["site_id", "mm_dma", "reg_time"] = "site_id",
    time_period: str | None = None,
) -> pd.DataFrame:
    print(
        f"Calculate aggregation by field {by_field} and event_type={event_type} and time_period={time_period}"
    )
    if by_field == "reg_time":
        df["reg_time"] = pd.to_datetime(df["reg_time"])
        grouped = df.groupby(pd.Grouper(key="reg_time", freq=time_period))
    else:
        grouped = df.groupby(by_field)

    count_df = grouped.size().reset_index(name="impressions count")
    count_events_df = (
        grouped["tag"]
        .apply(lambda x: x[x.isin([event_type, f"v{event_type}"])].count())
        .rename("event count")
    )
    count_clicks_df = (
        grouped["tag"].apply(lambda x: x[x == event_type].count()).rename("click count")
    )

    new_df = pd.merge(count_df, count_clicks_df, on=by_field)
    new_df = pd.merge(new_df, count_events_df, on=by_field)

    new_df["CTR"] = round(100 * new_df["click count"] / new_df["impressions count"], 2)
    new_df["EvPM"] = round(100 * new_df["event count"] / new_df["impressions count"], 2)

    return new_df.set_index(by_field)


st.markdown("# Analytics of CTR and EvPM")

impressions_with_tags = get_joined_impressions()
event_types = get_event_types(impressions_with_tags)

st.markdown("## Changing by time")
event_type_time = st.selectbox("Choose event type: ", event_types, key="reg_time")
time_period = st.select_slider(
    "Choose time period: ", options=TIME_PERIODS_MAP.keys(), value="1 day", key="period"
)

aggregation_by_time = get_aggregation(
    impressions_with_tags,
    event_type_time,
    by_field="reg_time",
    time_period=TIME_PERIODS_MAP[time_period],
)
st.write(aggregation_by_time)
st.line_chart(aggregation_by_time[["CTR", "EvPM"]])

st.markdown("## Aggregation by DMA")
event_type_dma = st.selectbox("Choose event type: ", event_types, key="mm_dma")
st.write(get_aggregation(impressions_with_tags, event_type_dma, by_field="mm_dma"))

st.markdown("## Aggregation by site")
event_type_site_id = st.selectbox("Choose event type: ", event_types, key="site_id")
st.write(get_aggregation(impressions_with_tags, event_type_site_id, by_field="site_id"))
