import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
def Impacts(homeimpacts,homegoals,homeids,positions_ours,names,cat):
    if cat == 'd':
        mult = 3
    else:
        mult = 2

    image = plt.imread('Football Pitch.jpg')
    fig=  plt.figure(figsize=(763/30,504/30))
    plt.imshow(image)
    count = 0
    for position in positions_ours:
        
        try:
            impact=(homeimpacts[homeids == position[-1]][0])
            goals=(homegoals[homeids == position[-1]][0])
        except:
            impact = 0
            goals = 0
        print(position,impact)
        plt.scatter(position[3]/3,position[4]/3,4000,color = (max(min(np.tanh(mult*(impact)),1),0),0,max(min(-np.tanh(3*(impact)),1),0),1))
        text =position[6]
        if goals > 0:
            if goals > 1:
                text += ' (' + str(round(goals)) + 'G)'
            else:
                text += ' (G)'

        plt.text(position[3]/3 - 2.4*len(text),position[4]/3 + 35,text,size='small',backgroundcolor = 'w')
        plt.text(position[3]/3-2.7*len(str(round(impact,2))) ,position[4]/3+3,str(round(impact,2)),size='small',c = 'w')
        count+=1


    count = 0
    for n in range(len(homeids)):
        if np.sum(positions_ours[:,-1] == homeids[n]) == 0:
            if count == 0:
                plt.text(8,20,'Subs:',size = 'small')
            plt.scatter(20,40 + 60*count,4000,color = (max(min(np.tanh(mult*(homeimpacts[n])),1),0),0,max(min(-np.tanh(3*(homeimpacts[n])),1),0),1),marker='s')
            text = ''
            pos = len(names[n]) - 1
            while names[n][pos] !=' ':
                text = names[n][pos] + text
                pos-=1
            goals = homegoals[n]
            if goals > 0:
                if goals > 1:
                    text += ' (' + str(homegoals[count]) + 'G)'
                else:
                    text += ' (G)'
            plt.text(50,42 + 60*count,text,backgroundcolor='w',size='small')
            
            plt.text(8,42 + 60*count,str(round(homeimpacts[n],2)),size='small',c = 'w')
            count+=1
    plt.yticks([])
    plt.xticks([]) 
    return fig
def Passmap(positions_ours,passes_ours):
    image = plt.imread('Football Pitch.jpg')
    fig=  plt.figure(figsize=(763/30,504/30))
    plt.imshow(image)

    plt.scatter(positions_ours[:,3]/3,positions_ours[:,4]/3,30*positions_ours[:,5].astype(int),c='k')
    import streamlit as st
    

    for position in positions_ours:
        plt.text(position[3]/3 - 2.4*len(position[6]),position[4]/3 + 20 + int(position[5]*0.1),position[6],size='small',backgroundcolor = 'w')


    for passour in passes_ours:
        plt.plot([passour[3]/3,passour[5]/3],[passour[4]/3,passour[6]/3],c=(max(0,min(1,passour[9]/255)),max(0,min(1,(passour[8])/255)),max(0,min(1,passour[7]/255))),linewidth=passour[10])#(passour[7]/255,passour[8]/255,passour[9]/255,0.99)

    plt.yticks([])
    plt.xticks([])    
    return fig
#    plt.scatter(position[3]/3,position[4]/3,s=position[5]*30,c = 'k')
    
    

