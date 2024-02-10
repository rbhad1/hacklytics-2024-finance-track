from flask import Flask, request, render_template_string
import yfinance as yf

app = Flask(__name__)

HTML_FORM = '''
<!DOCTYPE html>
<html>
<head>
    <title>Portfolio Data</title>
</head>
<body>
    <h2>Enter Ticker Symbols</h2>
    <form method="POST">
        <label for="tickers">Tickers (comma-separated, e.g., AAPL,MSFT,GOOGL):</label><br>
        <input type="text" id="tickers" name="tickers"><br>
        <input type="submit" value="Submit">
    </form>
</body>
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
                data[ticker] = percent_change_net_income
            except Exception as e:
                data[ticker] = f"Error retrieving data: {e}"
        return f'<pre>{data}</pre>'
    else:
        return render_template_string(HTML_FORM)

if __name__ == '__main__':
    app.run(debug=True)