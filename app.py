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
        font-size: 50px; /* Large text */
    }
    </style>
</head>
<body>  

<div class="banner">
    PANDA
</div>
<p>
Type in a stock ticker and see a brief summary of how earnings changed between the most recent fiscal 
year and the previous fiscal year. The score at the bottom summaries the changes. (It is not necessarily a 
represenation of the stock's health.)
<p>Here is what the scores mean:</p>
<p>[1] Earnings decreased drastically</p>
<p>[2] Earnings decreased slighly overall</p>
<p>[3] Earnings largely remained the same</p>
<p>[4] Earnings increased slightly</p>
<p>[5] Earnings increased a lot</p>
</body>  

<head>
<style>
    body {background-color: #add8e6;}
</style>
</head>

<body>
    <h2 style="font-size: 30px;">Enter Ticker Symbol</h2>
    
    <form method="POST">
        <label for="tickers" size="20">Ticker</label><br>
        <input type="text" id="tickers" name="tickers" size="20"><br>
        <input type="submit" value="Submit">
    </form>
    {% if data %}
        <h2>Financial Data <h2>
        <pre>{{ data }}</pre>
        <p> (percentage) </p>
        <h2>Score <h2>
        <p>{{score}} out of 5</p>
        <p style="font-size: 12px;">Please note: This data only quantifies how earnings change from year to year.</p>

    {% endif %}
    


    
</body>

<head>
    <style>
        h2 {
            font-size: 20px;
        }
    </style>
</head>
<body>
    <p>{{indicator}} </p>
</body>


</html>
'''


@app.route('/', methods=['GET', 'POST'])
def home():
    flag = False #
    while (flag == False):


        if request.method == 'POST':
            tickers = request.form['tickers'].split(',')
            data = {}
            for ticker in tickers:
                try:
                    stock = yf.Ticker(ticker.strip())
                    table = stock.income_stmt
                    net_income_2022 = float(
                        table[table.columns.values[1]].iloc[table.index == "Net Income"].to_string(index=False).strip())
                    net_income_2023 = float(
                        table[table.columns.values[0]].iloc[table.index == "Net Income"].to_string(index=False).strip())
                    percent_change_net_income = (((net_income_2023 - net_income_2022) / net_income_2022) * 100)
                    percent_change_net_income = round(percent_change_net_income, 2)

                    flag = True #

                    gross_profit_2022 = float(
                        table[table.columns.values[1]].iloc[table.index == "Gross Profit"].to_string(index=False).strip())
                    gross_profit_2023 = float(
                        table[table.columns.values[0]].iloc[table.index == "Gross Profit"].to_string(index=False).strip())
                    percent_change_gross_profit = (((gross_profit_2023 - gross_profit_2022) / gross_profit_2022) * 100)
                    percent_change_gross_profit = round(percent_change_gross_profit, 2)



                    operating_expense_2022 = float(
                        table[table.columns.values[1]].iloc[table.index == "Operating Expense"].to_string(
                            index=False).strip())
                    operating_expense_2023 = float(
                        table[table.columns.values[0]].iloc[table.index == "Operating Expense"].to_string(
                            index=False).strip())
                    percent_change_operating_expense = (
                                ((operating_expense_2023 - operating_expense_2022) / operating_expense_2022) * 100)
                    percent_change_operating_expense = round(percent_change_operating_expense, 2)



                    diluted_EPS_2022 = float(
                        table[table.columns.values[1]].iloc[table.index == "Diluted EPS"].to_string(
                            index=False).strip())
                    diluted_EPS_2023 = float(
                        table[table.columns.values[0]].iloc[table.index == "Diluted EPS"].to_string(
                            index=False).strip())
                    percent_change_diluted_EPS = (((diluted_EPS_2023 - diluted_EPS_2022) / diluted_EPS_2022) * 100)
                    percent_change_diluted_EPS = round(percent_change_diluted_EPS, 2)

                    total_revenue_2022 = float(
                        table[table.columns.values[1]].iloc[table.index == "Diluted EPS"].to_string(
                            index=False).strip())
                    total_revenue_2023 = float(
                        table[table.columns.values[0]].iloc[table.index == "Diluted EPS"].to_string(
                            index=False).strip())
                    percent_change_total_revenue = (((total_revenue_2023 - total_revenue_2022) / total_revenue_2022) * 100)
                    percent_change_total_revenue = round(percent_change_total_revenue, 2)

                    data[ticker] = {"net income": percent_change_net_income,
                                    "gross profit": percent_change_gross_profit,
                                    "operating expense": percent_change_operating_expense,
                                    "diluted EPS": percent_change_diluted_EPS,
                                    "total revenue": percent_change_total_revenue}


                except Exception as e:
                    #data[ticker] = f"Error retrieving data: {e}"
                    return render_template_string(HTML_FORM, error=str("Type in a valid ticker"))

            # calculate score
            score = 1
            for metric, value in data[ticker].items():
                if (metric == "operating expense"):
                    if (float(value) < 0 ):
                        score += 1
                else:
                    if (float(value) > 0):
                        score += 1



            return render_template_string(HTML_FORM, data=data, score=score)
            # return render_template_string(HTML_FORM + f'<pre>{data}</pre>')
        else:
            return render_template_string(HTML_FORM, error=str("Type in a valid ticker"))

            # return render_template_string(HTML_FORM)




if __name__ == '__main__':
    app.run(debug=True)
