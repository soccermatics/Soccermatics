"""
Using Statsbomb
=====================
Getting familiar with Statsbomb data
"""

#importing SBopen class from mplsoccer to open the data
from mplsoccer import Sbopen
# The first thing we have to do is open the data. We use a parser SBopen available in mplsoccer.
parser = Sbopen()

##############################################################################
# Competition data
# ----------------------------
# Using method *competition* of the parser we can explore competitions to find the competition we are interested in.
# The most important information for us is in the *competition_id* (id of competition) and *season_id*.
# The first one is the key in Statsbomb database of a competition, the second one of a season 
# of this competition (for example WC 2018 would have a different *season_id* than WC 2014, but the same *competition_id*).

#opening data using competition method
df_competition = parser.competition()
#structure of data
df_competition.info()



##############################################################################
# Match data
# ----------------------------
# Using method *match* of the parser we can explore matches of a competition to find the match we are interested in.
# To open it we need to know the *competition_id* (id of competition) and *season_id*.
# We know that for Women World Cup *competition_id* is 72 and *season_id* is 30
# From this dataframe for us the most important imformation is provided in *match_id*, 
# *home_team_id* and *home_team_name* and adequately *away_team_id* and *away_team_name*.

#opening data using match method
df_match = parser.match(competition_id=72, season_id=30)
#structure of data
df_match.info()



##############################################################################
# Lineup data
# ----------------------------
# To check the lineups we use the *lineup* method. We do it for England Sweden WWC 2019 game - *game_id* is 69301 
# - you can check that in the df_match. In this dataframe you will find all players who played in this game, their teams 
# and jersey numbers
# COMMENTED OUT BECAUSE OF CHANGE OF DATA FORMAT.

#opening data using match method
#df_lineup = parser.lineup(69301)
#structure of data
#df_lineup.info()

##############################################################################
# Event data
# ----------------------------
# The Statsbomb data that we will use the most during the course is event data. 
# Knowing *game_id* you can open all the events that occured on the pitch
# In the event dataframe you will find events with additional information, we will mostly use this dataframe.
# Tactics dataframe provides information about player position on the pitch. 'Related' dataframe provides information
# on events that were related to each other - for example ball pass and pressure applied. *df_freeze* consists of freezed
# frames with player position in the moment of shots. We will learn more about tracking data later in the course.
# Below, an example of event data is presented.

#opening data
df_event, df_related, df_freeze, df_tactics = parser.event(69301)
#if you want only event data you can use 
#df_event = parser.event(69301)[0]
#structure of data
df_event.info()

##############################################################################
# 360 data
# ----------------------------
# Statsbomb offers 360 data which track not only location of an event but also players' location. To open them we need
# an id of game. Later, we will also need id of the event. In the *df_frame* we find information on players' position (but only if teammate, not all information)
# and in *df_visible* it is provided which part of the pitch was tracked during an event.

df_frame, df_visible = parser.frame(3788741)

# exploring the data
df_frame.info()


##############################################################################
# Before you start
# ----------------------------
# Run these lines in Spyder/Jupyter notebook and explore dataframes 
# to get more familiar before you start working on the course.