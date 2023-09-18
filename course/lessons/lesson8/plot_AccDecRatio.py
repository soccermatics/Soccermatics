"""
Calculate distance-based metrics for player fitness
=========================================
In this tutorial we will calculate distance-based metrics for player fitness. 
The code is based on Sudarshan "Suds" Gopaladesikan's 
`code <https://github.com/slbenfica1079/sportsdatascience>`_


The code here is commented out, because it takes too long to run on the readthedocs server.

"""

# #importing necessary libraries 
# import Metrica_IO as mio
# import Metrica_Velocities as mvel
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
# import ruptures as rpt
# import statsmodels.formula.api as smf
# import scipy as sp
# import warnings
# warnings.filterwarnings("ignore")
# pd.options.mode.chained_assignment = None  


##############################################################################
# Opening data
# ----------------------------
# For this task we will use Metrica data. 
# We make separate dataframes for home and away teams as well as for events.
# Then we adjust the direction so the teams attack the same direction for both halves.

#Change data directory #add to description where you can put the Metrica data

# DATADIR = '../data/Metrica'
# game_id = 2  # let's look at sample match 2

# # read in the event data
# events = mio.read_event_data(DATADIR, game_id)

# # read in tracking data
# tracking_home = mio.tracking_data(DATADIR, game_id, 'Home')
# tracking_away = mio.tracking_data(DATADIR, game_id, 'Away')

# # Convert positions from metrica units to meters (note change in Metrica's coordinate system since the last lesson)
# tracking_home = mio.to_metric_coordinates(tracking_home)
# tracking_away = mio.to_metric_coordinates(tracking_away)
# events = mio.to_metric_coordinates(events)

# # reverse direction of play in the second half so that home team is always attacking from right->left
# tracking_home, tracking_away, events = mio.to_single_playing_direction(tracking_home, tracking_away, events)

# GK_numbers = [mio.find_goalkeeper(tracking_home),mio.find_goalkeeper(tracking_away)]
# home_attack_direction = mio.find_playing_direction(tracking_home,'Home') # 1 if shooting left-right, else -1

##############################################################################
# Calculating player velocities
# ----------------------------
# Here we calculate Home player 5 velocities both unsmoothed and smoothed. 
# As the next step we plot both of them to show advantages of smoothing the velocity.
# if we calculate the speed of a player from the camera. Also it is assumed that a 
# football player should not run faster than 12 m/s.

# # Calculate the Player Velocities 
# player_ids = np.unique(list(c[:-2] for c in tracking_home.columns if c[:4] in ['Home', 'Away']))
# #impossible to run faster than 12 m/s
# maxspeed = 12
# dt = tracking_home['Time [s]'].diff()
# #get first frame of second half
# second_half_idx = tracking_home.Period.idxmax()

# tracking_home_unsmoothed = mvel.calc_player_velocities(tracking_home, smoothing=False)
# tracking_away_unsmoothed = mvel.calc_player_velocities(tracking_away, smoothing=False)

# fig, ax = plt.subplots(2, figsize=(24, 16))
# ax[0].plot(range(1, 3001), tracking_home_unsmoothed.loc[1:3000]['Home_5_speed'], color = "blue")
# ax[0].set_title('Unsmoothed Velocities', fontsize = 20)
# ax[0].set_ylabel('Velocity (m/s)', fontsize = 16)
# ax[0].set_xlabel('Time (s)', fontsize = 16)
# ax[0].set_xticklabels([(i-1)*0.5 for i in range(8)])
# unsmoothed_vel = tracking_home_unsmoothed.loc[1:9000]['Home_5_speed']
# ax[0].tick_params(axis='both', which='major', labelsize=12)
# # Using Laurie's smoothing code

# tracking_home = mvel.calc_player_velocities(tracking_home, smoothing=True)
# tracking_away = mvel.calc_player_velocities(tracking_away, smoothing=True)

# ax[1].plot(range(1, 3001), tracking_home.loc[1:3000]['Home_5_speed'], color = "blue")
# ax[1].set_title('Smoothed Velocities', fontsize = 20)
# ax[1].set_ylabel('Velocity (m/s)', fontsize = 16)
# ax[1].set_xlabel('Time (s)', fontsize = 16)
# ax[1].set_xticklabels([(i-1)*0.5 for i in range(8)])
# ax[1].tick_params(axis='both', which='major', labelsize=12)
# #tracking_home.loc[1:67941][['Home_5_speed']].boxplot().set_title('Smoothed Velocities (Home_5)')

