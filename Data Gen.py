import numpy as np
import random as rd
import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd

odd=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
split=[1,2]

#Simulates a set number of roulette games with given wager, bet type and money start amount
def num_games(bet,wager,payout,games,start_money):
    money = start_money
    for game in range(games):
        roll = rd.randint(1,38)
        if roll in bet:
            money += payout*min(wager,money)
        else:
            money -= min(wager,money)
        if money<0:
            return 0
    return money

#Caluclates standard deviation of winnings for a specific wager and number of games
def std(bet,wager,payout,games,start_money):
    rounds = 30000 #number of simulated games
    a = np.empty(0)
    for i in range(rounds):
        a = np.append(num_games(bet,wager,payout,games,start_money),a)
    return np.std(a)

#Creates matrix of values of standard deviation of winnings across a range of bets and games played
def std_matrix(bet,payout,start_money):
    b = np.ones(29)
    for games in range(2,50,2):
        a = np.empty(0)
        for wager in range(2,60,2):
            a = np.append(a,std(bet,wager,payout,games,100))
        b=np.vstack((a,b))
        if games%5==0:
            print(games*2, "% Complete")
    print('100 % complete')
    return b

#Caluclates average winnings/loss for a specific wager and number of games
def avg(bet,wager,payout,games,start_money):
    rounds = 30000 #number of simulated games
    avg = 0
    for i in range(rounds):
        avg+=num_games(bet,wager,payout,games,start_money)
    return(avg/rounds)

#Creates matrix of values of average winnings across a range of bets and games played
def avg_matrix(bet,payout,start_money):
    b = np.ones(29)
    for games in range(2,50,2):
        a = np.empty(0)
        for wager in range(2,60,2):
            a = np.append(a,avg(bet,wager,payout,games,100))
        b=np.vstack((a,b))
        if games%5==0:
            print(games*2, "% Complete")
    print('100 % complete')
    return b

#creates CSV file to save data
def make_csv(matrix,file):
    df = pd.DataFrame(matrix)
    df.to_csv(file)
    print(file,'Created')

"""
Below lines create data files for different bet types when run. Average winnings/loss as well as standard deviation information stored as CSV files
"""
    
make_csv(split_avg,'CSVs\splits_avg.csv')
make_csv(odd_std,'CSVs\odd_std.csv')
make_csv(split_std,'CSVs\split_std.csv')

odd_avg = avg_matrix(odd,1,100)
make_csv(odd_avg,'CSVs\odd_avg.csv')
odd_std = std_matrix(odd,1,100)
make_csv(odd_std,'CSVs\odd_std.csv')

split_avg =avg_matrix(split,17,100)
make_csv(split_avg,'CSVs\splits_avg.csv')
split_std = std_matrix(split,17,100)
make_csv(split_std,'CSVs\split_std.csv')

straight_avg = avg_matrix([14],35,100)
make_csv(straight_avg,'CSVs\straight_avg.csv')
straight_std = std_matrix([14],35,100)
make_csv(straight_std,'CSVs\straight_std.csv')

corner = [11,12,14,15]
corner_avg = avg_matrix(corner,8,100)
make_csv(corner_avg,'CSVs\corner_avg.csv')
corner_std = std_matrix(corner,8,100)
make_csv(corner_std,'CSVs\corner_std.csv')

dozens = [1,2,3,4,5,6,7,8,9,10,11,12]
dozens_avg = avg_matrix(dozens,2,100)
make_csv(dozens_avg,'APP\CSVs\Two_to_one_avg.csv')
dozens_std = std_matrix(dozens,2,100)
make_csv(dozens_std,'APP\CSVs\Two_to_one_std.csv')

sixes = [1,2,3,4,5,6]
six_avg = avg_matrix(sixes,5,100)
make_csv(six_avg,'APP\CSVs\Five_to_one_avg.csv')
six_std = std_matrix(sixes,5,100)
make_csv(six_std,'APP\CSVs\Five_to_one_std.csv')