def Match_Scroller(team,string,strings,matchdata):
      
     #### This match! ###

    #string = '1 Jan v Slough'
    indices = np.arange(len(strings))
    row = matchdata[indices[strings == string][0]]
    impactdata = pd.read_csv('AllAttacks.csv')
    impactdata.columns = ['id','date','opp','start','sub','a','a','a','a','a','a','a','a','a','a','a','goal','assist']


    homedata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        homedata = homedata[(homedata['opp'] == row[2])].to_numpy()
    else:
        homedata = homedata[(homedata['opp'] == row[1])].to_numpy()


    homeimpacts = np.sum(homedata[:,5:-2],1)
    homegoals = homedata[:,-1]
    homeassists = homedata[:,-2]
    homeids = homedata[:,0]
    namesdata = pd.read_csv('Player_List.csv').to_numpy()
    names = []
    for idin in homeids:
        try:
            names.append(namesdata[namesdata[:,0] == idin][0][1])
        except:
            names.append('Unknown')
    ######
    awaydata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        awaydata = awaydata[(awaydata['opp'] == row[1])].to_numpy()
    else:
        awaydata = awaydata[(awaydata['opp'] == row[2])].to_numpy()

    awayimpacts = np.sum(awaydata[:,5:-2],1)
    awayids = awaydata[:,0]
    awaygoals = awaydata[:,-1]
    awayassists=awaydata[:,-2]
    awaynames = []
    for awayid in awayids:
        try:
            awaynames.append(namesdata[namesdata[:,0] == awayid][0][1])
        except:
            awaynames.append('Unknown')


    ####
    impactdata = pd.read_csv('AllDefences.csv')
    impactdata.columns = ['id','date','opp','start','sub','a','a','a','a','a','a','a','a']
    homedata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        opp_out = row[2]
        homedata = homedata[(homedata['opp'] == row[2])].to_numpy()
    else:
        opp_out = row[1]
        homedata = homedata[(homedata['opp'] == row[1])].to_numpy()
    homeimpactsd = np.sum(homedata[:,5:],1)

    homeidsd = homedata[:,0]
    namesdata = pd.read_csv('Player_List.csv').to_numpy()
    namesd = []
    for idin in homeidsd:
        try:
            namesd.append(namesdata[namesdata[:,0] == idin][0][1])
        except:
            namesd.append('Unknown')
    ######
    awaydata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        awaydata = awaydata[(awaydata['opp'] == row[1])].to_numpy()
    else:
        awaydata = awaydata[(awaydata['opp'] == row[2])].to_numpy()
    awayimpactsd = np.sum(awaydata[:,5:],1)
    awayidsd = awaydata[:,0]

    awaynamesd = []
    for awayid in awayidsd:
        try:
            awaynamesd.append(namesdata[namesdata[:,0] == awayid][0][1])
        except:
            awaynamesd.append('Unknown')



    ####
    passes = pd.read_csv('Passes.csv')

    passes.columns = ['Away', 'Home','Date','Pos1','Pos2','Pos3','Pos4','Col1','Col2','Col3','Weight']
    passes_rel = passes[(passes['Date'] == row[0])]
    passes_ours = passes_rel[passes_rel['Home'] == team]
    import streamlit as st

    opponent = passes_ours['Away'].to_numpy()
    
    opponent = opponent[0]
    
    passes_opp = passes_rel[passes_rel['Home'] == opponent]
    positions = pd.read_csv('Positions.csv')
    positions.columns = ['Away', 'Home','Date','Pos1','Pos2','Size','Name','id']
    positions_rel = positions[(positions['Date'] == row[0])]
    positions_ours = positions_rel[positions_rel['Home'] == team]
    opponent = positions_ours['Away'].to_numpy()
    opponent = opponent[0]
    positions_opp = positions_rel[positions_rel['Home'] == opponent]
    positions_ours = positions_ours.to_numpy()
    passes_ours =passes_ours.to_numpy()
    positions_opp =positions_opp.to_numpy()
    passes_opp = passes_opp.to_numpy()
    fig1 = Impacts(homeimpactsd,np.zeros(len(homeimpactsd)),homeidsd,positions_ours,namesd,'d')
    fig2 = Impacts(homeimpacts,homegoals,homeids,positions_ours,names,'a')
    fig3 = Impacts(awayimpacts,awaygoals,awayids,positions_opp,awaynames,'d')
    fig4 = Impacts(awayimpactsd,np.zeros(len(awayimpactsd)),awayids,positions_opp,awaynamesd,'d')
    fig5 = Passmap(positions_ours,passes_ours)
    fig6 = Passmap(positions_opp,passes_opp)
    return fig1,fig2,fig3,fig4,fig5,fig6,opp_out
