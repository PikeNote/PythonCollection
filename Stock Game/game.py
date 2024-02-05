import math
import os
import random
import time
import sys
from termcolor import colored
import termchart
stocks = [
{"name":"Real World Connections","price":200, "abrv":"RWC","pastcost":200,"item":[200]}
,
{"name":"Intro to Python","price":68,"abrv":"PYN","pastcost":68,"item":[68]}
,
{"name":"Robotics","price":50,"abrv":"RBT","pastcost":50,"item":[50]}
,
{"name":"Next Gen Tech","price":23,"abrv":"NGT","pastcost":23,"item":[23]}
,
{"name":"Beginner Web Dev","price":4,"abrv":"BWD","pastcost":4,"item":[4]}
,
{"name":"Advanced Web Dev","price":17,"abrv":"AWD","pastcost":17,"item":[17]}
,
{"name":"Film","price":7,"abrv":"FLM","pastcost":7,"item":[7]}
,
{"name":"Architecture","price":32,"abrv":"ACT","pastcost":32,"item":[32]}
,
{"name":"Android App Dev","price":1,"abrv":"APD","pastcost":1,"item":[1]}
,
{"name":"Game Development","price":2,"abrv":"APD","pastcost":2,"item":[2]}
]



ownedstocks = []

user_balance = 1000

def stargame():
  print ("Welcome to the Stock Market game!")
  name = input("Enter your name here: ") 

  os.system('clear')

  print (f"Get ready {name}, the game is about to begin!")
  stockMenu()


#list( filter((lambda x: x < 0), range(-10,5)))

def buystocks():
  global user_balance
  newmsg = "Number - Stock Name (Stock Code) - Price\n"
  number = 1
  for stock in stocks:
    newmsg += f"{str(number)}) - {stock['name']} ({stock['abrv']}) - {stock['price']} RWC Bucks\n"
    number+=1
  user_input = input(newmsg + "\nChoose a number (1-11) to select what stock you would like\n\nType 'cancel' to go back to the main screen\n")
  if (user_input.isnumeric()):
   os.system("clear")
   if (int(user_input) > 0 and int(user_input) <= 11):
     priceperstock = stocks[int(user_input)-1]['price']
     youcanbuy = math.floor(user_balance / priceperstock)
     if (youcanbuy == 0):
       os.system("clear")
       print("You don't have a sufficient balance!")
       stockMenu()
     stockamount = input(f"Please enter how much of this stock you want to buy!\n\nYour balance: {user_balance}\nPrice Per Stock: {priceperstock}\nYou can buy {youcanbuy} stocks\n\n")
     
     if (stockamount.isnumeric()):
       os.system('clear')
       iiii = 0
       while (iiii != int(stockamount)):
         ownedstocks.append(stocks[int(user_input) - 1]['abrv'])
         iiii+=1
       user_balance -= stocks[int(user_input) - 1]['price'] * int(stockamount)
       
       stockItem = stocks[int(user_input) - 1]
       print(f"Congratulations!\nYou have purchased {stockamount} stock in {stockItem['name']}\n")
       randomizestock(False)
     elif (user_input == "cancel"):
       os.system('clear')
       stockMenu()
     else:
       os.system('clear')
       print("Please enter a NUMERIC number\n\n")

  elif (user_input == "cancel"):
    os.system('clear')
    stockMenu()
  else:
    os.system('clear')
    print("Please enter a NUMERIC number between 1-11\n\n")
    buystocks()


def sellstock():
  global stocks
  global user_balance
  stockCount = {i:ownedstocks.count(i) for i in ownedstocks}
  stockKeys = stockCount.keys()
  newmsg = "Number - Stock Name (Stock Code) - Price\n"
  number = 1
  stockKe = []
  for stock in stockKeys:
    #stockitem = stockdict[stock]
    #{"PYN":{"price":1}}
    stockitem = [stk for stk in stocks if(stk['abrv'] == stock)][0]
    stockKe.append(stock)
    newmsg += f"{str(number)}) - {stockitem['name']} ({stockitem['abrv']}) - {stockitem['price']} RWC Bucks\n"
    number+=1
  user_input = input(newmsg + f"\nChoose a number (1-{len(stockKeys)}) to select what stock you would like\n\nType 'cancel' to go back to the main screen\n")
  if (user_input.isnumeric()):
    newlist = list(dict.fromkeys(ownedstocks))
    os.system("clear")
    if (int(user_input) > 0 and int(user_input) <= len(stockKeys)):
      stockitem = [stk for stk in stocks if(stk['abrv'] == stockKe[int(user_input)-1])][0]
      priceperstock = stockitem['price']
      youcansell = stockCount[newlist[int(user_input)-1]]
      int(user_input) > youcansell
      if int(user_input) > youcansell:
        os.system("clear")
        print("You don't have a sufficient amount of that stock!")
        stockMenu()
      stockamount = input(f"Please enter how much of this stock you want to sell!\n\nYour balance: {user_balance}\nPrice Per Stock: {priceperstock}\nYou can sell {youcansell} stocks\n\n")
     
      if (stockamount.isnumeric()):
        os.system('clear')
        iiii = 0
        bruh = newlist[int(user_input)-1]
        while (iiii != int(stockamount)):
          ownedstocks.remove(bruh)#ownedstocks[int(user_input) - 1])
          iiii+=1

        user_balance += stocks[int(user_input) - 1]['price'] * int(stockamount)
        print(f"Congratulations!\nYou have sold {stockamount} stock in {stockitem['name']}\n")
        randomizestock(False)
      else:
         os.system('clear')
         print("Please enter a NUMERIC number\n\n")
  elif (user_input == "cancel"):
    os.system('clear')
    stockMenu()
  else:
    os.system("clear")
    print(f"Please enter a NUMERIC number between 1-{len(stockKeys)}\n\n")
    sellstock()

    

