import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv("Data.csv")  # put your CSV in the same folder

st.set_page_config(
    page_title="Beer Market Insights",
    layout='wide'
)

def load_data():
    df = pd.read_csv('Data.csv')

    df = df.drop(columns=['review_profilename', 'beer_beerid', 'brewery_id'], errors='ignore')

    df['review_date'] = pd.to_datetime(df['review_time'], unit='s', errors='coerce')
    df['review_year_month'] = df['review_date'].dt.to_period('M').astype(str)

    df = df.dropna(subset=['review_overall'])

    with st.sidebar:
        
        st.markdown('Filters')
        st.markdown('Please use the follwing filters to change your results and explore the market')
        st.divider()

        all_styles = sorted(df['beer_style'].dropna().unique().tolist())
        selected_style = st.selectbox(
            "Beer Style",
            options=['All Styles'] + all_styles,
            index = 0,
        )

        st.selectbox(
            "Location",
            options=['All Locations - we need the details here'],
            disabled=True,
        )

        st.divider()
        st.markdown('**Minimum Rating Points**')
        st.caption('Slide the below qualities to set the minimum of each attribute you would like')

        min_aroma = st.slider(
            'Aroma',
            min_value=float(df['review_aroma'].min()),
            max_value=float(df['review_aroma'].max()),
            value=float(df['review_aroma'].min()),
            step=0.5,
        )

        min_appearance = st.slider(
            'Appearance',
            min_value=float(df['review_appearance'].min()),
            max_value=float(df['review_appearance'].max()),
            value=float(df['review_appearance'].min()),
            step=0.5,
        )

        min_palate = st.slider(
            'Palate',
            min_value=float(df['review_palate'].min()),
            max_value=float(df['review_palate'].max()),
            value=float(df['review_palate'].min()),
            step=0.5,
        )

        min_taste = st.slider(
            'Taste',
            min_value=float(df['review_taste'].min()),
            max_value=float(df['review_taste'].max()),
            value=float(df['review_taste'].min()),
            step=0.5,
        )

        abv_min_val = float(df['beer_abv'].min())
        abv_max_val = float(df['beer_abv'].max())

        st.divider()
        st.markdown('**Alcohol ABV Range**')
        st.caption('Slide a range below to select how alcoholic you like your beer')

        abv_range = st.slider(
            "Alcohol by Volume (%)",
            min_value=abv_min_val,
            max_value=abv_max_val,
            value=(abv_min_val, abv_max_val),
            step=1.0
        )

    return df

df = load_data()


