#   JPMorganChase.py
#
#   By Angus Lin, 2022.3.28
#
#   Remark :
#   1.  It is assumed that the trading transactions are recorded in chronological order

from datetime import timedelta
from time import time
from random import randrange

#   Declaration of error code
ERR_EMPTY_SYMBOL = 1001
ERR_SYMBOL_NOT_FOUND = 1002
ERR_ZERO_PRICE = 1003
ERR_MSG_EMPTY_SYMBOL = 'Empty symbol'
ERR_MSG_SYMBOL_NOT_FOUND = 'Symbol not found'
ERR_MSG_ZERO_PRICE = 'Zero price'

#   Class Exchange holds all stocks


class Exchange:
    def __init__(self, exchange='GBCE'):
        self.__exchange = exchange
        self.__stocks = dict()
        #   load all stocks data
        self.__loadData()

    #   load all stocks data
    def __loadData(self):
        self.__stocks['TEA'] = Stock('TEA', 'GBCE', 'Common', 0.0, 0.0, 100.0)
        self.__stocks['POP'] = Stock('POP', 'GBCE', 'Common', 8.0, 0.0, 100.0)
        self.__stocks['ALE'] = Stock('ALE', 'GBCE', 'Common', 23.0, 0.0, 60.0)
        self.__stocks['GIN'] = Stock(
            'GIN', 'GBCE', 'Preferred', 8.0, 0.02, 100.0)
        self.__stocks['JOE'] = Stock('JOE', 'GBCE', 'Common', 13.0, 0.0, 250.0)

    #   calculate Yield for stock at specified price
    def getYield(self, symbol='', price=0):
        #   symbol : symbol of stock
        #   price : price for yield calculation
        #   return yield calculated
        assert price != 0, f"Error : ({ERR_ZERO_PRICE}) {ERR_MSG_ZERO_PRICE}"
        try:
            stock = self.__stocks[symbol]
            return stock.getYield(price)
        except:
            assert stock != None, f"Error : ({ERR_SYMBOL_NOT_FOUND}) {ERR_MSG_SYMBOL_NOT_FOUND}"

    #   calculate PE Ratio for stock at speicifed price
    def getPE(self, symbol='', price=0):
        #   symbol : symbol of stock
        #   price : price for PE calculation
        #   return PE calculated
        stock = self.__stocks[symbol]
        assert stock != None, "Error : ({ERR_SYMBOL_NOT_FOUND}) {ERR_MSG_SYMBOL_NOT_FOUND}"
        return stock.getPE(price)

    #   register a buy transaction
    def addBuy(self, timestamp, symbol, price, qty):
        #   timestamp : timestamp of the transaction
        #   symbol : symbol of stock
        #   price : buy price
        #   qty : qty bought
        stock = self.__stocks[symbol]
        assert stock != None, "Error : ({ERR_SYMBOL_NOT_FOUND}) {ERR_MSG_SYMBOL_NOT_FOUND}"
        stock.addTransaction(timestamp, price, qty, 1)

    #   register a sell transaction
    def addSell(self, timestamp, symbol, price, qty):
        #   timestamp : timestamp of the transaction
        #   symbol : symbol of stock
        #   price : sell price
        #   qty : qty sold
        stock = self.__stocks[symbol]
        assert stock != None, "Error : ({ERR_SYMBOL_NOT_FOUND}) {ERR_MSG_SYMBOL_NOT_FOUND}"
        stock.addTransaction(timestamp, price, qty, -1)

    #   calculate Volume Weighted Stock Price for the stock at the specified timestamp
    def getVWPriceAt(self, timestamp, symbol):
        #   timestammp : timestamp for the calculation
        #   symbol : symbol of stock
        #   return Volume Weighted Stock Price calculated
        assert symbol in self.__stocks.keys(
        ), "Error : ({ERR_SYMBOL_NOT_FOUND}) {ERR_MSG_SYMBOL_NOT_FOUND}}"
        return self.__stocks[symbol].getVWPriceAt(timestamp)

    #   calculate Volume Weighted Stock Price for the stock at current timestamp
    def getVWPrice(self, symbol):
        #   symbol : symbol of stock
        #   return Volume Weighted Stock Price calculated
        return self.getVWPriceAt(time(), symbol)

    #   calculate GBCE All Share Index
    def getAllShareIndex(self):
        #   return GBCE All Share Index calculated
        timestamp = time()
        index = 1.0
        for symbol in self.__stocks.keys():
            index *= self.__stocks[symbol].getVWPriceAt(timestamp)
        return index ** (1.0 / len(self.__stocks.keys()))

    #   get all stock symbols
    def getAllSymbols(self):
        #   return all stock symbols
        return self.__stocks.keys()

    #   get stocks list - for debug and testing
    def getStocks(self):
        #   return a copy of the stocks dict
        return self.__stocks.copy()

    #   get transactions - for debug and testing
    def getTransactions(self, symbol):
        #   symbol : symbol of stock
        #   return a copy of the transactions of the stock
        assert symbol in self.__stocks.keys(
        ), "Error : ({ERR_SYMBOL_NOT_FOUND}) {ERR_MSG_SYMBOL_NOT_FOUND}}"
        return self.__stocks[symbol].getTransactions()

