import streamlit as st

def set_style():
    st.markdown(
        """
        <style>
            h1, h2, h3{
                color: black;
                font-weight: bold;
                animation: fadeIn 1.5s ease-in-out;
            }
            .css-1d391kg h2 {
                color: #ffffff !important;
            }
            .stApp {
                background: linear-gradient(180deg, #162C33, #5295AB);
                font-family: 'Helvetica Neue', sans-serif;
            }
            .stDownloadButton > button {
                display: inline-flex;
                align-items: center;
                color: white;
                background-color: #28a745;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                transition: background 0.3s ease;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stDownloadButton > button:hover {
                background-color: #218838;
                transform: scale(1.05);
            }
            .stDownloadButton > button::before {
                content: url('https://img.icons8.com/fluency-systems-filled/24/FFFFFF/download.png');
                display: inline-block;
                margin-right: 8px;
            }
            .stButton > button {
                display: inline-flex;
                align-items: center;
                color: #5edc84;
                background-color: #28a745;
                border-radius: 12px;
                padding: 10px 20px;
                font-size: 16px;
                font-weight: bold;
                transition: background 0.3s ease;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            .stButton > button:hover {
                background-color: #218838;
                transform: scale(1.05);
            }
            .stButton > button::before {
                content: url('https://img.icons8.com/fluency-systems-filled/24/FFFFFF/combo-chart.png');
                display: inline-block;
                margin-right: 8px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <h1 class="tooltip">
            <img src="" style="vertical-align: middle;">
            🗖️ Operação de baldeio
            <span class="tooltiptext"></span>
        </h1>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.markdown(
        """<h2 class="tooltip"><img src="https://img.icons8.com/ios-filled/30/ffffff/filter.png" style="vertical-align: middle;">
        <span class="tooltiptext"></span></h2>""",
        unsafe_allow_html=True,
    )
