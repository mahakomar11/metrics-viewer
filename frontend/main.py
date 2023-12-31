import os

import pandas as pd
import requests
import streamlit as st

base_url = os.getenv("API_URL")

if not base_url:
    from dotenv import load_dotenv

    load_dotenv(".env-dev")
    base_url = f'http://localhost:{os.getenv("API_PORT")}{os.getenv("API_PREFIX")}'

aggregation_url = f"{base_url}/aggregation"

HEADERS = {"Api-Key": os.getenv("API_KEY")}

TIME_PERIODS_MAP = {
    "10 minutes": "P0DT10M",
    "30 minutes": "P0DT30M",
    "1 hour": "P0DT1H",
    "5 hours": "P0DT5H",
    "1 day": "P1D",
    "5 days": "P5D",
    "1 month": "P1M",
}


def get_event_types() -> list[str]:
    res = requests.get(f"{base_url}/event-types", headers=HEADERS)
    res.raise_for_status()
    return res.json()["event_types"]


def get_aggregation_by_time(event_type: str, interval: str) -> pd.DataFrame:
    res = requests.get(
        f"{aggregation_url}/time",
        params={"event_type": event_type, "interval": interval},
        headers=HEADERS,
    )
    res.raise_for_status()
    data = res.json()
    df = pd.DataFrame(data["data"])
    df["reg_interval"] = pd.to_datetime(df["reg_interval"])
    return df.set_index("reg_interval")


def get_aggregation_by_dma(event_type: str) -> pd.DataFrame:
    res = requests.get(
        f"{aggregation_url}/dma", params={"event_type": event_type}, headers=HEADERS
    )
    res.raise_for_status()
    data = res.json()
    return pd.DataFrame(data["data"]).set_index("mm_dma")


def get_aggregation_by_site(event_type: str) -> pd.DataFrame:
    res = requests.get(
        f"{aggregation_url}/site", params={"event_type": event_type}, headers=HEADERS
    )
    res.raise_for_status()
    data = res.json()
    return pd.DataFrame(data["data"]).set_index("site_id")


st.set_page_config("Metrics")

event_types = get_event_types()

st.markdown("# Analytics of CTR and EvPM")

st.markdown("## Changing by time")
event_type_time = st.selectbox("Choose event type: ", event_types, key="reg_time")
time_period = st.select_slider(
    "Choose time period: ", options=TIME_PERIODS_MAP.keys(), value="1 day", key="period"
)

aggregation_by_time = get_aggregation_by_time(
    event_type_time, TIME_PERIODS_MAP[time_period]
)
st.write(aggregation_by_time)
st.line_chart(aggregation_by_time[["ctr", "evpm"]])

st.markdown("## Aggregation by DMA")
event_type_dma = st.selectbox("Choose event type: ", event_types, key="mm_dma")
st.write(get_aggregation_by_dma(event_type_dma))

st.markdown("## Aggregation by site")
event_type_site_id = st.selectbox("Choose event type: ", event_types, key="site_id")
st.write(get_aggregation_by_site(event_type_site_id))
