# stock_web_app.py
import streamlit as st
from modules import stock_analysis
import datetime
import os

st.set_page_config(page_title="Stock & Mutual Fund Research Bot", layout="wide")

st.title("📊 Stock & Mutual Fund Research Bot")

# Create two tabs for Stock and Mutual Fund analysis
tabs = st.tabs(["📈 Stock Analysis", "💰 Mutual Fund Explorer"])

# --- STOCK ANALYSIS TAB ---
with tabs[0]:
    st.subheader("📌 Enter Stock Symbol (e.g., TCS.NS)")
    symbol = st.text_input("Symbol:", value="")

    analyze_clicked = st.button("Analyze Stock")
    export_pdf_clicked = st.button("⬇ Export to PDF")
    export_excel_clicked = st.button("⬇ Export to Excel")

    if symbol and (analyze_clicked or export_pdf_clicked or export_excel_clicked):
        with st.spinner("Fetching data..."):
            result = stock_analysis.fetch_stock_fundamentals(symbol)

        if "error" in result:
            st.error(f"Error: {result['error']}")
        else:
            st.success(f"Analysis for {symbol.upper()}:")
            st.json(result)

            today = datetime.date.today().strftime("%Y-%m-%d")
            pdf_path = f"{symbol}_{today}_report.pdf"
            excel_path = f"{symbol}_{today}_report.xlsx"

            if export_pdf_clicked:
                stock_analysis.export_to_pdf(result, pdf_path)
                with open(pdf_path, "rb") as f:
                    st.download_button("📄 Download PDF", f, file_name=pdf_path)

            if export_excel_clicked:
                stock_analysis.export_to_excel(result, excel_path)
                with open(excel_path, "rb") as f:
                    st.download_button("📊 Download Excel", f, file_name=excel_path)

# --- MUTUAL FUND TAB ---
with tabs[1]:
    st.subheader("🔍 Explore Top Mutual Funds")
    st.markdown("Coming soon: Mutual Fund filters and ranking based on returns, risk, and consistency.")

    sample_funds = [
        {"Fund": "Parag Parikh Flexi Cap", "Category": "Flexi Cap", "5Y Returns": "17.5%", "Rating": "★★★★★"},
        {"Fund": "Mirae Asset Large Cap", "Category": "Large Cap", "5Y Returns": "14.2%", "Rating": "★★★★"},
        {"Fund": "Axis Bluechip", "Category": "Large Cap", "5Y Returns": "12.3%", "Rating": "★★★"},
    ]

    st.table(sample_funds)