# fig.suptitle('Home_5 Velocities', fontsize = 28)
# plt.show()

##############################################################################
# Calculating total distance covered by team players
# ----------------------------
# To calculate distance covered by each player we calculate the sum of distances covered between one 
# frame and the following one. We also check which players didn't play
# the entire game. Then we make a plot. Star means that the player was either subbed in or subbed off during the game

# # get home players
# home_players = np.unique(list(c.split('_')[1] for c in tracking_home.columns if c[:4] == 'Home'))
# home_summary = pd.DataFrame(index=home_players)

# #calculating minutes played
# minutes_home = []
# for player in home_players:
#     # search for first and last frames that we have a position observation for each player (when a player is not on the pitch positions are NaN)
#     column = 'Home_' + player + '_x' # use player x-position coordinate
#     player_minutes = (tracking_home[column].last_valid_index() - tracking_home[column].first_valid_index() + 1) / 25 / 60. # convert to minutes
#     minutes_home.append( player_minutes )
# home_summary['Minutes Played'] = minutes_home
# home_summary = home_summary.sort_values(['Minutes Played'], ascending=False)

# #calculating distance covered
# distance_home = []
# for player in home_summary.index:
#     column = 'Home_' + player + '_speed'
#     player_distance = tracking_home[
#                           column].sum() / 25. / 1000  # this is the sum of the distance travelled from one observation to the next (1/25 = 40ms) in km.
#     distance_home.append(player_distance)
# home_summary['Distance [km]'] = distance_home

# #get away players
# away_players = np.unique(list(c.split('_')[1] for c in tracking_away.columns if c[:4] == 'Away'))
# away_summary = pd.DataFrame(index=away_players)

# #calculating minutes played
# minutes_away = []
# for player in away_players:
#     # search for first and last frames that we have a position observation for each player (when a player is not on the pitch positions are NaN)
#     column = 'Away_' + player + '_x' # use player x-position coordinate
#     player_minutes = (tracking_away[column].last_valid_index() - tracking_away[column].first_valid_index() + 1 ) / 25 / 60. # convert to minutes
#     minutes_away.append( player_minutes )
# away_summary['Minutes Played'] = minutes_away
# away_summary = away_summary.sort_values(['Minutes Played'], ascending=False)

# #calculating distance covered
# distance_away = []
# for player in away_summary.index:
#     column = 'Away_' + player + '_speed'
#     player_distance = tracking_away[
#                           column].sum() / 25. / 1000  # this is the sum of the distance travelled from one observation to the next (1/25 = 40ms) in km.
#     distance_away.append(player_distance)
# away_summary['Distance [km]'] = distance_away

# home_summary['Team'] = 'Home'
# away_summary['Team'] = 'Away'

# #create summary dataframe to make a plot 
# game_summary = pd.concat([home_summary, away_summary])
# game_summary['isSub'] = np.where(game_summary['Minutes Played']== max(game_summary['Minutes Played']),0,1)
# game_summary_sorted = game_summary.sort_values(['Team', 'Distance [km]'], ascending=[False, False])
# game_summary_sorted['Player'] = game_summary_sorted.index
# #star mean that player was subbed in or of
# game_summary_sorted['Player'] = np.where(game_summary_sorted['isSub']==0, game_summary_sorted['Player'], game_summary_sorted['Player']+'*')

# #make plot
# colors = ['red' for _ in range(len(home_summary))]
# colors.extend(['blue' for _ in range(len(away_summary))])
# color_map = {'Home':'red', 'Away':'blue'}         
# labels = list(color_map.keys())
# handles = [plt.Rectangle((0,0),1,1, color=color_map[label]) for label in labels]

# plt.figure(figsize=(10,5))
# plt.bar(game_summary_sorted['Player'], game_summary_sorted['Distance [km]'], color=colors)
# plt.xlabel("Player", fontsize = 14)
# plt.ylabel("Distance [km]", fontsize = 14)
# plt.title("Distance covered by each player", fontsize = 20)
# plt.legend(handles, labels)
# plt.show()


