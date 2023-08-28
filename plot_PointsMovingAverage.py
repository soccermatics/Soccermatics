"""
Points Moving Average
=====================
Investigate Points Moving Average
"""


#importing necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

##############################################################################
# Downloading data
# ----------------------------
# For our task we will download the data from `Football-Data <https://football-data.co.uk/>`_ with match scores from 
# the English Premier League since Pep Guardiona began to coach Manchester City. Here, we download the data, save it in 
# a dataframe and append to list and then store them in one big dataframe.

#list of dataframes
dflist = []
#list of all seasons, we'll use them later
seasonst = []
#taking to last year because United hasn't played yet when I'm doing this code
for year in range(16,22,1):
    #create a string with season name
    if year<9:
        yeartext='0'+str(year)+'0'+str(year+1)
        yeartext2='0'+str(year)+'-0'+str(year+1)
    elif year==9:
        yeartext='0910'
        yeartext2='09-10'
    else:
        yeartext=str(year)+str(year+1)
        yeartext2=str(year)+'-'+str(year+1)
    #get data from webpage
    performance_year = pd.read_csv("https://www.football-data.co.uk/mmz4281/"+yeartext+"/E0.csv",delimiter=',') 
    #append season name
    seasonst.append(yeartext2)
    #make list of dataframes
    dflist.append(performance_year)
#put dataframes into one big
performance = pd.concat(dflist).reset_index()

##############################################################################
# Preparing data
# ----------------------------
# We want to investigate Pep Guardiola's City performance against other TOP6 clubs performance in this period.
# For each of these teams, we get games played by them and assign number of points that they scored. Then, we calculate
# the 10 game points rolling average. Feel free to experiment with window size and check how the diagram changes!  

#top6 teams
teams = ['Man City', 'Liverpool', 'Arsenal', 'Chelsea', 'Tottenham', 'Man United']

#dictionary to store data
team_dfs = dict()
for team in teams:
    #empty dataframe
    team_df = pd.DataFrame(columns = ["Points", "Date", "Game"])
    #get matches by this team 
    matches = performance.loc[(performance['AwayTeam'] == team) | (performance['HomeTeam'] == team)]
    #auxilliary variable that will be helpful to plot
    game = 0
    for i, match in matches.iterrows():
        game +=1
        #if team was away
        if match['AwayTeam'] == team:
            #get goals for both teams 
            goalsfor = match['FTAG']
            goalsagainst = match['FTHG']
            #assign 3 points if win, 1 if draw, 0 if lost
            if match['FTR'] == 'A':
                points = 3
            elif match['FTR'] == 'D':
                points = 1
            else:
                points = 0
        else:
            #geat goals for both teams
            goalsfor = match['FTHG']
            goalsagainst = match['FTAG']
            #assign 3 points if win, 1 if draw, 0 if lost
            if match['FTR'] == 'H':
                points = 3
            elif match['FTR'] == 'D':
                points = 1      
            else:
                points = 0
                #assign value to dataframe
        team_df.at[i, "Points"] = points
        team_df.at[i, "Game"] = game
    #calculate rolling average   
    team_df['PointsRA'] = team_df['Points'].rolling(window=10, win_type='triang').mean()
    #append df
    team_dfs[team] = team_df


##############################################################################
# Making plot
# ----------------------------
# After calculating the rolling average, we can plot our data. Make sure that you understand the lines below!

#create plot 
fig, ax = plt.subplots(figsize=(20, 8))
#arsenal got yellow because of those 2004 kits, but it was invisible so they got green  
colors = ['blue', 'red', 'green', 'blue', 'grey', 'darkred']
#city highlighted more
alphas = [1, 0.2, 0.2, 0.2, 0.2, 0.2]
for club, color, alpha in zip(teams, colors, alphas):
    ax.plot(team_dfs[club]['Game'],  team_dfs[club]['PointsRA'], linewidth=2, linestyle='-',color=color, alpha = alpha, zorder = 2, label = club)

#set title
ax.set_title("Man City since Guardiola's arrival - 10 game rolling average points comparing to TOP 6 clubs", fontsize = 24, pad=20)
#make visible ticks for beginning of each season
ax.set_xticks(np.arange(0, max(team_dfs["Liverpool"]['Game']) + 38, 38))
#no text
ax.set_xticklabels([])
#make ticks in the middle
ax.set_xticks(np.arange(0, max(team_dfs["Liverpool"]['Game']), 38) + 19, minor=True)
#put season text in the middle of season
ax.set_xticklabels(seasonst, minor=True)
#set axis limits
ax.set_xlim(0, max(team_dfs["Liverpool"]['Game']) + 10)
ax.set_ylim(-0.1,3.2)
#disable black ticks, but big text xaxis
ax.tick_params(axis='x', color='white', which='both', labelsize = 20)
#grey y ticks
ax.tick_params(axis='y', color='grey', labelsize = 14)
#add grid
ax.grid(zorder = 1, linestyle = "--", alpha = 0.5)
#disable spines
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
#add axis labels
ax.set_ylabel('Rolling Average Points Per Game', fontsize = 16,labelpad=10)
ax.set_xlabel('Season', fontsize = 24, labelpad=10)
#make legend
plt.legend(bbox_to_anchor=(1.0, 0.5), loc="center left",fontsize=16, edgecolor='white')
plt.show()

##############################################################################
# Challenge
# ----------------------------
# 1. Improve so that the rolling average is calculated for each season independently!
# 2. Make this plot for Norwich and account for their relegations!