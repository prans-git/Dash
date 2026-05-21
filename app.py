import streamlit as st
import pandas as pd

df = pd.read_csv("Data.csv")  # put your CSV in the same folder

st.title("Our Dashboard")
st.dataframe(df)