##############################################################################
# Calculating total distance covered by team players
# ----------------------------
# The next step that can be done is to calculate distance covered at various velocity bands. We define walking as covering space with velocity 0-2 m/s, jogging
# as maintaining speed between 2-4 m/s. Running is defined as velocity between 4 and 7 m/s and sprinting is not less than 7 m/s. However, our assumption that 
# a football player can't run faster than 12 m/s still holds. Distance at each velocity is calculated the same way as in previous example.

# walking = []
# jogging = []
# running = []
# sprinting = []
# for player in home_summary.index:
#     column = 'Home_' + player + '_speed'
#     # walking (less than 2 m/s)
#     player_distance = tracking_home.loc[tracking_home[column] < 2, column].sum() / 25. / 1000
#     walking.append(player_distance)
#     # jogging (between 2 and 4 m/s)
#     player_distance = tracking_home.loc[
#                           (tracking_home[column] >= 2) & (tracking_home[column] < 4), column].sum() / 25. / 1000
#     jogging.append(player_distance)
#     # running (between 4 and 7 m/s)
#     player_distance = tracking_home.loc[
#                           (tracking_home[column] >= 4) & (tracking_home[column] < 7), column].sum() / 25. / 1000
#     running.append(player_distance)
#     # sprinting (greater than 7 m/s)
#     player_distance = tracking_home.loc[tracking_home[column] >= 7, column].sum() / 25. / 1000
#     sprinting.append(player_distance)

# home_summary['Walking'] = walking
# home_summary['Jogging'] = jogging
# home_summary['Running'] = running
# home_summary['Sprinting'] = sprinting


# ax = home_summary[['Walking','Jogging','Running','Sprinting']].plot.bar(colormap='coolwarm', figsize=(10, 5))
# ax.set_xlabel('Player', fontsize = 14)
# ax.set_ylabel('Distance covered [km]', fontsize = 14)
# ax.set_title('Distance Covered At Various Velocity Bands - Home Team', fontsize = 16)
# plt.show()

##############################################################################
# Calculating acceleration/deceleration ratio
# ----------------------------
# To calculate player acceleration deceleration ratio we need an information about their accelerations. We define a high acceleration as one where player exceeded
# 2 m/s2. Also, a footballer can't accelerate faster than 6 m/.s2. 
# Then we calculate ratio of high accerelations to high decelerations which took more than 0.75 s. for each player. As the last step we plot it together with covered distance by player.

# maxacc = 6
# home_acc_dict = {}

# for player in home_players:
#     #calculate acceleration
    
#     tracking_home['Home_' + player + '_Acc'] = tracking_home['Home_' + player + '_speed'].diff() / dt
#     #set acceleration condition
#     tracking_home['Home_' + player + '_Acc'].loc[np.absolute(tracking_home['Home_' + player + '_Acc']) > maxacc] = np.nan
#     ##check if acceleration was high or low
#     tracking_home['Home_' + player + '_Acc_type'] = np.where(np.absolute(tracking_home['Home_' + player + '_Acc']) >= 2,
#                                                              "High", "Low")
#     tracking_home['Home_' + player + '_Acc_g'] = tracking_home['Home_' + player + '_Acc_type'].ne(
#         tracking_home['Home_' + player + '_Acc_type'].shift()).cumsum()
    
#     #for each player
#     for g in np.unique(tracking_home['Home_' + player + '_Acc_g']):
#         acc_temp = tracking_home[tracking_home['Home_' + player + '_Acc_g'] == g]
#         if acc_temp['Home_' + player + '_Acc_type'].iloc[0] == 'High':
#             #get the acceleration period
#             acc_duration = round(max(acc_temp['Time [s]']) - min(acc_temp['Time [s]']), 2)
#             #check if it was acceleration or deceleration
#             acc_or_dec = np.where(np.mean(acc_temp['Home_'+player+'_Acc']) > 0, "Acc", "Dec")
#             #create a dictionary
#             home_acc_dict[len(home_acc_dict) + 1] = {'Player': player, 'Group': g, 'Duration': acc_duration,
#                                                      'Type': acc_or_dec}

# home_acc_df = pd.DataFrame.from_dict(home_acc_dict,orient='index')
# #get accelerations that were longer than 0.75 sec
# home_acc_df1 = home_acc_df[home_acc_df['Duration']>=.75]

