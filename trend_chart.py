import pandas as pd
import plotly.express as px
import streamlit as st


def render_trend_chart(df: pd.DataFrame, selected_style: str):
    """
    Generate a line chart showing the number of reviews over time
    for the selected beer style.

    Parameters:
        df: the dataframe 
        selected_style : the beer style chosen in the sidebar
    """

    st.subheader('Selected Beer Style Trend Over Time')

    # Filter by selected style
    if selected_style == "All Styles":
        # Show a placeholder empty chart with a prompt message
        fig = px.line(
            title=" ",
            labels={
                "review_year_month": "Time",
                "review_count": "Number of Reviews",
            },
        )

        fig.update_layout(
            title_font_size=10,
            title_font_color="#888888",
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            height=250,
            margin=dict(t=50, b=20, l=20, r=20),
        )

        fig.add_annotation(
            text="Choose a beer style from the sidebar",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False,
            font=dict(size=14, color="#aaaaaa"),
        )

        st.plotly_chart(fig, use_container_width=True)
        return

    else:
        filtered = df[df["beer_style"] == selected_style].copy()
        chart_title = f"{selected_style} — Monthly Review Count"

    if filtered.empty:
        st.warning("No review data found for the selected beer style.")
        return

    # Aggregate by month
    trend = (
        filtered.groupby("review_year_month")
        .size()
        .reset_index(name="review_count")
    )

    # Convert back to datetime for proper axis ordering
    trend["review_year_month"] = pd.to_datetime(trend["review_year_month"])
    trend = trend.sort_values("review_year_month")

    # Build the line chart
    fig = px.line(
        trend,
        x="review_year_month",
        y="review_count",
        title=chart_title,
        labels={
            "review_year_month": "Month",
            "review_count": "Number of Reviews",
        },
        markers=True,
    )

    fig.update_traces(
        line=dict(color="#F5A623", width=2),
        marker=dict(size=4, color="#F5A623"),
    )

    fig.update_layout(
        title_font_size=16,
        xaxis_title="Time",
        yaxis_title="Number of Reviews",
        hovermode="x unified",
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(showgrid=True, gridcolor="#e0e0e0"),
        yaxis=dict(showgrid=True, gridcolor="#e0e0e0"),
        height=250,
        margin=dict(t=50, b=40, l=40, r=20),
    )

    st.plotly_chart(fig, use_container_width=True)