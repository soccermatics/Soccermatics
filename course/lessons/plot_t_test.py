"""
Z and t-tests
=========================================
In this tutorial we demonstrate how to check if values are significantly different from each other 
using z-tests and t-tests
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
# First we open the data. For this example we will use WyScout data from 2017/18 Premier League season.  To meet file size requirements of 
# Github, we have to open it from different files,
# but you can open the file locally from the directory you saved it in. Also, we open the file containing all teams in WyScout database.

#open events
train = pd.DataFrame()
for i in range(13):
    file_name = 'events_England_' + str(i+1) + '.json'
    path = os.path.join(str(pathlib.Path().resolve()), 'data', 'Wyscout', file_name)
    with open(path) as f:
        data = json.load(f)
    train = pd.concat([train, pd.DataFrame(data)])
    
#open team data
path = os.path.join(str(pathlib.Path().resolve()),"data", 'Wyscout', 'teams.json')
with open(path) as f:
    teams = json.load(f)

teams_df = pd.DataFrame(teams)
teams_df = teams_df.rename(columns={"wyId": "teamId"})
    
##############################################################################
# Preparing the dataset
# ----------------------------
#
# First, we take out corners. Then, we sum them by team. We also merge it together with team dataframe to keep their names.
# Then we repeat the same, but calculate corners taken by each team per game. 
    
#get corners
corners = train.loc[train["subEventName"] == "Corner"]
#count corners by team
corners_by_team = corners.groupby(['teamId']).size().reset_index(name='counts')
#merge with team name
summary = corners_by_team.merge(teams_df[["name", "teamId"]], how = "left", on = ["teamId"])
#count corners by team by game
corners_by_game = corners.groupby(['teamId', "matchId"]).size().reset_index(name='counts')
#merge with team name
summary2 = corners_by_game.merge(teams_df[["name", "teamId"]], how = "left", on = ["teamId"])



##############################################################################
# Two-sided z-test
# ----------------------------
#
# We use two-sided z-test to check if Manchester City take 8 corners per game. We set the significance level at 0.05.
# At this significance level, there's no reason to reject the null hypothesis. Therefore, we claim that City takes
# 8 corners per game.

from statsmodels.stats.weightstats import ztest

#get city corners
city_corners = summary2.loc[summary2["name"] == 'Manchester City']["counts"]

#test 
t, pvalue = ztest(city_corners,  value=8)
#checking outcome
if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Manchester City do not take 8 corners per game")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Manchester City take 8 corners per game")

##############################################################################
# One-sided z-test
# ----------------------------
#
# We use one-sided z-test to check if Manchester City take more than 6 corners per game. We set the significance level at 0.05.
# At this significance level, we reject the null hypothesis. Therefore, we claim that City takes
# more than 6 corners per game.

t, pvalue = ztest(city_corners,  value=6, alternative = "larger")
if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Manchester City take more than 6 corners per game")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Manchester City do not take 6 more corners per game")

##############################################################################
# One-sample two-sided t-test
# ----------------------------
#
# We use one-sample t-test to check if Leicester City take different number of corners than the league average. We set the significance level at 0.05.
# At this significance level, there's no reason to reject the null hypothesis. Therefore, we claim that Leicester City take
# more than 6 corners per game. 

mean = summary["counts"].mean()
std = summary["counts"].std()


from scipy.stats import ttest_1samp
leicester_corners = summary.loc[summary["name"] == "Leicester City"]["counts"].iloc[0]
t, pvalue = ttest_1samp(summary["counts"], leicester_corners)

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Leicester City do not take average number of corners than league average")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Leicester City take average number of corners than league average")

##############################################################################
# One-sample one-sided t-test
# ----------------------------
#
# We use one-sample t-test to check if Arsenal took more number of corners than the league average. We set the significance level at 0.05.
# At this significance level, we reject the null hypothesis. Therefore, we claim that Arsenal take
# more than 6 corners per game. 

from scipy.stats import ttest_1samp
arsenal_corners = summary.loc[summary["name"] == "Arsenal"]["counts"].iloc[0]
t, pvalue = ttest_1samp(summary["counts"], arsenal_corners, alternative='less')

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Arsenal take more corners than league average")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Arsenal do not take more corners than league average")


##############################################################################
# Two-sample two-sided t-test
# ----------------------------
#
# We use two-sample t-test to check if Liverpool took different number of corners per game than the league average. We set the significance level at 0.05.
# At this significance level, there is no reason to reject the null hypothesis. Therefore, we claim that Liverpool took
# the same number of corners as United. 

#check if united takes the same average number of corners per game as liverpool
liverpool_corners = summary2.loc[summary2["name"] == 'Liverpool']["counts"]
united_corners = summary2.loc[summary2["name"] == 'Manchester United']["counts"]

from scipy.stats import ttest_ind
t, pvalue  = ttest_ind(a=liverpool_corners, b=united_corners, equal_var=True)

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - Liverpool took different number of corners per game than United")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - Liverpool took the same number of corners per game as United")


##############################################################################
# Two-sample one-sided t-test
# ----------------------------
#
# We use two-sample t-test to check if Manchester City took more corners per game than Newcastle. We set the significance level at 0.05.
# At this significance level, we reject the null hypothesis. Therefore, we claim that City took
# more corners than Newcastle. 

city_corners = summary2.loc[summary2["name"] == 'Manchester City']["counts"]
castle_corners = summary2.loc[summary2["name"] == 'Newcastle United']["counts"]

from scipy.stats import ttest_ind
t, pvalue  = ttest_ind(a=city_corners, b=castle_corners, equal_var=True, alternative = "greater")

if pvalue < 0.05:
    print("P-value amounts to", pvalue, "- We reject null hypothesis - City took more corners per game than Newcastle")
else:
    print("P-value amounts to", pvalue, " - We do not reject null hypothesis - City did not  take the more corners per game than Newcastle")