# #repeat for away team
# away_acc_dict = {}
# for player in away_players:
#     tracking_away['Away_' + player + '_Acc'] = tracking_away['Away_' + player + '_speed'].diff() / dt
#     tracking_away['Away_' + player + '_Acc'].loc[np.absolute(tracking_away['Away_' + player + '_Acc']) > maxacc] = np.nan
#     tracking_away['Away_' + player + '_Acc_type'] = np.where(np.absolute(tracking_away['Away_' + player + '_Acc']) >= 2,
#                                                              "High", "Low")
#     tracking_away['Away_' + player + '_Acc_g'] = tracking_away['Away_' + player + '_Acc_type'].ne(
#         tracking_away['Away_' + player + '_Acc_type'].shift()).cumsum()

#     for g in np.unique(tracking_away['Away_' + player + '_Acc_g']):
#         acc_temp = tracking_away[tracking_away['Away_' + player + '_Acc_g'] == g]
#         if acc_temp['Away_' + player + '_Acc_type'].iloc[0] == 'High':
#             acc_duration = round(max(acc_temp['Time [s]']) - min(acc_temp['Time [s]']), 2)
#             acc_or_dec = np.where(np.mean(acc_temp['Away_'+player+'_Acc']) > 0, "Acc", "Dec")
#             away_acc_dict[len(away_acc_dict) + 1] = {'Player': player, 'Group': g, 'Duration': acc_duration,
#                                                      'Type': acc_or_dec}

# away_acc_df = pd.DataFrame.from_dict(away_acc_dict,orient='index')
# away_acc_df1 = away_acc_df[away_acc_df['Duration']>=.75]


# #calculate ratio for each player fo the home team
# accdec = []
# for player in home_players:
#     accs = home_acc_df1[(home_acc_df1['Player']==player) & (home_acc_df1['Type']=='Acc')].count()[0]
#     decs = home_acc_df1[(home_acc_df1['Player']==player) & (home_acc_df1['Type']=='Dec')].count()[0]
#     ac_ratio = accs / decs
#     accdec.append(ac_ratio)
# #saving it in a dataframe
# home_summary['AccDec'] = accdec

# #making a plot
# fig, ax = plt.subplots(figsize=(12, 8))
# ax.scatter(home_summary['Distance [km]'], home_summary['AccDec'], color = "red", s = 50)
# for i in home_summary.index:
#     ax.annotate(str(i), (home_summary[home_summary.index==i]['Distance [km]']+ 0.1, home_summary[home_summary.index==i]['AccDec'] + 0.005), fontsize = 10)
# ax.set_xlabel("Distance [km]")
# ax.set_ylabel("AccDec Ratio")
# plt.grid()
# plt.title("Acceleration - Deceleration Ratio")
# plt.show()


# ##############################################################################
# # Calculating metabolic power
# # ----------------------------
# # To calculate metabolic power, we use formulas provided 
# # `here <https://jeb.biologists.org/content/221/15/jeb182303>`_. Then, we make a plot how it has changed
# # for Home Player 6.

# def split_at(s, c, n):
#     words = s.split(c)
#     return c.join(words[:n]), c.join(words[n:])

# #function to calculate metabolic cost
# def metabolic_cost(acc): #https://jeb.biologists.org/content/221/15/jeb182303
#     if acc > 0:
#         cost = 0.102 * ((acc ** 2 + 96.2) ** 0.5) * (4.03 * acc + 3.6 * np.exp(-0.408 * acc))
#     elif acc < 0:
#         cost = 0.102 * ((acc ** 2 + 96.2) ** 0.5) * (-0.85 * acc + 3.6 * np.exp(1.33 * acc))
#     else:
#         cost = 0
#     return cost

# team = tracking_home

# playerids = np.unique(list(c[:-2] for c in team.columns if c[:4] in ['Home', 'Away']))
# playerids = np.unique(list(map(lambda x: split_at(x, '_', 2)[0], playerids)))

# fig, ax = plt.subplots(figsize = (10, 6))
# player = 'Home_6'
# #calculate metabolic cost
# mc_temp = list(map(lambda x: metabolic_cost(team[player + '_Acc'][x]), range(1, len(team[player + '_Acc'])+1)))
# #multiply it by speed
# mp_temp = mc_temp * team[player+'_speed']
# #calculate rolling average
# test_mp = mp_temp.rolling(7500,min_periods=1).apply(lambda x : np.nansum(x)) #Use Changepoint Detection Here
# ax.plot(test_mp[7500:])
# ax.set_title('Metabolic Power Output')
# ax.set_ylabel("Metabolic Power")
# ax.set_xlabel("Frame")
# plt.show()

