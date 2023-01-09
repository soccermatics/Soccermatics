"""
Sign test
=========================================
In this tutorial we demonstrate how to check equal size of two samples using the sign test. To do so, we provide an example
in which we check if Heung-Min Son shoots with both feet the same number of times. 
"""
import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
#opening data
import os
import pathlib
import warnings

pd.options.mode.chained_assignment = None
warnings.filterwarnings('ignore')

##############################################################################
# Opening the dataset
# ----------------------------
#
# First we open the data. For this example we will use WyScout data from 2017/18 Premier League season.  To meet file size requirements of Github, we have to open it from different files,
# but you can open the file locally from the directory you saved it in. Also, we open the file containing all players in WyScout database.

#open event data
train = pd.DataFrame()
for i in range(13):
    file_name = 'events_England_' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve().parents[0]), 'data', 'Wyscout', file_name)
    with open(path) as f:
        data = json.load(f)
    train = pd.concat([train, pd.DataFrame(data)])
    
    path = os.path.join(str(pathlib.Path().resolve().parents[0]),"data", 'Wyscout', 'players.json')

#open dataset with players
with open(path) as f:
    players = json.load(f)
player_df = pd.DataFrame(players)

##############################################################################
# Preparing the dataset
# ----------------------------
#
# First, we filter the events to only keep shots. Then, we check for Son's id in the player database. As the next step,
# we keep shots made by him. Then, we look for the shots made with his left (ones with *id* = 401) and right (ones with *id* = 401) foot.
# In the end, we create a list with ones for shots with his left foot and -1 for shots with his right foot.

#take shots only
shots = train.loc[train['subEventName'] == 'Shot'] 
#look for son's id
son_id = player_df.loc[player_df["shortName"] == "Son Heung-Min"]["wyId"].iloc[0]
#get son's shot
son_shots = shots.loc[shots["playerId"] == son_id]

#left leg shots
lefty_shots = son_shots.loc[son_shots.apply (lambda x:{'id':401} in x.tags, axis = 1)]
#right leg shots
righty_shots = son_shots.loc[son_shots.apply (lambda x:{'id':402} in x.tags, axis = 1)]

#create list with ones for left foot shots and -1 for right foot shots   
l = [1] * len(lefty_shots) 
l.extend([-1] * len(righty_shots))

##############################################################################
# Testing the hypothesis
# ----------------------------
#
# Now we can test the hypothesis that Heung-Min Son is indeed ambidextrous. To do so, a `sign test <https://en.wikipedia.org/wiki/Sign_test>`_ is used.
# We set the significance level at 0.05. After conducting the hypothesis, there's no reason to reject the null hypothesis. Therefore, we claim that
# Son shoots with his right and left foot the same number of times.

from statsmodels.stats.descriptivestats import sign_test
test = sign_test(l, mu0 = 0)
pvalue = test[1]

if pvalue < 0.05:
    print("P-value amounts to", str(pvalue)[:5], "- We reject null hypothesis - Heung-Min Son is not ambidextrous")
else:
    print("P-value amounts to", str(pvalue)[:5], " - We do not reject null hypothesis - Heung-Min Son is ambidextrous")


