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

    numeric_cols = ['review_overall', 'review_aroma', 'review_appearance',
                    'review_palate', 'review_taste', 'beer_abv']
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    df = df.dropna(subset=['review_overall'])
    return df

df = load_data()

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
    abv_low, abv_high = abv_range

filtered = df.copy()

if selected_style != 'All Styles':
    filtered = filtered[filtered['beer_style'] == selected_style]


filtered = filtered[
    (filtered['review_aroma']  >= min_aroma) &
    (filtered['review_appearance']  >= min_appearance) &
    (filtered['review_palate']  >= min_palate) &
    (filtered['review_taste']  >= min_taste) &
    (filtered['beer_abv']  >= abv_min_val) &
    (filtered['beer_abv']  <= abv_max_val)
]

if filtered.empty:
    st.warning("⚠️ No reviews match your current filters. Try loosening the sliders.")
    st.stop() 

st.header('**Beer Market Analysis - Production and Marketing**')
st.markdown(
    f'Currently Showing **{len(filtered):,}** reviews'
    + (f' for {selected_style}' if selected_style != 'All Styles' else ' accross **all styles**')
    + ' matching your filter'
)

st.divider()

k1, k2, k3, k4 = st.columns(4)
k1.metric('Total Reviews', f'{len(filtered):,}')
k2.metric('Average Overall Score', f'{filtered['review_overall'].mean():.2f}')
k3.metric('Unique Beers', f'{filtered['beer_name'].nunique():.,}')
k4.metric('Unique Breweries', f'{filtered['brewery_name'].nunique():,}')

st.divider()

st.subheader('Ascpect Importance in selected Beer Style and Location')
aspect_means = {
    'Aroma': filtered['review_aroma'].mean(),
    'Appearance': filtered['review_appearance'].mean(),
    'Palate': filtered['review_palate'].mean(),
    'Taste': filtered['review_taste'].mean(),
}

aspect_df = pd.DataFrame(
    list(aspect_means.items()),
    columns=['Aspect', 'Average Score']
).sort_values('Average Score', ascending=False)

fig1 = px.bar(
    aspect_df,
    y='Aspect',
    x='Average Score',
    orientation='h',
    text_auto='.2f',
    color='Average Score',
    color_continuous_scale='Oranges',
)

fig1.update_traces(textposition='outside')
fig1.update_layout(
    xaxis_range=[0, 5.5],
    coloraxis_showscale=False,
    yaxis_title='Average Score',
    xaxis_title='',
)
st.plotly_chart(fig1, width='content')