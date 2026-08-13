import streamlit as st
import plotly.express as px

def show_risk_distribution(df):

    # Count users in each risk band
    chart_data = (
        df.groupby("risk_band")
          .size()
          .reset_index(name="Users")
    )

    fig = px.pie(
        chart_data,
        names="risk_band",
        values="Users",
        title="Risk Score Distribution",
        hole=0.45
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)