import yfinance as yf
import numpy as np
import pandas as pd
x = False

portfolio = {}
list_of_tickers = {}
value = {}

flag = False
while (flag == False):
    try:
        number_of_tickers = input("how many tickers do you want to add to your porfolio?");
        print("please enter", number_of_tickers, "tickers")
        tickers_as_int = int(number_of_tickers)
        flag = True

    except ValueError:
        print("value Error")
        print("Do it again")

    while (tickers_as_int > 0):
        # for i in range(tickers_as_int) :
        print(tickers_as_int)
        try:
            # print("i ", i)
            # enter a valid ticker value
            # print("in the try block")
            value = input("please enter a valid ticker")
            print("you entered", value);
            # print("type i ", type(value))

            ticker = yf.Ticker(value)
            table = ticker.income_stmt

            # NET INCOME 2022
            print("net income 2022")

            net_income_2022 = float(
                table[table.columns.values[1]].iloc[table.index == "Net Income"].to_string(index=False).strip())
            print(net_income_2022)
            # x = True
            # print("after break")

            portfolio[value] = {}
            print("portfolio")
            print(portfolio)

            ###DECREMENTING INDEX
            tickers_as_int -= 1

            # portfolio[value]['net_income_2022'] = net_income_2022
            # print("portfolio[value]['net_income_2022']")
            # print("****")
            # print(portfolio)

            # value[0] = net_income_2022
            # print("value")
            # print(value)

            print("net income 2023")
            # msft = yf.Ticker("MSFT")
            # table = msft.income_stmt
            net_income_2023 = float(
                table[table.columns.values[0]].iloc[table.index == "Net Income"].to_string(index=False).strip())
            print(net_income_2023)

            print("percent change")
            percent_change_net_income = (((net_income_2023 - net_income_2022) / net_income_2022) * 100)
            print(percent_change_net_income)
            portfolio[value]['%change_net_income'] = percent_change_net_income
            print(portfolio)

            list_of_tickers[0] = percent_change_net_income

            print("gross profit 2022")
            msft = yf.Ticker("MSFT")
            table = msft.income_stmt
            gross_profit_2022 = float(
                table[table.columns.values[1]].iloc[table.index == "Gross Profit"].to_string(index=False).strip())
            print(gross_profit_2022)

            print("gross profit 2023")
            msft = yf.Ticker("MSFT")
            table = msft.income_stmt
            gross_profit_2023 = float(
                table[table.columns.values[0]].iloc[table.index == "Gross Profit"].to_string(index=False).strip())
            print(gross_profit_2023)

            print("percent change")
            percent_change_gross_profit = (((gross_profit_2023 - gross_profit_2022) / gross_profit_2022) * 100)
            print(percent_change_gross_profit)
            portfolio[value]['%change_gross_profit'] = net_income_2022
            print(portfolio)

            list_of_tickers[1] = percent_change_gross_profit

            list = [percent_change_net_income, percent_change_gross_profit]
            array = np.array(list)
            # print("array")
            # print(array)
            # print("list of tickers")
            # print(list_of_tickers);
            x = False
        except IndexError:
            print("in the except block")
            print("Do it again")