##############################################################################
# Change point detection
# ----------------------------
# We will try to identify a correct moment for a player to be substituted. To do so, we will use Binary Segmentation method.

# signal = np.array(test_mp[7500:len(test_mp)]).reshape((len(test_mp[7500:len(test_mp)]),1))
# algo = rpt.Binseg(model="l2").fit(signal)  ##potentially finding spot where substitution should happen
# result = algo.predict(n_bkps=1)  # big_seg
# rpt.show.display(signal, result, figsize=(10, 6))
# plt.title('Metabolic Power Output  - Binary segmentation prediction')
# plt.ylabel("Metabolic Power")
# plt.xlabel("Frame")
# plt.show()

##############################################################################
# Multiple changing points
# ----------------------------
# To see how player pacing strategy or identify moments in the game that are slower we can use PELT - 
# lineary penalized segmentation

# signal = np.array(test_mp[7500:len(test_mp)]).reshape((len(test_mp[7500:len(test_mp)]),1))
# algo = rpt.Pelt(model="l2",min_size=7500).fit(signal)
# result = algo.predict(pen=np.log(len(signal))*1*np.std(signal)**2) 
# rpt.show.display(signal, result, figsize=(10, 6))
# plt.title('Metabolic Power Output  - PELT')
# plt.ylabel("Metabolic Power")
# plt.xlabel("Frame")
# plt.show()

##############################################################################
# Using statistics to determine statistical significance between average distance covered and distance covered after high intensity run
# ----------------------------
# In this part of the tutorial we can show how you can conclude that players cover less distance a minute after high intensity run than in average. But first,
# we have to prepare the data for both home and away players to calculate both values. Then, we will use mixed linear regression to show significance of this diffference.


# #for home team
# home_spi_list = []
# #for each player
# for player in home_players:
    
#     #get speed rolling average
#     test_spi = tracking_home['Home_'+player+'_speed'].rolling(1500,min_periods=1).apply(lambda x : np.nansum(x)) / 25.
#     #find it peaks
#     xcoords = sp.signal.find_peaks(test_spi, distance=1500)
#     #get values and indicies of peaks
#     spi_values = list(map(lambda x: test_spi[x], xcoords[0]))
#     #take minute after
#     spi_values_index = np.argsort(spi_values)[-3:]
#     spi_index = xcoords[0][spi_values_index]
#     #for each peak calculate a minute after
#     for i in range(len(spi_index)):
#         spi_temp = spi_index[i]
#         spi_value_temp = spi_values[spi_values_index[i]]
#         spi_min_after = sum(tracking_home['Home_'+player+'_speed'][spi_temp+2:spi_temp+1502]) / 25. 
#         #append it
#         spi_append = [player,'Dist', spi_value_temp, spi_min_after]
#         home_spi_list.append(spi_append)
#     #find only high intensity runs
#     test_hsd_spi = pd.Series(np.where(tracking_home['Home_'+player+'_speed'] >= 5,tracking_home['Home_'+player+'_speed'],0)).rolling(1500,min_periods=1).apply(lambda x : np.nansum(x)) / 25.
#     #find peaks and their indicies
#     xcoords = sp.signal.find_peaks(test_hsd_spi, distance=1500)
#     hsd_values = list(map(lambda x: test_hsd_spi[x], xcoords[0]))
#     #take minutes after
#     hsd_values_index = np.argsort(hsd_values)[-3:]
#     hsd_index = xcoords[0][hsd_values_index]
#     for i in range(len(hsd_index)):
#         hsd_temp = hsd_index[i]
#         hsd_value_temp = hsd_values[hsd_values_index[i]]
#         hsd_min_after = sum(tracking_home['Home_' + player + '_speed'][hsd_temp+ 2:hsd_temp+ 1502]) / 25.
#         hsd_append = [player,'HSD', hsd_value_temp, hsd_min_after]
#         home_spi_list.append(hsd_append)

# #calculate distance covered per minute
# home_summary['DPM'] = 1000*(home_summary['Distance [km]'] / home_summary['Minutes Played'])

