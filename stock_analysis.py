# modules/stock_analysis.py
import yfinance as yf
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def fetch_stock_fundamentals(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        result = {
            "Symbol": symbol.upper(),
            "Company Name": info.get("longName"),
            "Current Price": info.get("currentPrice"),
            "PE Ratio": info.get("trailingPE"),
            "PB Ratio": info.get("priceToBook"),
            "ROE": info.get("returnOnEquity"),
            "ROCE": info.get("returnOnAssets"),
            "Debt to Equity": info.get("debtToEquity"),
            "Dividend Yield": info.get("dividendYield"),
            "Dividend Rate": info.get("dividendRate"),
            "5Y Avg Dividend Yield": info.get("fiveYearAvgDividendYield"),
            "Market Cap": info.get("marketCap"),
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "52 Week Low": info.get("fiftyTwoWeekLow"),
            "Fair Value Hint": "Use PE vs Sector PE to gauge valuation",
        }

        return result

    except Exception as e:
        return {"error": str(e)}

def export_to_pdf(data, filename):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, height - 50, f"Stock Analysis Report: {data.get('Symbol')}")

    c.setFont("Helvetica", 12)
    y = height - 90
    for key, value in data.items():
        if key != "Symbol":
            c.drawString(40, y, f"{key}: {value}")
            y -= 20
            if y < 80:
                c.showPage()
                y = height - 50

    c.save()

def export_to_excel(data, filename):
    df = pd.DataFrame.from_dict(data, orient='index', columns=['Value'])
    df.to_excel(filename)
