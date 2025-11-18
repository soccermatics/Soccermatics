# -*- coding: utf-8 -*-
# importing necessary libraries
import pandas as pd
import numpy as np
import json
# plotting
import matplotlib.pyplot as plt
from mplsoccer import VerticalPitch
# statistical fitting of models
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os
import pathlib

train = pd.DataFrame()
for i in range(13):
    file_name = 'events_England_' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve().parents[1]), 'data', 'Wyscout', file_name)
    with open(path) as f:
        data = json.load(f)
    train = pd.concat([train, pd.DataFrame(data)])

shots = train.loc[train["eventName"] == "Shot"]

#headers have id = 403
headers = shots.loc[shots.apply (lambda x:{'id':403} in x.tags, axis = 1)]
non_headers = shots.drop(headers.index)

#making a function for data transformation
def prepare_data(shots):
    """
    function that returns a dataframe of shots to fit logistic regression
    - inputs - shots - a dataframe of shots
    - returns - shots - a dataframe of shots with extra columns
    """
    
    shots["X"] = shots.positions.apply(lambda cell: (100 - cell[0]['x']) * 105/100)
    shots["Y"] = shots.positions.apply(lambda cell: cell[0]['y'] * 68/100)
    shots["C"] = shots.positions.apply(lambda cell: abs(cell[0]['y'] - 50) * 68/100)
    #calculate distance and angle 
    shots["Distance"] = np.sqrt(shots["X"]**2 + shots["C"]**2)
    shots["Angle"] = np.where(np.arctan(7.32 * shots["X"] / (shots["X"]**2 + shots["C"]**2 - (7.32/2)**2)) > 0, np.arctan(7.32 * shots["X"] /(shots["X"]**2 + shots["C"]**2 - (7.32/2)**2)), np.arctan(7.32 * shots["X"] /(shots["X"]**2 + shots["C"]**2 - (7.32/2)**2)) + np.pi)
    #if you ever encounter problems (like you have seen that model treats 0 as 1 and 1 as 0) while modelling - change the dependant variable to object 
    shots["Goal"] = shots.tags.apply(lambda x: 1 if {'id':101} in x else 0)
    return shots

headers = prepare_data(headers)
non_headers = prepare_data(non_headers)

#fitting models 
#headers
headers_model = smf.glm(formula="Goal ~ Distance + Angle" , data=headers, 
                           family=sm.families.Binomial()).fit()
print(headers_model.summary())
#non-headers
nonheaders_model = smf.glm(formula="Goal ~ Distance + Angle" , data=non_headers, 
                           family=sm.families.Binomial()).fit()
print(nonheaders_model.summary())

#assigning xG
#headers
b_head = headers_model.params
xG = 1/(1+np.exp(-(b_head[0]+b_head[1]*headers['Distance'] + b_head[2]*headers['Angle']))) 
headers = headers.assign(xG = xG)

#non-headers 
b_nhead = nonheaders_model.params
xG = 1/(1+np.exp(-(b_nhead[0]+b_nhead[1]*non_headers['Distance'] + b_nhead[2]*non_headers['Angle']))) 
non_headers = non_headers.assign(xG = xG)

#2
penalties = train.loc[train["subEventName"] == "Penalty"]
penalties = penalties.assign(xG = 0.8)

#3
#put dataframes together 
all_shots_xg = pd.concat([non_headers[["playerId", "xG"]], headers[["playerId", "xG"]], penalties[["playerId", "xG"]]])
#group by player and sum 
xG_sum = all_shots_xg.groupby(["playerId"])["xG"].sum().sort_values(ascending = False).reset_index()

#check this player name in Wyscout database
path = os.path.join(str(pathlib.Path().resolve().parents[1]), 'data', 'Wyscout', 'players.json')
with open(path) as f:
    data = json.load(f)
players_df = pd.DataFrame(data)

players_df["playerId"] = players_df["wyId"]

summary = xG_sum.merge(players_df[["playerId", "shortName"]], how = "inner", on = ["playerId"])
