#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, redirect
import requests
from iexfinance import Stock
import datetime
import json

with open('stocks.json') as f:
    data = json.load(f)

app = Flask(__name__)

global stocks_list_input

class Stock:

    def __init__(self, amount,strategies,stocks):
        self.amount = amount
        self.strategies = strategies
        self.stocks = stocks

    def inputStrategies(self, strategies):
        self.strategies = strategies    

    def inputStocks(self,stocks):
        self.stocks = stocks

@app.route('/', methods = ['GET'])
def display_strategies():
    strategies = ['Ethical Investing','Growth Investing','Index Investing','Quality Investing','Value Investing']
    strategiesPicked = request.form.getlist("strategies")


    return render_template('index.html', strategies = strategies)


@app.route('/stocks', methods = ['POST'])
def display_stocks():
    stocks = []
    userAmount = request.form['Amount']
    investment_amount = float(userAmount)
    strategiesPicked = request.form.getlist("strategies")
    if len(strategiesPicked) == 0:
        errorMessage = 'Please select at least 1 strategy'
        return render_template('error.html', errorMessage = errorMessage)
    strategy1 = strategiesPicked[0]
    strategy2 = ''
    errorMessage = ''
    two_strategies = 0

    if len(strategiesPicked) > 1:
        two_strategies = 1
        strategy2 = strategiesPicked[1]
    if len(strategiesPicked) > 2:
        errorMessage = 'Please select upto 2 strategies'
        return render_template('error.html', errorMessage=errorMessage)

    

    for s in strategiesPicked:
        stocks.append(data[s])

    stocks_list = [item for sublist in stocks for item in sublist]
    s =  Stock(userAmount,strategiesPicked,stocks_list)

    stocks = stocks_list

    # print(stocks_list)


    # portfolio_dict = {}
    # now = datetime.datetime.now()
    # print("in portfolio")
    # for stock in stocks_list:
    #     ticker_symbol = data[stock]

    #     portfolio_list = []

    #     for i in range(4,0,-1):
    #         date = now - datetime.timedelta(days=i)

    #         lookup_date = str(date.year)+str(date.month)+str(date.day)
    #         stock_info = requests.get('https://api.iextrading.com/1.0/stock/'+ticker_symbol+'/chart/date/'+lookup_date)

    #         if stock_info.status_code == 200:
    #             json_data = stock_info.json()
    #             portfolio_list.add(json_data['marktOpen'])
    #         else:
    #             print("Error: API unreachable") 

    #     portfolio_dict[ticker_symbol] = portfolio_list

    # print("####:    "+str(portfolio_dict))

    stock_dict = {}
    latestPriceDictionary = {}
    changeDictionary = {}
    companyNameDictionary = {}
    percent_change1 = {}
    stock_quote = []
    sortedChange = []

    param_filter = '?filter=companyName,latestPrice,latestTime,change,changePercent'

    for stock in stocks_list:

        ticker_symbol = data[stock]
        now = datetime.datetime.now()
        current_datetime = str(now.month)+" "+str(now.day)+" "+str(now.hour)+":"+str(now.minute)+":"+str(now.second)+" "+str(now.year)
        stock_info = requests.get('https://api.iextrading.com/1.0/stock/'+ticker_symbol+'/quote/'+param_filter)

        if stock_info.status_code == 200:
            json_data = stock_info.json()
            changePercent = json_data['changePercent']

            latestPrice = json_data['latestPrice']
            change = json_data['change']
            companyName = json_data['companyName']

            stock_quote.append(json_data)
            # print("Stock quote list:    "+str(stock_quote))

            stock_dict[stock] = changePercent
            latestPriceDictionary[stock] = latestPrice
            changeDictionary[stock] = change
            companyNameDictionary[stock] = companyName

        else:
            print("Error: API not reachable!!")

    stocks_list_input = stock_quote

    for x in stock_quote:
        percent_change1 = stock_dict.values()
        latest_Price = latestPriceDictionary.values()
        changeInPrice = changeDictionary.values()
        compName = companyNameDictionary.values()
     
    percent_change1 = changeInPrice[0]
    percent_change2 = changeInPrice[1]
    percent_change3 = changeInPrice[2]

    if percent_change1 > percent_change2 and percent_change1 > percent_change3 :
        
        amount1 = 0.5 * investment_amount

        if percent_change2 > percent_change3 :
            amount2 = 0.3 * investment_amount
            amount3 = 0.2 * investment_amount

        elif percent_change3 > percent_change2 :
            amount3 = 0.3 * investment_amount
            amount2 = 0.2 * investment_amount

        # print("percent_change1 is greatest")


    if percent_change2 > percent_change1 and percent_change2 > percent_change3 :
        
        amount2 = 0.5 * investment_amount

        if percent_change1 > percent_change3 :
            amount1 = 0.3 * investment_amount
            amount3 = 0.2 * investment_amount

        elif percent_change3 > percent_change1 :
            amount3 = 0.3 * investment_amount
            amount1 = 0.2 * investment_amount

        # print("percent_change2 is greatest")


    if percent_change3 > percent_change2 and percent_change3 > percent_change1 :
            
        amount3 = 0.5 * investment_amount

        if percent_change2 > percent_change1 :
            amount2 = 0.3 * investment_amount
            amount1 = 0.2 * investment_amount

        elif percent_change1 > percent_change2 :
            amount1 = 0.3 * investment_amount
            amount2 = 0.2 * investment_amount

        # print("percent_change3 is greatest")
 
    return render_template('displayStock.html',investment_amount = userAmount, chosen_strategy = strategiesPicked, compName= compName, 
        changeInPrice=changeInPrice, latestPrice= latest_Price, amount1 =amount1, amount2=amount2,
        amount3 =amount3, two_strategies=two_strategies, strategy1= strategy1, strategy2=strategy2)

@app.route('/portfolio', methods = ['POST'])
def displayportfolio(): 

    portfolio_dict = {}
    now = datetime.datetime.now()
    print("in portfolio")
    

    print(stocks_list_input)

    for stock in stocks_list:
        ticker_symbol = data[stock]

        portfolio_list = []

        for i in range(4,0,-1):
            date = now - datetime.timedelta(days=i)

            lookup_date = str(date.year)+str(date.month)+str(date.day)
            stock_info = requests.get('https://api.iextrading.com/1.0/stock/'+ticker_symbol+'chart/date/'+lookup_date)

            if stock_info.status_code == 200:
                json_data = stock_info.json()
                portfolio_list.add(json_data['marktOpen'])
            else:
                print("Error: API unreachable") 

        portfolio_dict[ticker_symbol] = portfolio_list

    print("####:    "+str(portfolio_dict))       

if __name__ == '__main__':
    app.debug = True

    app.run(host="0.0.0.0", port=3000)