import copy
import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _streamlit_datagrid = components.declare_component(
        "streamlit_datagrid",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _streamlit_datagrid = components.declare_component("streamlit_datagrid", path=build_dir)


def is_out(label, th, value):
    if label in th:
        thresh = th[label]["value"]
        side = th[label]["side"]
        if side == "<":
            return 1 if value < thresh else 0
        elif side == "<=":
            return 1 if value <= thresh else 0
        elif side == ">":
            return 1 if value > thresh else 0
        elif side == ">=":
            return 1 if value >= thresh else 0
        elif side == "=":
            return 1 if value == thresh else 0
    else:
        return 0


def streamlit_datagrid(df, th, headers=[], label="label", measure="measure", height=400, key=None):
    processed_df = copy.deepcopy(df)
    if headers == []:
        headers = processed_df.columns
    processed_df["out"] = processed_df.apply(lambda row: is_out(row[label], th, row[measure]), axis=1)
    streamlit_datagrid_value = _streamlit_datagrid(processed_df=processed_df, headers=headers, height=height, key=key)
    return streamlit_datagrid_value


if not _RELEASE:
    import streamlit as st
    import numpy as np
    import pandas as pd
    from datetime import datetime
    import streamlit_lchart_card as stgc

    st.set_page_config(layout="wide")

    t = [datetime(2023, 1, i, j, 0, 0) for i in range(1, 3) for j in range(0, 24, 3)]

    nb_samples = len(t)
    label_temp = "Température"
    unit_temp = "°C"
    label_pH = "pH"
    unit_pH = ""
    label_nitrate = "Nitrate"
    unit_nitrate = "mg/L"
    label_ammonia = "Ammoniaque"
    unit_ammonia = "mg/L"
    label_water_level = "Niveau d'eau"
    unit_water_level = ""

    m_temp = 20.4
    m_pH = 6.79
    m_nitrate = 100.3
    m_ammonia = 2.9

    th_temp = {"value": 19.5, "side": "<"}
    th_pH = {"value": 6, "side": "<"}
    th_nitrate = {"value": 93.6, "side": ">"}
    th_ammonia = {"value": 2.99, "side": ">"}
    th_water_level = {"value": 1, "side": "="}
    th = {
        f"{label_temp}": th_temp,
        f"{label_pH}": th_pH,
        f"{label_nitrate}": th_nitrate,
        f"{label_ammonia}": th_ammonia,
        f"{label_water_level}": th_water_level
    }

    temps = [round(m, 1) for m in np.random.normal(m_temp, 2, nb_samples)]
    pHs = [round(m, 2) for m in np.random.normal(m_pH, 1, nb_samples)]
    nitrates = [round(m, 2) for m in np.random.normal(m_nitrate, 20, nb_samples)]
    ammonias = [round(m, 2) for m in np.random.normal(m_ammonia, 0.1, nb_samples)]
    water_levels = [float(m) for m in np.random.binomial(1, 0.1, nb_samples)]

    df_temps = pd.DataFrame({"label": [label_temp] * len(t), "date": t, "measure": temps, "unit": [unit_temp] * len(t)})
    df_pHs = pd.DataFrame({"label": [label_pH] * len(t), "date": t, "measure": pHs, "unit": [unit_pH] * len(t)})
    df_nitrates = pd.DataFrame(
        {"label": [label_nitrate] * len(t), "date": t, "measure": nitrates, "unit": [unit_nitrate] * len(t)})
    df_ammonias = pd.DataFrame(
        {"label": [label_ammonia] * len(t), "date": t, "measure": ammonias, "unit": [unit_ammonia] * len(t)})
    df_water_levels = pd.DataFrame({"label": [label_water_level] * len(t), "date": t, "measure": water_levels,
                                    "unit": [unit_water_level] * len(t)})

    multiple_graphs = st.columns(4)
    with multiple_graphs[0]:
        stgc.streamlit_lchart_card(title="Température", df=df_temps, x="date", y="measure",
                                   labels={"measure": "°C", "date": "Date"}, defaultColor="rgb(255, 180, 15)",
                                   thresh=th[label_temp]["value"],
                                   threshColor="rgb(255, 90, 132)", rounding=1, format="%d/%m %Hh",
                                   key="streamlit_temp_graphic_card")
    with multiple_graphs[1]:
        stgc.streamlit_lchart_card(title="Nitrate", df=df_nitrates, x="date", y="measure",
                                   labels={"measure": "mg/L", "date": "Date"}, defaultColor="rgb(132, 99, 255)",
                                   thresh=th[label_nitrate]["value"],
                                   rounding=2, key="streamlit_nitrate_graphic_card")
    with multiple_graphs[2]:
        stgc.streamlit_lchart_card(title="pH", df=df_pHs, x="date", y="measure",
                                   labels={"measure": "", "date": "Date"}, defaultColor="rgb(99, 255, 132)", thresh=th[label_pH]["value"],
                                   rounding=2, key="streamlit_pH_graphic_card")
    with multiple_graphs[3]:
        stgc.streamlit_lchart_card(title="Ammoniaque", df=df_ammonias, x="date", y="measure",
                                   labels={"measure": "mg/L", "date": "Date"}, defaultColor="rgb(90, 90, 90)",
                                   thresh=th[label_ammonia]["value"],
                                   rounding=2, key="streamlit_ammonia_graphic_card")

    df = pd.concat([df_temps, df_pHs, df_nitrates, df_ammonias, df_water_levels], ignore_index=True)
    streamlit_datagrid(df=df, th=th, headers=["Mesure", "Date", "Valeur", "Unité"], label="label", measure="measure", height=370, key="test")
