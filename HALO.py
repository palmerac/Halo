import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


st.set_page_config(layout="wide")

st.sidebar.markdown(
    """
---
Created with ❤️ by [Aaron Palmer](https://github.com/palmerac/).
"""
)

st.title("Halo Infinite Dashboard")
st.markdown("\n  ")
st.text("This is a dashboard for my Halo Infinite ranked games.")
st.text("It has a bunch of graphs and statistics.")
st.markdown("\n  ")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "Raw Data",
        "Boxplots",
        "Distance Histogram",
        "Avg HR Histogram",
        "Cumulative Distance",
        "Raw File",
    ]
)

with tab1:
    st.dataframe(df)
    pass

with tab2:
    st.
