import streamlit as st
import plotly.express as px

def show_risk_distribution(df):

    # Count users in each risk band
    chart_data = (
        df.groupby("risk_band")
          .size()
          .reset_index(name="Users")
    )

    colors = {
        "Normal": "#22C55E",       # green — good/healthy
        "Suspicious": "#6366F1",   # indigo — worth a look
        "High Risk": "#F97316",    # orange — elevated concern
        "Critical": "#DC2626"      # red — urgent
    }

    fig = px.pie(
        chart_data,
        names="risk_band",
        values="Users",
        title="Risk Score Distribution",
        hole=0.45,
        color="risk_band",
        color_discrete_map=colors,
        category_orders={"risk_band": ["Normal", "Suspicious", "High Risk", "Critical"]}
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    st.plotly_chart(fig, use_container_width=True)