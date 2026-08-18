import streamlit as st
import plotly.graph_objects as go

from components.badges import BAND_COLORS

BAND_ORDER = ["Critical", "High Risk", "Suspicious", "Normal"]


def show_risk_distribution(df):
    counts = df["risk_band"].value_counts()
    total = int(counts.sum())

    labels = [b for b in BAND_ORDER if b in counts.index]
    values = [int(counts[b]) for b in labels]
    colors = [BAND_COLORS[b] for b in labels]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.62,
                marker=dict(colors=colors),
                textinfo="none",
                sort=False,
                hovertemplate="%{label}: %{value} users (%{percent})<extra></extra>",
            )
        ]
    )
    fig.update_layout(
        showlegend=False,
        margin=dict(t=10, b=10, l=10, r=10),
        height=260,
        annotations=[
            dict(
                text=f"<b>{total:,}</b><br><span style='font-size:12px'>Users</span>",
                x=0.5, y=0.5, showarrow=False, font=dict(size=22),
            )
        ],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )

    chart_col, legend_col = st.columns([1.3, 1])

    with chart_col:
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with legend_col:
        st.markdown('<div style="margin-top:24px;">', unsafe_allow_html=True)
        for band, value, color in zip(labels, values, colors):
            pct = (value / total * 100) if total else 0
            st.markdown(
                f"""
                <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;">
                  <div style="display:flex;align-items:center;gap:8px;">
                    <span style="width:12px;height:12px;border-radius:3px;background:{color};display:inline-block;"></span>
                    <span style="font-size:0.85rem;color:var(--text-color);">{band} ({pct:.0f}%)</span>
                  </div>
                  <span style="font-size:0.85rem;font-weight:700;color:var(--text-color);">{value:,}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)

    st.caption("Distribution of users by risk score bands")