def showstocks():
  os.system("clear")
  print("NAME (ABRV) | COST | PRICE NOW | PRICE BEFORE")
  somei = 0
  for stock in stocks:
    somei += 1
    change = stock["price"]-stock["pastcost"]
    pastchange = stock["pastcost"]
    if (change > 0):
      change = colored(change, 'green')
    elif (change <0):
      change = colored(change, 'red')
    else:
      change = colored(change, 'yellow')
    abrv = stock["abrv"]
    if len(abrv) < 4:
	    abrv += " "*(4-len(abrv))
    
    print("{}){} ({})".format(somei,stock["name"],stock["abrv"])+" - {}".format(change) + f" | {stock['price']} | {pastchange}")
  usrin = input("\n\nIf you would like to see the stock price graph, please enter an stock number. (1-11)\n")
  os.system("clear")
  if (usrin.isnumeric() and int(usrin) > 0 and int(usrin) <= 11):
    graph = termchart.Graph([])
    graph.setCols(80)
    graph.setRows(60)
    for stocknum in stocks[int(usrin) - 1]["item"]:
      graph.addData(stocknum)
    graph.draw()
    print(f"Stock - {stocks[int(usrin) - 1]['name']} | Price - {stocks[int(usrin) - 1]['price']}")
    input("")
    os.system("clear")
    stockMenu()
  else:
    stockMenu()
  
def randomizestock(test):
  for stock in stocks:
    stock["pastcost"] = stock["price"]
    newprice = random.randrange(
		-math.ceil(stock["price"]/10),
		math.ceil(stock["price"]/10)+1
	)
    if stock["price"] + newprice <= 1:
      stock["price"] = 1
      stock["item"].append(1)
    else:
      stock["price"] += newprice
      stock["item"].append(stock["price"])
  if (test):
    return True
  else:
    stockMenu()
  
  
def stockMenu():
  stockMenuOwn = "None"
  if (len(ownedstocks) != 0):
    stockMenuOwn = ""

    stockCount = {i:ownedstocks.count(i) for i in ownedstocks}
    newOwnedStocks = []
    for i in ownedstocks: 
      if i not in newOwnedStocks: 
        newOwnedStocks.append(i) 
    

    
    for stocko in newOwnedStocks:
      stockitem = list(filter((lambda stock: stock['abrv'] == stocko), stocks))
      stockquan = stockCount[stocko]
      stockname = stockitem[0]['name']
      stockabrv = stockitem[0]['abrv']
      stockprice = stockitem[0]['price'] * stockquan
      

      if (stockprice > stockitem[0]['pastcost'] * stockquan):
        stockchange = "^"
      elif (stockprice < stockitem[0]['pastcost']* stockquan):
        stockchange = "v"
      elif (stockprice == stockitem[0]['pastcost']* stockquan):
        stockchange = "~"
      stockMenuOwn += f"x{stockquan} {stockname} {stockabrv} - ${stockprice} RWC Bucks {stockchange}\n"

#for stock change

    
  userinput = input(f"""
Legend:
~ = No Change
^ = Increase price
v = Decrease Price

Balance:
{user_balance} RWC Bucks

Your Stocks:
{stockMenuOwn}

1) Buy Stocks
2) Sell Stocks
3) Hold/Pass Turn
4) Show stocks

(Respond with a number 1-4)
""")

  if (userinput.isnumeric()):
    if (int(userinput) > 0 and int(userinput) <= 4):
      userinput = int(userinput)
      os.system("clear")
      if (userinput == 1):
        buystocks()
      elif (userinput == 2):
        sellstock()
      elif (userinput == 3):
        os.system("clear")
        raninput = input("How many turns would you like to hold your stock?\n")
        if (raninput.isnumeric):
          os.system("clear")
          i = 0
          while i < int(raninput):
            i += 1
            randomizestock(True) 
          stockMenu()
        else:
          os.system("clear")
          print("You didn't enter a valid number!\nExiting..\n\n")
          stockMenu()
      elif (userinput == 4):
        os.system("clear")
        showstocks()
      else:
        os.system("clear")
        stockMenu()
    else:
      os.system("clear")
      stockMenu()
  else:
    os.system("clear")
    stockMenu()



stargame()