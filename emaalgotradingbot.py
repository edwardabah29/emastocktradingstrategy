# Exponential moving average method for algorithimc stock trading


# Import libraries
import pandas as panda
import numpy as nump
import matplotlib.pyplot as pt
pt.style.use('fivethirtyeight')



# Store the data
secuirity_data_frame = panda.read_csv('BTC-USD.csv')


# Set the date as index
secuirity_data_frame = secuirity_data_frame.set_index(panda.DatetimeIndex(secuirity_data_frame['Date'].values))


# Exponential moving average
def EMA(data, period=30, column='Close'): # Take in the close price column from our data set
    return data[column].ewm(span=period, adjust=False).mean()


# Create a new column to store the EMA
secuirity_data_frame['EMA30'] = EMA(secuirity_data_frame)


# Create the strategy
def strategy(data_frame):
    buy = [ ]   # Empty buy list
    sell = [ ]  # Empty sell list
    flag = 0    # To indicate if we last bought or sold the asset
    buy_price = 0 # place holder for the last price that we bought at

    # EMA
    for i in range(0, len(data_frame)): # Create a loop to go through the data
        # if the 30 day moving average is greater than the closing price at position i and the flag = 0 indicating that its okay to buy.
        if data_frame['EMA30'][i] > data_frame['Close'][i] and flag == 0:
            buy.append(data_frame['Close'][i]) # Buy the asset and append it to the buy list
            sell.append(nump.nan) # Dont sell asset and append nan value to the sell list
            buy_price = data_frame['Close'][i]
            flag = 1
        elif data_frame['EMA30'][i] < data_frame['Close'][i] and flag == 1 and buy_price < data_frame['Close'][i]:
        # if the 30 day moving average is less than the closing price at position i and the flag = 1 indicating that its okay to sell and the last buy price is less than the price we are trying to sell at.
            sell.append(data_frame['Close'][i])
            buy.append(nump.nan)
            buy_price = 0
            flag = 0
        else:
            sell.append(nump.nan)
            buy.append(nump.nan)


    # print buy prices
    remove_nan_buy = remove_nan(buy)
    print ('Bought at prices: ', remove_nan_buy)

    # print sell prices
    remove_nan_sell = remove_nan(sell)
    print ('Sold at prices: ', remove_nan_sell)

    # print profit
    length_of_buy = len(remove_nan_buy)
    remove_nan_buy = nump.delete(remove_nan_buy, length_of_buy-1) # remove the last buy price from the list so its can be equal for profit calculation.
    for j in remove_nan_sell:
        for i in remove_nan_buy:
            profit = remove_nan_sell - remove_nan_buy
    print('Realized P/L: ', sum(profit))
    

    return(buy, sell)


# remove non numbers
def remove_nan(l):
    numpy_array = nump.array(l)
    remove_nan = numpy_array[nump.logical_not(nump.isnan(numpy_array))]
    return  remove_nan


# Get the buy and sell list
trading_strategy = strategy(secuirity_data_frame)
secuirity_data_frame['Buy'] = trading_strategy[0]
secuirity_data_frame['Sell'] = trading_strategy[1]


# Visualize the close price and the buy and sell signals
pt.figure(figsize=(16, 8))
pt.title('Close Price with buy and sell signals')
pt.plot(secuirity_data_frame['Close'], alpha = 0.5, label = 'Close' )
pt.plot(secuirity_data_frame['EMA30'], alpha = 0.5, label = 'EMA30')
pt.scatter(secuirity_data_frame.index, secuirity_data_frame['Buy'], color = 'green', label = 'Buy Signal', marker = '^', alpha = 1)
pt.scatter(secuirity_data_frame.index, secuirity_data_frame['Sell'], color = 'red', label = 'Sell Signal', marker = 'v', alpha = 1)
pt.xlabel('Date')
pt.ylabel('Close Price in USD')
pt.show()
