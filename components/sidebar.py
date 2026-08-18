import os
import datetime
import streamlit as st
from database.db import load_sidebar_summary


def show_sidebar() -> None:
    """Render the AnomAlert Quick Summary sidebar, matching LFD.png styling."""
    with st.sidebar:
        # ── Injected Responsive Styles ──
        st.markdown(
            """
            <style>
              /* Card container: stands out by using page background on top of sidebar background */
              .metric-card {
                display: flex;
                align-items: center;
                background-color: var(--background-color);
                border: 1px solid rgba(128, 128, 128, 0.12);
                border-radius: 12px;
                padding: 14px 16px;
                margin-bottom: 12px;
                font-family: var(--font);
                box-shadow: 0 1px 3px rgba(0,0,0,0.02);
              }
              /* Icon container: rounded square container using sidebar background */
              .metric-icon-container {
                display: flex;
                align-items: center;
                justify-content: center;
                width: 44px;
                height: 44px;
                background-color: rgba(128, 128, 128, 0.08);
                border-radius: 10px;
                color: var(--text-color);
                flex-shrink: 0;
              }
              .metric-info {
                margin-left: 16px;
                display: flex;
                flex-direction: column;
              }
              .metric-label {
                font-size: 0.85rem;
                color: var(--secondary-text-color);
                font-weight: 500;
                margin: 0;
                line-height: 1.2;
              }
              .metric-value {
                font-size: 1.3rem;
                color: var(--text-color);
                font-weight: 700;
                margin: 5px 0 0 0;
                line-height: 1.2;
              }
              /* Centered header logo & typography */
              .sidebar-header-container {
                display: flex;
                flex-direction: column;
                align-items: center;
                text-align: center;
                font-family: var(--font);
                padding-top: 15px;
              }
              .sidebar-title {
                font-size: 2.2rem;
                font-weight: 700;
                color: var(--text-color);
                margin-top: 10px;
                line-height: 1.1;
              }
              .sidebar-subtitle {
                font-size: 0.9rem;
                color: var(--secondary-text-color);
                line-height: 1.4;
                margin-top: 10px;
                max-width: 90%;
              }
              
              /* Custom circular secondary button in the sidebar */
              .stSidebar button[kind="secondary"] {
                border-radius: 50% !important;
                width: 36px !important;
                height: 36px !important;
                min-width: 36px !important;
                max-width: 36px !important;
                display: inline-flex !important;
                align-items: center !important;
                justify-content: center !important;
                padding: 0 !important;
                font-size: 1.2rem !important;
                border: 1px solid rgba(128, 128, 128, 0.3) !important;
                background-color: transparent !important;
                color: var(--text-color) !important;
                box-shadow: none !important;
              }
              .stSidebar button[kind="secondary"]:hover {
                border-color: var(--primary-color) !important;
                color: var(--primary-color) !important;
                background-color: rgba(128, 128, 128, 0.05) !important;
              }
            </style>
            """,
            unsafe_allow_html=True
        )

        # ── Sidebar Logo & Header ──
        st.markdown(
            """
            <div class="sidebar-header-container">
              <div style="font-size: 3.5rem; line-height: 1;">🛡️</div>
              <div class="sidebar-title">AnomAlert</div>
              <div class="sidebar-subtitle">Behavioral Risk Scoring<br>for Authentication Events</div>
            </div>
            <div style="border-top: 1px solid rgba(128, 128, 128, 0.15); margin: 20px 0;"></div>
            <div style="font-size: 1.1rem; font-weight: 600; color: var(--text-color); margin-bottom: 16px; font-family: var(--font);">Quick Summary</div>
            """,
            unsafe_allow_html=True
        )

        # ── Quick Summary Metrics Cards ──
        summary = load_sidebar_summary()

        st.markdown(
            f"""
            <!-- Total Logins Card -->
            <div class="metric-card">
              <div class="metric-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
              </div>
              <div class="metric-info">
                <span class="metric-label">Total Logins</span>
                <span class="metric-value">{summary['total_logins']:,}</span>
              </div>
            </div>

            <!-- Success Rate Card -->
            <div class="metric-card">
              <div class="metric-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>
              </div>
              <div class="metric-info">
                <span class="metric-label">Success Rate</span>
                <span class="metric-value">{summary['success_rate']:.2f}%</span>
              </div>
            </div>

            <!-- Failed Logins Card -->
            <div class="metric-card">
              <div class="metric-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
              </div>
              <div class="metric-info">
                <span class="metric-label">Failed Logins</span>
                <span class="metric-value">{summary['failed_logins']:,}</span>
              </div>
            </div>

            <!-- Unique Devices Card -->
            <div class="metric-card">
              <div class="metric-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="3" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
              </div>
              <div class="metric-info">
                <span class="metric-label">Unique Devices</span>
                <span class="metric-value">{summary['unique_devices']:,}</span>
              </div>
            </div>

            <!-- Countries Accessed Card -->
            <div class="metric-card">
              <div class="metric-icon-container">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>
              </div>
              <div class="metric-info">
                <span class="metric-label">Countries Accessed</span>
                <span class="metric-value">{summary['unique_countries']}</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ── Last Data Refresh Section ──
        db_path = "AnomAlert.sqlite"
        if os.path.exists(db_path):
            mtime = os.path.getmtime(db_path)
            refresh_time = datetime.datetime.fromtimestamp(mtime).strftime("%d %b %Y %I:%M %p")
        else:
            refresh_time = "Unknown"

        st.markdown("<div style='border-top: 1px solid rgba(128, 128, 128, 0.15); margin: 20px 0;'></div>", unsafe_allow_html=True)

        col_time, col_btn = st.columns([3.5, 1])
        with col_time:
            st.markdown(
                f"""
                <div style="font-family: var(--font); display: flex; flex-direction: column;">
                  <span style="font-size: 0.85rem; color: var(--secondary-text-color); font-weight: 500;">Last Data Refresh</span>
                  <span style="font-size: 0.95rem; font-weight: 600; color: var(--text-color); margin-top: 4px;">{refresh_time}</span>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col_btn:
            st.write("")  # vertical spacer to align nicely with double line text
            if st.button("↻", key="sidebar_refresh_btn", help="Clear cache & reload data"):
                st.cache_data.clear()
                st.rerun()