#   Class Stock holds the data of a stock


class Stock:
    def __init__(self, symbol='', exchange='', type='', lastDividend=0, fixedDividend=0.0, par=0):
        assert symbol != '', 'Error : Empty symbol'
        self.__symbol = symbol
        self.__exchange = exchange
        self.__type = type
        self.__lastDividend = lastDividend
        self.__fixedDividend = fixedDividend
        self.__par = par
        self.__transactions = list()

    def getSymbol(self):
        #   return symbol of this stock
        return self.__symbol

    def getExchange(self):
        #   return exchange of this stock
        return self.__exchange

    def getType(self):
        #   return type of this stock (Common or Preferred)
        return self.__type

    def getLastDividend(self):
        #   return last dividend of this stock
        return self.__lastDividend

    def getFixedDividend(self):
        #   return fixed dividend of this stock
        return self.__fixedDividend

    def getPar(self):
        #   return par value of this stock
        return self.__par

    def getTransactions(self):
        #   return the transaction list of this stock
        return self.__transactions.copy()

    def __str__(self):
        #   return a string representation of this stock
        return f'{self.__symbol},{self.__exchange},{self.__type},{self.__lastDividend},{self.__fixedDividend},{self.__par}'

    #   calculate yield of this stock at specified price
    def getYield(self, price):
        #   price : price for yield calculation
        #   return yield calculated
        if self.__type == 'Common':
            return self.__lastDividend / price
        elif self.__type == 'Preferred':
            return (self.__fixedDividend * self.__par) / price
        return None

    #   calculate PE Ratio of this stock at specified price
    def getPE(self, price):
        #   price : price for PE calculation
        #   return PE calculated, None if PE cannot be calculated (last dividend = 0)
        if self.__lastDividend == 0:
            return None
        else:
            return price / self.__lastDividend

    #   register a trade of this stock
    def addTransaction(self, timestamp, price, qty, action):
        #   timestamp : timestamp of this trade
        #   price : price of this trade
        #   qty : qty of this trade
        #   action : buy(1) or sell(-1)
        self.__transactions.append([timestamp, price, qty, action])

    #   calculate Volume Weighted Price of this stock at the specified timestamp
    def getVWPriceAt(self, timestamp):
        #   timestamp : timestamp for the calculation
        #   return Volume Weighted Price calculated
        index = len(self.__transactions) - 1
        if index == 0:
            return None
        start = timestamp - 5.0 / 1440.0
        volume, qty = 0, 0
        print(f"{start}/{timestamp}")
        while (index >= 0) and (self.__transactions[index][0] >= start):
            if self.__transactions[index][0] <= timestamp:
                volume += self.__transactions[index][1] * \
                    self.__transactions[index][2]
                qty += self.__transactions[index][2]
                print(f"{volume}/{qty}")
            index -= 1

        print(f'volume/qty : {volume}/{qty}')
        if qty == 0:
            return None
        else:
            return volume / qty


def test():
    exchange = Exchange()
    stocks = exchange.getStocks()
    for key in stocks.keys():
        s = stocks[key]
        print(s)


def testPEYield():
    def calcPEYield(price):
        print(f'Yield / PE at price {price}')
        symbols = exchange.getAllSymbols()
        for symbol in symbols:
            print(
                f"{symbol} : {exchange.getYield(symbol,price)} / {exchange.getPE(symbol,price)} ")

    exchange = Exchange()
    calcPEYield(100)
    #print(exchange.getYield("TEA", 0))
    try:
        print(exchange.getYield("TEA", 0))
    except:
        print("symbol ABC not found")


def testTx():
    def genTx(count):
        result = list()
        f = open('test.txt', 'w')
        for i in range(0, count):
            j = randrange(-100, 100)
            result.append([time(), 100 + j / 100, 1000 + j])
            f.write(f'{1000 + j}, {100 + j / 100}\n')
        f.close()
        return result

    exchange = Exchange()
    data = genTx(100)
    print(data)
    # for symbol in exchange.getAllSymbols():
    #     for row in data:
    #         exchange.addBuy(row[0], symbol, row[1], row[2])
    #     print(f"VWPrice: {symbol} - {exchange.getVWPrice(symbol)}")
    symbol = 'TEA'
    for row in data:
        exchange.addBuy(row[0], symbol, row[1], row[2])
    print(f"VWPrice: {symbol} - {exchange.getVWPrice(symbol)}")
    #print(f"Index : {exchange.getAllShareIndex()}")


if __name__ == '__main__':
    test()
    testPEYield()
    testTx()
