import csv
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
from Graph_Creators import Radar_Chart, Match_Chart, Match_Chart_Defensive,ShotMap
from MatchScroller import Match_Scroller,Match_Scroller_Lite
import seaborn as sns
st.set_page_config(layout="wide")
tab0, tab1, tab2 = st.tabs(["Note","Teams", "Division"])
with tab0:
    st.subheader('Notes on underlying data')
    st.write('1) This app presents detailed analysis of players and teams in the 2017/18 Premier League season, as well as predictions for the current (2022/23) season. All data used is open source.')
    st.write('2) Data from the 2017/18 season (in the teams tab) was taken from https://github.com/koenvo/wyscout-soccer-match-event-dataset. The data for Premier League results this season (in the division tab) was taken from https://www.footballwebpages.co.uk/premier-league/match-grid on 2 Feb, 2023.')
    st.write('3) The squad of each team in the app is as it was at the end of the 2017/18 season. Thus, some players may be missing (e.g. a team may appear to have no goalkeeper!)')
with tab1:
    
    col1,col2,col3 = st.columns(3)
    lines = pd.read_csv('Player_List.csv').to_numpy()
    teams = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])
    with col1:
        teams = st.selectbox("Choose team: ",teams)
    with col2:
        views = st.selectbox("Choose view",np.array(["Dashboard","Attributes",'Attacking Impact Per Game','Defensive Impact Per Game',"Matches","Player Detail"]))
    
    ######################################################################################################################
    ########################################### Dashboard ################################################################
    ######################################################################################################################
    if views == "Dashboard":
        col1,col2 = st.columns(2)
        
        ################################### Get Passing ##############################
        plt.rcParams.update({'font.size': 25})
        teams_array = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])

        teams_orig = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])
        
        
        
        
        team = teams_array[teams_orig == teams][0]

        matchdata = pd.read_csv('MatchCSV.csv',header=None)
        matchdata.columns = ['Date','Home','Away','S1','S2']

        matchdata =matchdata[(matchdata['Home'] == team)|(matchdata['Away']==team)].to_numpy()

        months = np.array(['Blank','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
        ##### Which match? ####

        strings = []

        for match in matchdata:
            datestring = match[0]
            stringout = '(Gameweek ' + str(datestring) + ')'
            strings.append(stringout)
        
        strings = np.array(strings)
        curr = 0
        pout = []
        while len(pout) == 0:
            fig,oppout,pout = Match_Scroller_Lite(team,strings[curr],strings,matchdata)
            curr+=1
        with col2:
            st.subheader('Most recent match (v ' + oppout + ')' )
            st.write('Note that this does not include substitutes')
            st.pyplot(fig)
        ######################################## Get Impacts ##########################################    
        
        attr = pd.read_csv('Attacks_Impact_DF.csv', header=None).fillna(0)
        attr.columns = ["ID","Name","Team",'Position','Games','Duels','Passing','Shooting','Attacking Impact / Game']
        
        attr = attr[(attr["Team"] == teams)]
        ids = attr.to_numpy()[:,0]
        attr = attr[["Name",'Position','Games','Attacking Impact / Game']] 
        
        attr_np = attr.to_numpy()
        games = []
        for row in attr_np:
            
            if row[2][1] != ' ':
                games.append(row[2][0:2])
            else:
                games.append(row[2][0])
        for n in range(len(games)):
            games[n] = int(games[n])
        attr = attr[np.array(games) > 4]
        attr = attr.sort_values(by=['Attacking Impact / Game'],ascending=False)  
        
        with col1:
            # CSS to inject contained in a string
            st.subheader('Top Attacking Threats:')
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            st.markdown(hide_table_row_index, unsafe_allow_html=True)
            
            st.table(attr[:5].style.format({'Attacking Impact / Game':"{:.2}"}))
        ############################################ Get Attributes ################################################
        attr = pd.read_csv('Attributes_CSV_DF.csv', header=None).fillna(0)
        attr.columns = ["ID","Name","Team",'Position','Games','Shooting','Passing','Aerial','Inters']
        averages = attr[attr['Team'] == 'None'].to_numpy()
        
        attr = attr[attr['Team'] == teams]
        attr_np = attr.to_numpy()
        games = []
        for row in attr_np:
            if len(row) < 4:
                games.append(0)
                continue
            else:
                if len(row[4]) < 2:
                    games.append(0)
                    continue
                    
            if row[4][1] != ' ':
                games.append(row[4][0:2])
            else:
                games.append(row[4][0])
        for n in range(len(games)):
            games[n] = int(games[n])
        attr = attr[np.array(games) > 4]
        attr_np = attr.to_numpy()
        Position_Groups = [
            ['GK'],
            ['DF'],
            ['MD'],
            ['FW']
        ]
        mainnames = ['GKs','DFs','MDs','FWs']
        indexes = [0,1,2,3,5,6]
        rows = []
        count = 0
        for pos in Position_Groups:
            sums = np.zeros(4)
            total_length = 0
            for posse in pos:
                rel = attr_np[attr_np[:,3] == posse]
                if len(rel) > 0:
                    total_length +=len(rel[:,5])
                    for m in range(4):
                        sums[m] += np.sum(rel[:,m+5])

            if total_length == 0:
                rows.append([mainnames[count],sums[0],sums[1],sums[2],sums[3]])
            else:
                output = (sums/total_length) - averages[indexes[count],5:]
                rows.append([mainnames[count],float(output[0]),float(output[1]),float(output[2]),float(output[3])])
            
            count+=1
        with col1:
            hide_table_row_index = """
                        <style>
                        thead tr th:first-child {display:none}
                        tbody th {display:none}
                        </style>
                        """

            # Inject CSS with Markdown
            rows = np.array(rows)
            
            vals = rows[:,1:]
            
            
            cm = sns.color_palette("RdYlGn_r", as_cmap=True)
            deep_pal = sns.color_palette('deep')
            cm = sns.blend_palette([deep_pal[3], deep_pal[-2], deep_pal[2]], as_cmap=True)
            rows = pd.DataFrame(rows, columns = ['Position','Shooting/Saving','Passing','Aerial','Inters'])
            rows[['Shooting/Saving','Passing','Aerial','Inters']] = rows[['Shooting/Saving','Passing','Aerial','Inters']].astype(float)
            st.subheader('Attributes Compared to EPL Average')
            st.markdown(hide_table_row_index, unsafe_allow_html=True)

            st.table(rows.style.background_gradient(axis=None,cmap=cm,subset=['Shooting/Saving','Passing','Aerial','Inters'],gmap = vals,vmin=-10,vmax=10).format({'Shooting/Saving':"{:.1f}",'Passing':"{:.1f}",'Aerial':"{:.1f}",'Inters':"{:.1f}"}))
        
       
        st.write('The attributes chart compares the average attributes by position of the players who have played at least 5 games for this team to the EPL average. A high number shows that this team is above average in an attribute for a position, while a low number indicates it is below average.')
    
    ######################################################################################################################
    ########################################### Player Details ###########################################################
    ######################################################################################################################
    
    if views == "Player Detail":

        with col3:
            players = st.selectbox(
                    "Choose player:", lines[lines[:,2] == teams,1]
                )

        index = (lines[:,1] == players)
        col1,col4, col2, col5,col3 = st.columns([1.3,0.3,2.2, 0.3,3])
        player = lines[index,0]
        position = lines[index,3]
        fig2,starts_out,subs_out,goals_out,assists_out,att_impact_out = Match_Chart(player)
        fig3,def_impact_out = Match_Chart_Defensive(player)
        with col1:
            st.subheader('Basic Stats:')
            st.write('Position: ' + position[0])
            st.write('Starts (Subs): ' + str(round(starts_out)) +  ' (' + str(round(subs_out)) + ')')
            st.write('Goals (Assists): ' + str(round(goals_out))+  ' (' + str(round(assists_out)) + ')')
            st.write('Attacking Impact / Game: ' + str(round(att_impact_out,2)))
            if starts_out + (1/3)*subs_out > 0:
                st.write('Defensive Impact / Game: ' + str(round(def_impact_out/(starts_out + (1/3)*subs_out),2)))
            else:
                st.write('Defensive Impact / Game: ' + str(0))

        with col3:
            st.subheader('Attributes:')
            fig = Radar_Chart(players)
            st.pyplot(fig)
        with col1:
            st.subheader('Shot Data:')
            fig = ShotMap(player)
            st.pyplot(fig)
        with col2:
            st.subheader('Attacking Impact:')

            st.pyplot(fig2)

            st.subheader('Defensive Impact:')

            st.pyplot(fig3)

            
    ######################################################################################################################
    ################################################ Attributes ##########################################################
    ######################################################################################################################
            
    if views == 'Attributes':
        attr = pd.read_csv('Attributes_CSV_DF.csv', header=None).fillna(0)
        attr.columns = ["ID","Name","Team",'Position','Games','Shooting','Passing','Aerial','Inters']
        attr = attr[(attr["Team"] == teams)|(attr["Team"] == 'None')]
        attr = attr[["Name",'Position','Games','Shooting','Passing','Aerial','Inters']]
        attr = attr[(attr['Games'] != '0')|(attr['Name'] == 'Average (EPL)')]
        attr[['Shooting','Passing','Aerial','Inters']]=attr[['Shooting','Passing','Aerial','Inters']].astype(int)
        cm = sns.color_palette("RdYlGn_r", as_cmap=True)
        deep_pal = sns.color_palette('deep')
        cm = sns.blend_palette([deep_pal[3], deep_pal[-2], deep_pal[2]], as_cmap=True)
        
        
        attr_gk = pd.read_csv('Attributes_CSV_DF.csv', header=None).fillna(0)
        attr_gk.columns = ["ID","Name","Team",'Position','Games','Saving','Passing','Aerial','Inters']
        attr_gk = attr_gk[(attr_gk["Team"] == teams)|(attr_gk["Team"] == 'None')]
        attr_gk = attr_gk[(attr_gk['Games'] != '0')|(attr_gk['Name'] == 'Average (EPL)')]
        attr_gk = attr_gk[["Name",'Games','Position','Saving','Passing','Aerial','Inters']]
        attr_gk[['Saving','Passing','Aerial','Inters']]=attr_gk[['Saving','Passing','Aerial','Inters']].astype(int)

        
        col21, col22, col23 = st.columns(3)
        with col21:

            st.subheader('Goalkeepers')
            a = attr_gk[(attr_gk['Position'] == 'GK')|(attr['Position'] == 'GKs')]
            vals = a[['Saving','Passing','Aerial','Inters']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.background_gradient(axis=None,cmap=cm,subset=['Saving','Passing','Aerial','Inters'],gmap = (vals - mids)/10,vmin=-1,vmax=1))
            
            st.subheader('Forwards')
            a = attr[(attr['Position'] == 'FW')|(attr['Position'] == 'FWs')]
            vals = a[['Shooting','Passing','Aerial','Inters']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.background_gradient(axis=None,cmap=cm,subset=['Shooting','Passing','Aerial','Inters'],gmap = (vals - mids)/10,vmin=-1,vmax=1))
        with col22:

            st.subheader('Defenders')
            a = attr[(attr['Position'] == 'DF')|(attr['Position'] == 'DFs')]
            vals = a[['Shooting','Passing','Aerial','Inters']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.background_gradient(axis=None,cmap=cm,subset=['Shooting','Passing','Aerial','Inters'],gmap = (vals - mids)/10,vmin=-1,vmax=1))

        with col23:

            st.subheader('Midfielders')
            a = attr[(attr['Position'] == 'MD')|(attr['Position'] == 'MDs')]
            vals = a[['Shooting','Passing','Aerial','Inters']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.background_gradient(axis=None,cmap=cm,subset=['Shooting','Passing','Aerial','Inters'],gmap = (vals - mids)/10,vmin=-1,vmax=1))


            
        
    ######################################################################################################################
    ################################################ Attacking ##########################################################
    ######################################################################################################################
            
    if views == 'Attacking Impact Per Game':
        attr = pd.read_csv('Attacks_Impact_DF.csv', header=None).fillna(0)
        attr.columns = ["ID","Name","Team",'Position','Games','Duels','Passing','Shooting','Overall']
        attr = attr[(attr["Team"] == teams)|(attr["Team"] == 'None')]
        attr = attr[["Name",'Position','Games','Duels','Passing','Shooting','Overall']]
        attr[['Duels','Passing','Shooting','Overall']]=attr[['Duels','Passing','Shooting','Overall']].astype(float)
        attr[['Duels','Passing','Shooting','Overall']].round(2)
        cm = sns.color_palette("RdYlGn_r", as_cmap=True)
        deep_pal = sns.color_palette('deep')
        cm = sns.blend_palette([deep_pal[3], deep_pal[-2], deep_pal[2]], as_cmap=True)
        
       
        
        col21, col22, col23 = st.columns(3)
        with col21:

            st.subheader('Goalkeepers')
            a = attr[(attr['Position'] == 'GK')|(attr['Position'] == 'GKs')]
            vals = a[['Duels','Passing','Shooting','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Duels':"{:.2}",'Passing':"{:.2}",'Shooting':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Duels','Passing','Shooting','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))
            
            st.subheader('Forwards')
            a = attr[(attr['Position'] == 'FW')|(attr['Position'] == 'FWs')]
            vals = a[['Duels','Passing','Shooting','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Duels':"{:.2}",'Passing':"{:.2}",'Shooting':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Duels','Passing','Shooting','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))
        with col22:

            st.subheader('Defenders')
            a = attr[(attr['Position'] == 'DF')|(attr['Position'] == 'DFs')]
            vals = a[['Duels','Passing','Shooting','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Duels':"{:.2}",'Passing':"{:.2}",'Shooting':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Duels','Passing','Shooting','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))

        with col23:

            st.subheader('Midfielders')
            a = attr[(attr['Position'] == 'MD')|(attr['Position'] == 'MDs')]
            vals = a[['Duels','Passing','Shooting','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Duels':"{:.2}",'Passing':"{:.2}",'Shooting':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Duels','Passing','Shooting','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))
        
       
        st.header('Explanation:')
        st.write('Duels: This measures the impact of the times that the player has won or lost the ball through headers and tackles')
        st.write('Passing: This measures the impact of the passes and crosses that each player has attempted')
        st.write("Shooting: This meausres the impact of players' shots.")
        
    ######################################################################################################################
    ################################################ Attacking ##########################################################
    ######################################################################################################################
        
    if views == 'Defensive Impact Per Game':
        attr = pd.read_csv('Defences_Impact_DF.csv', header=None).fillna(0)
        attr.columns = ["ID","Name","Team",'Position','Games','Pickups','Duels','Lost Balls','Overall']
        attr = attr[(attr["Team"] == teams)|(attr["Team"] == 'None')]
        attr = attr[["Name",'Position','Games','Pickups','Duels','Lost Balls','Overall']]
        attr[['Pickups','Duels','Lost Balls','Overall']]=attr[['Pickups','Duels','Lost Balls','Overall']].astype(float)
        attr[['Pickups','Duels','Lost Balls','Overall']].round(2)
        cm = sns.color_palette("RdYlGn_r", as_cmap=True)
        deep_pal = sns.color_palette('deep')
        cm = sns.blend_palette([deep_pal[3], deep_pal[-2], deep_pal[2]], as_cmap=True)
        
       
        
        col21, col22, col23 = st.columns(3)
        with col21:

            st.subheader('Goalkeepers')
            a = attr[(attr['Position'] == 'GK')|(attr['Position'] == 'GKs')]
            vals = a[['Pickups','Duels','Lost Balls','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Pickups':"{:.2}",'Duels':"{:.2}",'Lost Balls':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Pickups','Duels','Lost Balls','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))
            
            st.subheader('Forwards')
            a = attr[(attr['Position'] == 'FW')|(attr['Position'] == 'FWs')]
            vals = a[['Pickups','Duels','Lost Balls','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Pickups':"{:.2}",'Duels':"{:.2}",'Lost Balls':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Pickups','Duels','Lost Balls','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))
        with col22:

            st.subheader('Defenders')
            a = attr[(attr['Position'] == 'DF')|(attr['Position'] == 'DFs')]
            vals = a[['Pickups','Duels','Lost Balls','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Pickups':"{:.2}",'Duels':"{:.2}",'Lost Balls':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Pickups','Duels','Lost Balls','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))

        with col23:

            st.subheader('Midfielders')
            a = attr[(attr['Position'] == 'MD')|(attr['Position'] == 'MDs')]
            vals = a[['Pickups','Duels','Lost Balls','Overall']].to_numpy()
            mids = vals[-1]
            st.dataframe(a.style.format({'Pickups':"{:.2}",'Duels':"{:.2}",'Lost Balls':"{:.2}",'Overall':"{:.2}"}).background_gradient(axis=None,cmap=cm,subset=['Pickups','Duels','Lost Balls','Overall'],gmap = (vals - mids)/0.1,vmin=-1,vmax=1))
        
        st.header('Explanation:')
        st.write('Pickups: This measures the impact of the times that the player has recovered possession (excluding through duels)')
        st.write('Duels: This measures the impact of the times that the player has won or lost the ball through headers and tackles')
       
        st.write("Lost balls: This measures the defensive cost of the times that the player has lost possession")
        
    ######################################################################################################################
    ################################################ Matches ##########################################################
    ######################################################################################################################   
    if views == 'Matches':    
        plt.rcParams.update({'font.size': 25})
        teams_array = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])

        teams_orig = np.array(['AFC Bournemouth','Arsenal','Brighton & Hove Albion','Burnley','Chelsea','Crystal Palace','Everton','Huddersfield Town','Leicester City','Liverpool','Manchester City','Manchester United','Newcastle United','Southampton','Stoke City','Swansea City','Tottenham Hotspur','Watford','West Bromwich Albion','West Ham United'])

        team = teams_array[teams_orig == teams][0]

        matchdata = pd.read_csv('MatchCSV.csv',header=None)
        matchdata.columns = ['Date','Home','Away','S1','S2']

        matchdata =matchdata[(matchdata['Home'] == team)|(matchdata['Away']==team)].to_numpy()

        months = np.array(['Blank','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'])
        ##### Which match? ####

        strings = []
        numbers = []
        for match in matchdata:
            datestring = match[0]
            stringout = 'Gameweek ' + str(datestring) 
            strings.append(stringout)
            numbers.append(-datestring)
        strings = np.array(strings)
        order = np.argsort(numbers)
        strings = strings[order]
       
        with col3:
            players = st.selectbox(
                    "Choose match:", strings
                )
        
        fig1,fig2,fig3,fig4,fig5,fig6,opp_out= Match_Scroller(team,players,strings,matchdata)
        col12,col22 = st.columns(2)
        with col12:
            st.subheader('Passmaps (' + team + ')')
            st.pyplot(fig5)
            st.subheader('Attacking Impact (' + team + ')')
            st.pyplot(fig2)
            st.subheader('Defensive Impact (' + team + ')')
            st.pyplot(fig1)
        with col22:
            st.subheader('Passmaps (' + opp_out + ')')
            st.pyplot(fig6)
            st.subheader('Attacking Impact (' + opp_out + ')')
            st.pyplot(fig3)
            st.subheader('Defensive Impact (' + opp_out + ')')
            st.pyplot(fig4)
        st.write('In the above graphs, red shows positive impact, while blue shows negative')
        st.write('In the pass charts, a larger dot size indicates a player was more involved in the passing. The line thickness shows how often a pair of players passed to each other. The line colour indicates the threat of these passes.')
        st.write('In the attacking impact charts, the number in each dot shows the attacking impact. A (G) after the name of a player indicates that they scored a goal in this match. Substitutes are indicated by squares and are placed to the side to avoid congestion in the middle of the pitch.')
        st.write('In the defensive impact charts, the number in each dot shows the defensive impact. Substitutes are indicated by squares and are placed to the side to avoid congestion in the middle of the pitch.')
    
