import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import scipy.stats as st
import tkinter as tk
from tkinter import *
import os


path = "" #Path string should be updated to match the location where the "CSV" folder is located
file_map = {'1:1 Payout':['One_to_one_avg.csv','One_to_one_std.csv'],
            '2:1 Payout':['Two_to_one_avg.csv','Two_to_one_std.csv'],
            '5:1 Payout':['Five_to_one_avg.csv','Five_to_one_std.csv'],
            '6:1 Payout':'',
            '8:1 Payout':['Eight_to_one_avg.csv','Eight_to_one_std.csv'],
            '11:1 Payout':'',
            '17:1 Payout':['Seventeen_to_one_avg.csv','Seventeen_to_one_std.csv'],
            '35:1 Payout':['Thirty_Five_to_one_avg.csv','Thirty_Five_to_one_std.csv']
           }
#Opens CSV files and removes column titles leaving only numerical values
def open_csv(file):
    file_name = os.path.join(path,file)
    df = pd.read_csv(file_name)
    a = df.drop('Unnamed: 0',axis =1).to_numpy()
    return a

#Uses a Z test to calculate the probability of winning a given amount of money (x). Mean and standard deviation values taken from CSV files
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
    return b

#Function creates plots based off of plot type
def make_fig(arr,title,name,plt_type,save,x=0):
    plt.imshow(arr[1:-1],cmap='jet',extent=[5, 60, 5, 50],interpolation='quadric')
    plt.xlabel('Wager')
    plt.ylabel('Number of Games')
    plt.title(title)
    if plt_type == 'avg':
        plt.colorbar(label = 'Amount remaining of n number of games')
    elif plt_type == 'prob':
        plt.colorbar(label = 'Probabilty of Winning designated amount or more')
    if save =='Yes':
        plt.savefig(('{}.png').format(name))
    plt.show()

#Creates title for plot based off of plot and bet type
def title_maker(plt_type,bet,x=0):
    if plt_type == 'avg':
        title = ('{} Average Winnings').format(bet)
    if plt_type =='prob':
        title = ('Probability of winning ${} or more with {}').format(x,bet)
    return title

#If user selection onption to save figure, this function automates file name creation
def plt_file_name(plt_type,bet,x=0):
    bet_name = bet.replace(':','_to_').replace(' ','_')
    if plt_type == 'avg':
        name = ('{}{}_avg').format(path,bet_name)
        return name
    if plt_type == 'prob':
        name = ('(){}_prob_{}').format(path,bet_name,x)
        return name

#Function that is activated by the GUI to present probability plots    
def prob():
    x = int(amnt.get())
    bet = str(bet_type.get())
    save_fig = str(save.get())
    means = open_csv(file_map[bet][0])
    stds = open_csv(file_map[bet][0])
    prob_arr = prob_matrix(x,means,stds)
    if save_fig == 'Yes':
        name = plt_file_name(path,'prob',bet,x)
    else:
        name = ''
    title = title_maker('prob',bet,x)
    make_fig(prob_arr,title,name,'prob',save_fig,x)

#Function that is activated by the GUI to present average winnings plots    
def avg_plt():
    bet = str(bet_type.get())
    save_fig = str(save.get())
    means = open_csv(file_map[bet][0])
    title = title_maker('avg',bet)
    if save_fig == 'Yes':
        fig_name = plt_file_name(path,'avg',bet)
    else:
        fig_name = ''
    title = title_maker('avg',bet)
    make_fig(means,title,fig_name,'avg',save_fig)

#Displays when user clicks the help button. Gives directions on how to use GUI
help_str = """
Reading Average Plots:
    x-axis represents how much is bet each round, starting with $100.
    y-axis represents how many rounds are played.
    Use color bar to find value at given point on plot. This value
    represents the average amount remaining after the number of games (y-axis)
    with a certain wager(x-axis)

Reading Probability Plots:
    Before using creating plot, an INTEGER value must be entered into the entry box.
    The program will calculate probabilities of winning the entered amount or more.
    x-axis represents how much is bet each round, starting with $100.
    y-axis represents how many rounds are played.
    Use color bar to find value at given point on plot. This value represents
    the probability, with 1 being 100% and 0 being 0%
    
Save Plot:
    Selecting yes will automatically save any generated plots with 
    auto-generated name.
    For average bets names go as: payout type_avg.png
    For probability plots names go as: payout type_prob_amount entered 
    used to calculate probabilities.
    """

#Presents help message when button is clicked
def help_window():
    color='PeachPuff2'
    wind =tk.Tk()
    can = tk.Canvas(wind, width = 650, height =400, bg =color)
    can.pack()
    
    label = tk.Label(wind,text = help_str)
    label.config(font=('Verdana', 10),bg=color)
    can.create_window(325,200, window=label)
    
    wind.mainloop()

"""
Code for GUI layout, text and buttons. 
"""
root = tk.Tk()

root.title('Roulette')

color='PeachPuff2'

main = tk.Canvas(root, width = 600, height = 600,bg=color)
main.pack()

label1 = tk.Label(root, text='Roulette Statistics')
label1.config(font=('Verdana', 25),bg=color)
main.create_window(300,25, window=label1)

label2 = tk.Label(root, text='Starting with $100')
label2.config(font=('Verdana', 12),bg=color)
main.create_window(300,50, window=label2)

help_but = tk.Button(root,text ='?',height=1,width= 2,bg='firebrick1',command = help_window)
main.create_window(590,15,window=help_but)

bet_type = StringVar(root)
bet_type.set("1:1 Payout")

bet_label = tk.Label(root, text = 'Bet Type:')
bet_label.config(font=('Verdana',15),bg=color)
main.create_window(200,125, window=bet_label)

bet_opt = OptionMenu(root, bet_type,'1:1 Payout','2:1 Payout','5:1 Payout','6:1 Payout','8:1 Payout',
                     '11:1 Payout','17:1 Payout','35:1 Payout',)
bet_opt.config(font=('Verdana', 10))
main.create_window(400,125, window=bet_opt)

save = StringVar(root)
save.set('No')

save_label = tk.Label(root, text = 'Save Plot?')
save_label.config(font=('Verdana',15),bg=color)
main.create_window(200,175, window=save_label)

save_opt = OptionMenu(root,save,'Yes','No')
save_opt.config(font=('Verdana', 10))
main.create_window(400,175, window=save_opt)

prob_label = tk.Label(root,text='Select Amount To View Probabilities')
prob_label.config(font=('Verdana', 18),bg=color)
main.create_window(300,250,window=prob_label)

amnt_label =tk.Label(root,text='Probability of \nleaving with at least $')
amnt_label.config(font=('Verdana', 12),bg=color)
main.create_window(200,300,window=amnt_label)

amnt = tk.Entry(root)
main.create_window(400,300,window=amnt)

prob_button = tk.Button(root,text='Create Probability Plot', height=3,width= 30,command = prob)
main.create_window(300,375,window=prob_button)

avg_label = tk.Label(root, text='View average winnings')
avg_label.config(font=('Verdana', 18),bg=color)
main.create_window(300,450, window=avg_label)

avg_button = tk.Button(root,text='Create Average Winnings Plot', height=3,width= 30,command = avg_plt)
main.create_window(300,525,window=avg_button)


root.mainloop()
