import pandas as pd
import csv
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json

############### CSV Imports #############
lines = pd.read_csv('Player_List.csv').to_numpy()
attr = pd.read_csv('Attributes_CSV.csv', header=None).to_numpy()
shots_csv= pd.read_csv('ShotDataCondensed.csv').to_numpy()

labels=['a','b','c','d']
markers = [0, 1, 2, 3, 4]
str_markers = ["0", "1", "2", "3", "4"]
def make_radar_chart_new(name, stats,stats2, attribute_labels=labels,
                     plot_markers=markers, plot_str_markers=str_markers):
    
    plt.rcParams.update({'font.size': 30})
    labels = np.array(attribute_labels)

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)
    stats = np.concatenate((stats,[stats[0]]))

    stats2 = np.concatenate((stats2,[stats2[0]]))
    angles = np.concatenate((angles,[angles[0]]))

    fig = plt.figure(figsize=(16, 16))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.plot(angles, stats2, 'o-', linewidth=8)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles[:-1] * 180/np.pi, labels)
    #plt.yticks([])
    plt.rcParams.update({'font.size': 20})
    plt.yticks(plot_markers)
    plt.rcParams.update({'font.size': 20})
    plt.legend(["Attributes", 'Average (EPL)'],loc="best")
    ax.set_title(name)
    ax.grid(True)

    return fig



def Radar_Chart(players):
    
    index = lines[players == lines[:,1]][0][0]
    attr_line = attr[attr[:,0] == index][0]
    attributes = np.zeros(4)
    for n in range(4,len(attr_line)):
        attributes[n-4] = float(attr_line[n])


    pos = lines[players == lines[:,1]][0][3]
    PositionGroups = [['GK'],
             ['DF'],
                     ['MD'],
                     ['FW']]

    position_code = -1
    for n in range(4):
        for m in range(len(PositionGroups[n])):

            if PositionGroups[n][m] == pos:
                position_code = n
    GK_indicator = (pos == 'GK')


    if position_code == -1:
        markers =[]
        curr = 0
        maxattr = max(attributes)
        while curr < maxattr:
            markers.append(curr)
            curr+=10

        make_radar_chart_new("", attr_line[4:],['Shooting','Passing','Aerial','Interceptions'],markers)
    else:
        mediantrue = attr[-(4-position_code),4:]
       
        for n in range(len(mediantrue)):
            try:
                mediantrue[n] = round(float(mediantrue[n]))
            except:
                mediantrue[n] = 0

        if GK_indicator:
            maxattr = max(max(mediantrue),max(attributes))
        else:
            maxattr = max(max(mediantrue),max(attributes))
        markers =[]
        curr = 0

        while curr < maxattr+20:
            markers.append(curr)
            curr+=10
        if GK_indicator:
            fig = make_radar_chart_new("", attributes,mediantrue,['Saving','Passing','Aerial','Interceptions'],markers)
        else:
            fig = make_radar_chart_new("", attributes,mediantrue,['Shooting','Passing','Aerial','Interceptions'],markers)
    return fig