with tab2:
    col1,col2 = st.columns(2)
    with col1:
        st.subheader('League Table:')
        cm = sns.color_palette("RdYlGn_r", as_cmap=True)
        deep_pal = sns.color_palette('deep')
        cm = sns.blend_palette([deep_pal[3], deep_pal[-2], deep_pal[2]], as_cmap=True)
        league_table = pd.read_csv('League Data.csv', header=None).fillna(0)
        league_table.columns = ['Team','P','W','D','L','F','A','GD','Pts']
        league_table = league_table[league_table['Team'] != 'blank']
        league_table[['P','W','D','L','F','A','GD','Pts']] = league_table[['P','W','D','L','F','A','GD','Pts']].astype(int)
        league_table[['P','W','D','L','F','A','GD','Pts']].round(1)
        
        league_table_np = league_table.to_numpy()
        league_index = np.arange(20)
        
        def custom_style(row):
            row_np = row.to_numpy()
            index = league_index[league_table_np[:,0] == row_np[0]][0]
            color = 'white'
            
            if index < 1:
                color = '#3bbf2c'
            elif index < 4:
                color = '#c1d49d'
            elif index < 7:
                color = '#dfe38a'
            elif index > 16:
                color = '#e39e8a'

            return ['background-color: %s' % color]*len(row.values)

        
        wanted_names = ['BOU','ARS','AVL','BRE','BHA','CHE','CPL','EVE','FUL','LEE','LEI','LIV','MCI','MUN','NEW','NFO','SOT','TOT','WHU','WOL']
        teamsin = np.array(['AFC Bournemouth', 'Arsenal', 'Aston Villa', 'Brentford',
       'Brighton & Hove Albion', 'Chelsea', 'Crystal Palace', 'Everton',
       'Fulham', 'Leeds United', 'Leicester City', 'Liverpool',
       'Manchester City', 'Manchester United', 'Newcastle United',
       'Nottingham Forest', 'Southampton', 'Tottenham Hotspur',
       'West Ham United', 'Wolverhampton Wanderers'])
        st.table(league_table.style.apply(custom_style, axis=1))
        attacks = pd.read_csv('Team Attacks.csv',header=None).to_numpy()
        defences = (pd.read_csv('Team Defences.csv',header=None).to_numpy())
        with col2:
            view = st.selectbox("Choose view: ",np.array(['Team Strengths','Season Predictions','Match Predictions']))
            if view == 'Team Strengths':
                plt.rcParams.update({'font.size': 10})
                fig=  plt.figure(figsize=(8,4))
                yerr =np.zeros((2,20))
                yerr[0,:] = attacks[:,1]- attacks[:,0]
                yerr[1,:] = attacks[:,2] - attacks[:,1]
                plt.errorbar(np.arange(20), abs(attacks[:,1]),yerr = yerr, fmt='o')
                plt.xticks(np.arange(20),labels = wanted_names,rotation=90)
                plt.title('Attacking Strengths')
                st.pyplot(fig)

                fig=  plt.figure(figsize=(8,4))
                yerr =np.zeros((2,20))
                yerr[0,:] = defences[:,1]- defences[:,0]
                yerr[1,:] = defences[:,2] - defences[:,1]
                plt.errorbar(np.arange(20), abs(defences[:,1]),yerr = yerr, fmt='o')
                plt.xticks(np.arange(20),labels = wanted_names,rotation=90)
                plt.title('Defensive Strengths')
                st.pyplot(fig)
            if view == 'Season Predictions':
                teamout = st.selectbox("Team: ",teamsin)
                
                index = np.arange(len(teamsin))[teamsin == teamout][0]

                ranks = pd.read_csv('Rank Probabilities.csv',header=None).to_numpy()
                st.write('Title Chance: ' + str(round(ranks[index,0]*100,2))  + '%')
                
                st.write('Top 4 Chance: ' + str(round(np.sum(ranks[index,0:4]*100),2)) + '%')
                st.write('Top 7 Chance: ' +  str(round(np.sum(ranks[index,0:7]*100),2)) + '%')
                st.write('Relegation Chance: ' +  str(round(np.sum(ranks[index,17:]*100),2)) + '%') 
                plt.rcParams.update({'font.size': 10})
                fig = plt.figure(figsize=(8,4))
                plt.bar(np.arange(20) + 1,ranks[index]*100)
                plt.xticks(np.arange(20)+1)
                plt.xlabel('Position')
                plt.ylabel('Percentage Chance')
                plt.title('Final Position Probabilities (' + teamout + ')')
                st.pyplot(fig)
            if view == 'Match Predictions':   
                teamout2 = st.selectbox("Choose Team: ",teamsin)
                
                index = np.arange(len(teamsin))[teamsin == teamout2][0]
                opp2 = st.selectbox("Choose Opponent: ",teamsin)
                indexopp = np.arange(len(teamsin))[teamsin == opp2][0]
                goals_scored_1 = attacks[index,1]/defences[indexopp,1]
                goals_scored_2 = attacks[indexopp,1]/defences[index,1]
                gs1 = np.random.poisson(goals_scored_1,size=10000)
                gs2 = np.random.poisson(goals_scored_2,size=10000)
                win = np.sum(gs1 > gs2)
                draw = np.sum(gs1 == gs2)
                loss = np.sum(gs1 < gs2)
                fig = plt.figure(figsize=(8,3))
                plt.rcParams.update({'font.size': 10})
                st.write('Expected Goals Scored (' + teamout2 + '): ' + str(round(goals_scored_1,2)))
                st.write('Expected Goals Scored (' + opp2 + '): ' + str(round(goals_scored_2,2)))
                labels = [teamout2 +  ' Win (' +   str(round(win/100)) + '%)', 'Draw (' +   str(round(draw/100)) + '%)', opp2 + ' Win (' +   str(round(loss/100)) + '%)' ]
                
                plt.pie([win,draw,loss],labels = labels)
                st.pyplot(fig)
              
    