def Match_Scroller_Lite(team,string,strings,matchdata):
      
    #### This match! ###

    #string = '1 Jan v Slough'
    indices = np.arange(len(strings))
    row = matchdata[indices[strings == string][0]]
    impactdata = pd.read_csv('AllAttacks.csv')
    impactdata.columns = ['id','date','opp','start','sub','a','a','a','a','a','a','a','a','a','a','a','goal','assist']


    homedata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        homedata = homedata[(homedata['opp'] == row[2])].to_numpy()
    else:
        homedata = homedata[(homedata['opp'] == row[1])].to_numpy()


    homeimpacts = np.sum(homedata[:,5:-2],1)
    homegoals = homedata[:,-1]
    homeassists = homedata[:,-2]
    homeids = homedata[:,0]
    namesdata = pd.read_csv('Player_List.csv').to_numpy()
    names = []
    for idin in homeids:
        try:
            names.append(namesdata[namesdata[:,0] == idin][0][1])
        except:
            names.append('Unknown')
    ######
    awaydata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        awaydata = awaydata[(awaydata['opp'] == row[1])].to_numpy()
    else:
        awaydata = awaydata[(awaydata['opp'] == row[2])].to_numpy()

    awayimpacts = np.sum(awaydata[:,5:-2],1)
    awayids = awaydata[:,0]
    awaygoals = awaydata[:,-1]
    awayassists=awaydata[:,-2]
    awaynames = []
    for awayid in awayids:
        try:
            awaynames.append(namesdata[namesdata[:,0] == awayid][0][1])
        except:
            awaynames.append('Unknown')


    ####
    impactdata = pd.read_csv('AllDefences.csv')
    impactdata.columns = ['id','date','opp','start','sub','a','a','a','a','a','a','a','a']
    homedata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        opp_out = row[2]
        homedata = homedata[(homedata['opp'] == row[2])].to_numpy()
    else:
        opp_out = row[1]
        homedata = homedata[(homedata['opp'] == row[1])].to_numpy()
    homeimpactsd = np.sum(homedata[:,5:],1)

    homeidsd = homedata[:,0]
    namesdata = pd.read_csv('Player_List.csv').to_numpy()
    namesd = []
    for idin in homeidsd:
        try:
            namesd.append(namesdata[namesdata[:,0] == idin][0][1])
        except:
            namesd.append('Unknown')
    ######
    awaydata = impactdata[(impactdata['date'] == row[0])]
    if row[1] == team:
        awaydata = awaydata[(awaydata['opp'] == row[1])].to_numpy()
    else:
        awaydata = awaydata[(awaydata['opp'] == row[2])].to_numpy()
    awayimpactsd = np.sum(awaydata[:,5:],1)
    awayidsd = awaydata[:,0]

    awaynamesd = []
    for awayid in awayidsd:
        try:
            awaynamesd.append(namesdata[namesdata[:,0] == awayid][0][1])
        except:
            awaynamesd.append('Unknown')



    ####
    passes = pd.read_csv('Passes.csv')

    passes.columns = ['Away', 'Home','Date','Pos1','Pos2','Pos3','Pos4','Col1','Col2','Col3','Weight']
    passes_rel = passes[(passes['Date'] == row[0])]
    passes_ours = passes_rel[passes_rel['Home'] == team]
    passes_opp = passes_rel[passes_rel['Home'] == passes_rel['Away'].to_numpy()[0]]
    positions = pd.read_csv('Positions.csv')
    positions.columns = ['Away', 'Home','Date','Pos1','Pos2','Size','Name','id']
    positions_rel = positions[(positions['Date'] == row[0])]
    positions_ours = positions_rel[positions_rel['Home'] == team]
    positions_opp = positions_rel[positions_rel['Home'] == positions_rel['Away'].to_numpy()[0]]
    positions_ours = positions_ours.to_numpy()
    passes_ours =passes_ours.to_numpy()
    positions_opp =positions_opp.to_numpy()
    passes_opp = passes_opp.to_numpy()
    fig1 = Passmap(positions_ours,passes_ours)
    return fig1,opp_out,positions_ours