def Match_Chart(playerid):
    match_data = pd.read_csv('AllAttacks.csv', header=None).to_numpy()
    impact = []
    teams = []
    order = []
    goals = []
    assists = []
    starts = []
    subs = []

    match_names = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])

    short_names = np.array(['BOU',"ARS",'BHA','BUR','CHE',
                  'CPL','EVE','HUD','LEI','LIV','MCI',
                  "MUN",'NEW','SOT','STO',"SWA",'TOT','WAT','WBA','WHU'])

    plt.rcParams.update({'font.size': 30})
    relevant_match_data = match_data[match_data[:,0] == playerid]
    for line in relevant_match_data:
        teams.append(line[2])
        order.append((line[1]))
        impact.append(line[5:-2])
        assists.append(int(line[-2]))
        goals.append(int(line[-1]))
        starts.append(int(line[3]))
        subs.append(int(line[4]))
    
    
    
    impact_ov = []
    argy = np.array(order).argsort().astype(int)
    teams = np.array(teams)[argy]
    impact = np.array(impact)[argy]
    goals = np.array(goals)[argy]
    assists = np.array(assists)[argy]
    starts = np.array(starts)[argy]
    subs = np.array(subs)[argy]
    
    
    
    impact_out = 0
    for n in range(len(impact)):
        impact_ov.append(0)
        for m in range(len(impact[n])):
            impact_ov[-1] += float(impact[n][m])
            impact_out += float(impact[n][m])
    
    ######## Getting extra parameters ####
    starts_out = np.sum(starts)
    subs_out = np.sum(subs)
    goals_out = np.sum(goals)
    assists_out = np.sum(assists)
    if starts_out + subs_out > 0:
        impact_out = impact_out/(starts_out + (1/3)*subs_out)
    else:
        impact_out = 0
    ###########################################
    
    
    
    
    teams_sh = []
    for n in range(len(teams)):
        teams_sh.append(short_names[match_names == teams[n]][0])

    fig = plt.figure(figsize=(16, 8))
    plt.bar(np.arange(len(impact_ov)),impact_ov,color=(0.2,0.2,0.8,1))
    jumpsize = (max(impact_ov)-min(impact_ov))/20
    for n in range(len(goals)):
        stackcount = 0
        if float(goals[n]) > 1:
            for m in range(round(float(goals[n]))):
                plt.scatter(n,jumpsize+m*2*jumpsize,s=750, marker="s",color=(0,0,0,1),zorder=5)
                plt.scatter(n,jumpsize+m*2*jumpsize,s=500, marker="$G$",color=(0.2,1,0.2,1),zorder=5)
                stackcount+=1
        elif float(goals[n]) == 1:
            plt.scatter(n,jumpsize,s=750, marker="s",color=(0,0,0,1),zorder=5)
            plt.scatter(n,jumpsize,s=500, marker="$G$",color=(0.2,1,0.2,1),zorder=5)
            stackcount+=1
        
        if float(assists[n]) > 1:
            for m in range(round(float(goals[n]))):
                plt.scatter(n,jumpsize+stackcount*jumpsize*2,s=750, marker="s",color=(0,0,0,1),zorder=5)
                plt.scatter(n,jumpsize+stackcount*jumpsize*2,s=500, marker="$A$",color=(0.2,1,0.2,1),zorder=5)
                stackcount+=1
        elif float(assists[n]) == 1:
            plt.scatter(n,jumpsize+stackcount*jumpsize*2,s=750, marker="s",color=(0,0,0,1),zorder=5)
            plt.scatter(n,jumpsize + stackcount*jumpsize*2,s=500, marker="$A$",color=(0.2,1,0.2,1),zorder=5)
            stackcount+=1    

    yticks = []
    curr = -1.6
    if max(impact_ov) - min(impact_ov) < 0.8:
        while curr+0.1 < min(impact_ov):
            curr+=0.1
        while curr-0.1<max(impact_ov):
            yticks.append(curr)
            curr+=0.1
    else:
        if max(impact_ov) - min(impact_ov) < 1.6:
            while curr+0.2 < min(impact_ov):
                curr+=0.2
            while curr-0.2<max(impact_ov):
                yticks.append(curr)
                curr+=0.2
        else:
            while curr+0.3 < min(impact_ov):
                curr+=0.3
            while curr-0.3<max(impact_ov):
                yticks.append(curr)
                curr+=0.3
    plt.yticks(yticks)
    plt.xticks(np.arange(len(impact_ov)),teams_sh,rotation='90')
    plt.ylabel('xG')

    plt.title('Attacking xG By Game (Most Recent on Right)')
    plt.grid(b=True, which='major', axis = 'y',color=(0.2,0.2,0.2,0.1), linestyle='-')
    return fig,starts_out,subs_out,goals_out,assists_out,impact_out
def Match_Chart_Defensive(playerid):
    impact = []
    teams = []
    order = []

    match_data = pd.read_csv('AllDefences.csv', header=None).to_numpy()
    relevant_match_data = match_data[match_data[:,0] == playerid]
    for line in relevant_match_data:
        teams.append(line[2])
        order.append((line[1]))
        impact.append(line[5:])
    match_names = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])

    short_names = np.array(['Bou',"Ars",'BHA','Bur','Che',
                  'CPl','Eve','Hud','Lei','Liv','MCi',
                  "MUn",'New','Sot','Sto',"Swa",'Tot','Wat','WBA','WHU'])
    plt.rcParams.update({'font.size': 30})


            
    impact_ov = []
    argy = np.array(order).argsort().astype(int)
    teams = np.array(teams)[argy]
    impact = np.array(impact)[argy]

    
    
    
    impact_out = 0
    for n in range(len(impact)):
        impact_ov.append(0)
        for m in range(len(impact[n])):
            impact_ov[-1] += float(impact[n][m])
            impact_out += float(impact[n][m])
    teams_sh = []
    for n in range(len(teams)):
        teams_sh.append(short_names[match_names == teams[n]][0])

    fig = plt.figure(figsize=(16, 8))
    plt.bar(np.arange(len(impact_ov)),impact_ov,color=(0.2,0.2,0.8,1))

    
    yticks = []
    curr = -1.6
    if max(impact_ov) - min(impact_ov) < 0.8:
        while curr+0.1 < min(impact_ov):
            curr+=0.1
        while curr-0.1<max(impact_ov):
            yticks.append(curr)
            curr+=0.1
    else:
        while curr+0.2 < min(impact_ov):
            curr+=0.2
        while curr-0.2<max(impact_ov):
            yticks.append(curr)
            curr+=0.2
    plt.yticks(yticks)
    plt.xticks(np.arange(len(impact_ov)),teams_sh,rotation='90')
    plt.ylabel('xG')

    plt.title('Defensive xG By Game (Most Recent on Right)')
    plt.grid(b=True, which='major', axis = 'y',color=(0.2,0.2,0.2,0.1), linestyle='-')
    return fig,impact_out
def ShotMap(playerid):
    image = plt.imread('ShotMapv2.png')
    relevant_rows = shots_csv[shots_csv[:,0] == int(playerid)]

    fig=  plt.figure(figsize=(0.5599588265568708*16, 16))
    plt.imshow(image,extent = [0,52.5,-34,34])
    colors = np.array([[0.9,0.2,0.2,1],[0.2,0.7,0.2,1],[0.9,0.9,0.1,1]])
    plt.scatter(50-relevant_rows[:,2],-relevant_rows[:,3],s=121,c=colors[relevant_rows[:,1].astype(int)])
    plt.yticks([])
    plt.xticks([])
    return fig