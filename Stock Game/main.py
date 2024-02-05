import http.client
import json
import os
import time
import termchart
from importlib import import_module

stockName = ""

connection = http.client.HTTPSConnection(
    'sandbox.tradier.com', 443, timeout=30)

headers = {
    "Accept": "application/json",
    "Authorization": "Bearer n1n8M9ytQRSiELVqBBFRVAGKFvxp"
}


def monitorStock(stockData, stockname):
	print(connection)
	graph = termchart.Graph([])
	graph.addData(stockData['quotes']['quote']['last'])
	graph.setCols(30)
	graph.setRows(30)
	while True:
		print(stockname)
		connection.request('GET', '/v1/markets/quotes?symbols=' + stockname,
		                   None, headers)
		response = connection.getresponse()
		content = json.loads(response.read())
		graph.addData(content['quotes']['quote']['last'])
		os.system('clear')
		graph.draw()
		print(
		    f"Stock - {content['quotes']['quote']['description']} | Price - {content['quotes']['quote']['last']}"
		)
		time.sleep(3)


def checkStk(stk):
	connection.request('GET', '/v1/markets/quotes?symbols=' + stk, None,
	                   headers)

	response = connection.getresponse()
	content = json.loads(response.read())
	if ("unmatched_symbols" in content['quotes']):
		os.system("clear")
		nst = input(
		    "Invalid stock abbreviation!\nPlease input a stock you want to monitor.\n"
		)
		checkStk(nst)
	else:
		monitorStock(content, stk)


def selectedOp(option):
	if (option.isnumeric()):
		print(option)
		os.system('clear')
		if (int((option)) == 1):
			stock_input = input(
			    "Please input what stock you want to monitor\n")
			checkStk(stock_input)
		else:
			import_module("game")
	else:
		os.system("clear")
		newop = input(
		    "Please enter a valid response. (1 or 2)\n\nChoose one of the follow options.\n\n1) Monitor Active Stock\n2) Stock Game\n\n"
		)
		selectedOp(newop)


option = input(
    "Hello\nWelcome to Stock Monitor!\n\nChoose one of the follow options.\n\n1) Monitor Active Stock\n2) Stock Game\n\n"
)

selectedOp(option)
