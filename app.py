# Importing necessary libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import cufflinks as cf
import datetime

# App title
st.markdown('''
# Stock Price App
Shown are the stock price data for query companies!
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date(2023, 1, 31))

# Retrieving tickers data
ticker_list = pd.read_csv('https://raw.githubusercontent.com/dataprofessor/s-and-p-500-companies/master/data/constituents_symbols.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list)
tickerData = yf.Ticker(tickerSymbol)
tickerDf = tickerData.history(period='1d', start=start_date, end=end_date)

# Display company information
try:
    string_name = tickerData.info['longName']
    st.header('**%s**' % string_name)

    string_summary = tickerData.info['longBusinessSummary']
    st.info(string_summary)
except KeyError:
    st.warning("Company information not available at Yahoo Finance.")

# Ticker data
st.header('**Ticker data**') 
st.write(tickerDf)
st.markdown('''
This table displays the raw ticker data for the selected stock. The table includes columns such as Open, High, Low, Close, Volume, Dividends, and Stock Splits.
''')

# Closing Price
st.header('**Closing Price**') 
st.line_chart(tickerDf.Close)
st.markdown('''
The line chart above illustrates the closing prices of the selected stock over the specified time period. It provides a visual representation of the stock's closing price trends.
''')

# Volume Price
st.header('**Volume Price**') 
st.line_chart(tickerDf.Volume)
st.markdown('''
This line chart represents the trading volume of the selected stock over the specified time period. It shows the amount of shares traded, providing insights into market activity.
''')

# Bollinger bands
st.header('**Bollinger Bands**')
qf = cf.QuantFig(tickerDf, title='First Quant Figure', legend='top', name='GS')
qf.add_bollinger_bands()
fig = qf.iplot(asFigure=True)
st.plotly_chart(fig)
st.markdown('''
The chart above displays Bollinger Bands for the selected stock. Bollinger Bands are volatility indicators that consist of a middle band being an N-period simple moving average, an upper band at K times an N-period standard deviation above the middle band, and a lower band at K times an N-period standard deviation below the middle band. They are useful for identifying overbought or oversold conditions.
''')