# #prepare data for modelling
# spi_df = pd.DataFrame(np.array(home_spi_list).reshape(83,4), columns = ['Player','Type','SPI','MinAfter'])
# merged = pd.merge(spi_df, home_summary[['DPM']], left_on='Player', right_index=True)
# #remove goalkeeper, would bias results
# hsd_df = merged[merged['Player']!='11']
# #remove nan
# hsd_df_lmm = hsd_df[~hsd_df['MinAfter'].str.contains("nan")]
# hsd_df_lmm['MinAfter'] = pd.to_numeric(hsd_df_lmm['MinAfter'])
# hsd_df_lmm['Diff'] = hsd_df_lmm['MinAfter'] - hsd_df_lmm['DPM']
# hsd_df_lmm['Team'] = 'Home'

# #repeat for away team
# away_spi_list = []

# for player in away_players:
#     #get speed rolling average
#     test_spi = tracking_away['Away_'+player+'_speed'].rolling(1500,min_periods=1).apply(lambda x : np.nansum(x)) / 25.
#     #find peaks
#     xcoords = sp.signal.find_peaks(test_spi, distance=1500)
#     #get values and indicies
#     spi_values = list(map(lambda x: test_spi[x], xcoords[0]))
#     #take 3 biggest peaks
#     spi_values_index = np.argsort(spi_values)[-3:]
#     spi_index = xcoords[0][spi_values_index]
#     for i in range(len(spi_index)):
#         spi_temp = spi_index[i]
#         spi_value_temp = spi_values[spi_values_index[i]]
#         spi_min_after = sum(tracking_away['Away_'+player+'_speed'][spi_temp+2:spi_temp+1502]) / 25. # Find the top 3 for each player and then can do a lmm (Diff From Avg ~ 1, group == Player)
#         spi_append = [player,'Dist',spi_value_temp,spi_min_after]
#         away_spi_list.append(spi_append)
#     #for each peak calculate a minute after
#     #same steps for high intensity runs    
#     test_hsd_spi = pd.Series(np.where(tracking_away['Away_'+player+'_speed'] >= 5,tracking_away['Away_'+player+'_speed'],0)).rolling(1500,min_periods=1).apply(lambda x : np.nansum(x)) / 25.
#     xcoords = sp.signal.find_peaks(test_hsd_spi, distance=1500)
#     hsd_values = list(map(lambda x: test_hsd_spi[x], xcoords[0]))
#     hsd_values_index = np.argsort(hsd_values)[-3:]
#     hsd_index = xcoords[0][hsd_values_index]
#     for i in range(len(hsd_index)):
#         hsd_temp = hsd_index[i]
#         hsd_value_temp = hsd_values[hsd_values_index[i]]
#         hsd_min_after = sum(tracking_away['Away_' + player + '_speed'][hsd_temp+ 2:hsd_temp+ 1502]) / 25.
#         hsd_append = [player,'HSD',hsd_value_temp,hsd_min_after]
#         away_spi_list.append(hsd_append)
        
# #change to meters
# away_summary['DPM'] = 1000*(away_summary['Distance [km]'] / away_summary['Minutes Played'])
# #prepare for modelling
# spi_df = pd.DataFrame(np.array(away_spi_list).reshape(72,4), columns = ['Player','Type','SPI','MinAfter'])
# merged = pd.merge(spi_df, away_summary[['DPM']], left_on='Player', right_index=True)
# #remove goalie
# hsd_df = merged[merged['Player']!='25']
# hsd_df_lmm_away = hsd_df[~hsd_df['MinAfter'].str.contains("nan")]
# hsd_df_lmm_away['MinAfter'] = pd.to_numeric(hsd_df_lmm_away['MinAfter'])
# hsd_df_lmm_away['Diff'] = hsd_df_lmm_away['MinAfter'] - hsd_df_lmm_away['DPM']
# hsd_df_lmm_away['Team'] = 'Away'

# hsd_full = pd.concat([hsd_df_lmm, hsd_df_lmm_away])

# #model hsd and distance
# md_hsd = smf.mixedlm("Diff ~ 1", hsd_full[hsd_full['Type']=='HSD'], groups = hsd_full[hsd_full['Type']=='HSD']['Player'])
# md_dist = smf.mixedlm("Diff ~ 1", hsd_full[hsd_full['Type']=='Dist'], groups = hsd_full[hsd_full['Type']=='Dist']['Player'])

# mdf_hsd = md_hsd.fit(method='cg')
# print(mdf_hsd.summary())

# mdf_dist = md_dist.fit(method='cg')
# print(mdf_dist.summary())

##############################################################################
# The code above has been commented out because of too long running time.
# If you unoccment it, it will print out that the difference is statistically significant
