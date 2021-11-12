#!/usr/bin/env python
# coding: utf-8

# In[766]:


import numpy as np
import random as rd
import matplotlib.pyplot as plt
import scipy.stats as st
import pandas as pd


# In[755]:


odd=[1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]
split=[1,2]


# In[829]:


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


# In[830]:


def std(bet,wager,payout,games,start_money):
    rounds = 27778
    a = np.empty(0)
    for i in range(rounds):
        a = np.append(num_games(bet,wager,payout,games,start_money),a)
    return np.std(a)


# In[831]:


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


# In[832]:


def avg(bet,wager,payout,games,start_money):
    #27778
    rounds = 27778
    avg = 0
    for i in range(rounds):
        avg+=num_games(bet,wager,payout,games,start_money)
    return(avg/rounds)


# In[833]:


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


# In[834]:


def prob_matrix(x,means,stds):
    b = np.ones(29)
    for i in range(24):
        a = np.empty(0)
        for j in range(29):
            mu = means[i][j]
            sigma = stds[i][j]
            z = (x-mu)/sigma
            prob = 1-st.norm.cdf(z)
            a = np.append(a,prob)
        b=np.vstack((a,b))
        if i%5==0:
            print(i*2, "% Complete")
    print('100 % complete')
    return b


# In[859]:


def make_fig(arr,title,name,plt_type):
    plt.imshow(arr[1:-1],cmap='jet',extent=[5, 60, 5, 50],interpolation='quadric')
    plt.xlabel('Wager')
    plt.ylabel('Number of Games')
    plt.title(title)
    if plt_type == 'avg':
        plt.colorbar(label = 'Amount remaining of n number of games')
    elif plt_type == 'std':
        plt.colorbar(label = 'Standard Deviation of Winnings')
    elif plt_type == 'prob':
        plt.clim(0,1)
        plt.colorbar(label = 'Probabilty of Winning designated amount or more')
    plt.savefig(('{}.png').format(name))
    plt.show()


# In[853]:


def reduce(x,y):
    y_list = y.tolist()
    y_red = []
    x_uni = np.unique(x)
    for i in x_uni:
        x_i = np.where(x == i)[0].tolist()
        avg = 0
        for j in x_i:
            avg+= y_list[j]
        y_red.append(avg/len(x_i))
    return x_uni.tolist(),y_red


# In[587]:


def equivalue_plot(x,y):
    wagers = np.arange(2,60,2)
    games = np.arange(2,52,2)
    xfin = []
    yfin= []
    for i in range(len(x)):
        xfin.append(wagers[i])
    for j in y:
        k = int(round(j))
        yfin.append(games[k-1])
    #yfin.reverse()
    plt.plot(xfin,yfin)
    plt.show()


# In[815]:


def make_csv(matrix,file):
    df = pd.DataFrame(matrix)
    df.to_csv(file)
    print(file,'Created')
def open_csv(file):
    df = pd.read_csv(file)
    a = df.drop('Unnamed: 0',axis =1).to_numpy()
    return a

make_csv(split_avg,'CSVs\splits_avg.csv')
make_csv(odd_std,'CSVs\odd_std.csv')
make_csv(split_std,'CSVs\split_std.csv')


# In[836]:


odd_avg = avg_matrix(odd,1,100)
make_csv(odd_avg,'CSVs\odd_avg.csv')
odd_std = std_matrix(odd,1,100)
make_csv(odd_std,'CSVs\odd_std.csv')


# In[837]:


split_avg =avg_matrix(split,17,100)
make_csv(split_avg,'CSVs\splits_avg.csv')
split_std = std_matrix(split,17,100)
make_csv(split_std,'CSVs\split_std.csv')


# In[838]:


straight_avg = avg_matrix([14],35,100)
make_csv(straight_avg,'CSVs\straight_avg.csv')
straight_std = std_matrix([14],35,100)
make_csv(straight_std,'CSVs\straight_std.csv')


# In[839]:


corner = [11,12,14,15]
corner_avg = avg_matrix(corner,8,100)
make_csv(corner_avg,'CSVs\corner_avg.csv')
corner_std = std_matrix(corner,8,100)
make_csv(corner_std,'CSVs\corner_std.csv')


# In[880]:


dozens = [1,2,3,4,5,6,7,8,9,10,11,12]
dozens_avg = avg_matrix(dozens,2,100)
make_csv(dozens_avg,'APP\CSVs\Two_to_one_avg.csv')
dozens_std = std_matrix(dozens,2,100)
make_csv(dozens_std,'APP\CSVs\Two_to_one_std.csv')


# In[881]:


sixes = [1,2,3,4,5,6]
six_avg = avg_matrix(sixes,5,100)
make_csv(six_avg,'APP\CSVs\Five_to_one_avg.csv')
six_std = std_matrix(sixes,5,100)
make_csv(six_std,'APP\CSVs\Five_to_one_std.csv')


# In[ ]:




