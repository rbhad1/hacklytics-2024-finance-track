from flask import Flask, request, render_template_string
import yfinance as yf
import numpy as np

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Data</title>
</head>


<head>
    <title>Banner Example</title>
    <style>
        .banner {
        background-color: #4CAF50; /* Green background */
        color: white; /* White text */
        text-align: center; /* Centered text */
        padding: 20px; /* Some padding */
        font-size: 24px; /* Large text */
    }
    </style>
</head>
<body>  

<div class="banner">
    PANDA
</div>
</body>  

<head>
<style>
    body {background-color: #add8e6;}
</style>
</head>

<body>
    <h2 style="color:blue;">Enter Ticker Symbols</h2>
    
    <form method="POST">
        <label for="tickers">Tickers (comma-separated, e.g., AAPL, MSFT, GOOGL):</label><br>
        <input type="text" id="tickers" name="tickers"><br>
        <input type="submit" value="Submit">
    </form>
</body>

<head>
    <style>
        h2 {
            font-size: 20px;
        }
    </style>
</head>


</html>
'''

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        tickers = request.form['tickers'].split(',')
        data = {}
        for ticker in tickers:
            try:
                stock = yf.Ticker(ticker.strip())
                table = stock.income_stmt
                net_income_2022 = float(table[table.columns.values[1]].iloc[table.index == "Net Income"].to_string(index=False).strip())
                net_income_2023 = float(table[table.columns.values[0]].iloc[table.index == "Net Income"].to_string(index=False).strip())
                percent_change_net_income = (((net_income_2023 - net_income_2022) / net_income_2022) * 100)

                gross_profit_2022 = float(
                    table[table.columns.values[1]].iloc[table.index == "Gross Profit"].to_string(index=False).strip())
                gross_profit_2023 = float(
                    table[table.columns.values[0]].iloc[table.index == "Gross Profit"].to_string(index=False).strip())
                percent_change_gross_profit = (((gross_profit_2023 - gross_profit_2022) / gross_profit_2022) * 100)
                data[ticker] = {"net income": percent_change_net_income,
                                "gross profit": percent_change_gross_profit}


            except Exception as e:
                data[ticker] = f"Error retrieving data: {e}"
        return f'<pre>{data}</pre>'
    else:
        return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)