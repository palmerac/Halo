import pandas as pd
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import datetime as dt
import seaborn as sns
import ssl

plt.style.use('ggplot')
st.set_page_config(layout="wide")

st.title('Halo Infinite Dashboard')

# Intro + Gamertag search
st.sidebar.markdown("To run with your own Halo data, follow these steps:")
st.sidebar.markdown("1. Go to leafapp.co and navigate to your Matches page")
st.sidebar.markdown("2. Press the Request Stat Update button on the left sidebar")
st.sidebar.markdown("3. Enter your gamertag, press Fetch Stats")
gamertag = st.sidebar.text_input("Enter your gamertag")
fetch_from_website = st.sidebar.button("Fetch Stats")

if 'df' not in st.session_state or fetch_from_website:
    try:
        ssl._create_default_https_context = ssl._create_unverified_context
        df = pd.read_csv(f'https://leafapp.co/player/{gamertag}/matches/csv/matches')
    except Exception as e:
        st.error(f"An error occurred while trying to fetch data from the website: {e}")
        df = pd.read_csv('earl694412-infinite-matchhistory.csv')
    st.session_state.df = df
else:
    df = st.session_state.df


# Data Modification
df['Date'] = pd.to_datetime(df['Date'])
df['LengthMinutes'] = df['LengthSeconds'] / 60
df.rename(columns={'TotalKills': 'Kills'}, inplace=True)
df['KillsBody'] = df['Kills'] - df['KillsGrenade'] - df['KillsHeadshot'] - df['KillsMelee'] - df['KillsPower']

## Per 10 Mins and Excess

tenmins = ['Kills', 'Deaths', 'Assists', 'DamageDone', 'DamageTaken', 'ShotsLanded', 'ShotsFired']

for i in tenmins:
    df[f'{i}/10Min'] = (df[i].replace(0,1) / df['LengthMinutes']) * 10

df['ExcessKills'] = df['Kills'].replace(0,1) - df['ExpectedKills'].replace(0,1)
df['ExcessDeaths'] = df['ExpectedDeaths'].replace(0,1) - df['Deaths'].replace(0,1)

## Ratios
df['DamageRatio'] = df['DamageDone'].replace(0, 1) / df['DamageTaken'].replace(0, 1)
df['Damage/KA'] = df['DamageDone'].replace(0,1) / (df['Assists'].replace(0,1) + df['Kills'].replace(0,1))
df['Damage/Life'] = df['DamageDone'].replace(0,1) / (df['Deaths'].replace(0,1))
df['Assists/Life'] = df['Assists'].replace(0,1) / df['Deaths'].replace(0,1)


## Lifetime
df['LifetimeKD'] = df['Kills'].cumsum() / df['Deaths'].cumsum()
df['LifetimeDmgRatio'] = df['DamageDone'].cumsum() / df['DamageTaken'].cumsum()
df['LifetimeAcc'] = df['ShotsLanded'].cumsum() / df['ShotsFired'].cumsum() * 100
df['LifetimeBodyPct'] = df['KillsBody'].cumsum() / df['Kills'].cumsum() *100
df['LifetimeMeleePct'] = df['KillsMelee'].cumsum() / df['Kills'].cumsum() * 100
df['LifetimeHSPct'] = df['KillsHeadshot'].cumsum() / df['Kills'].cumsum() * 100
df['LifetimeGrenadePct'] = df['KillsGrenade'].cumsum() / df['Kills'].cumsum() * 100
df['LifetimePowerPct'] = df['KillsPower'].cumsum() / df['Kills'].cumsum() * 100

df['Map'] = df['Map'].str.replace(' - Ranked', '')
df['Category'] = df['Category'].str.replace('3 Captures', '').str.replace('5 Captures', '')

df = df.drop(['Player', 'MatchId', 'Input', 'Queue', 'Mmr', 'WasAtStart', 'WasAtEnd',
            'WasInProgressJoin', 'AssistsEmp', 'AssistsDriver', 'AssistsCallout', 'VehicleDestroys',
            'VehicleHijacks', 'Perfects', 'PreCsr', 'SeasonNumber', 'SeasonVersion'],axis=1)
dfr = df[df['Date']> '2023-01-01']
dfr = dfr[dfr['Playlist'] == 'Ranked Arena']
dfr['Csr'] = dfr['PostCsr'].replace(0, method='ffill')
# dfr = dfr[dfr['Outcome'] != 'Draw']
dfr = dfr[dfr['Outcome'] != 'Left']
dfr['Outcome'] = dfr['Outcome'].map({'Win': 1, 'Loss': 0, 'Draw':0.5})
dfr['LifetimeWinRate'] = (dfr['Outcome'].cumsum() / 
                          (dfr['Outcome'].cumsum() + 
                           dfr['Outcome'].eq(0).cumsum())).fillna(0)
dfr = dfr.drop(['Playlist', 'PostCsr'], axis=1).reset_index()
dfr.loc[:4, 'Csr'] = 808
 # Scorigami
dfGami = pd.DataFrame()
dfGami['Kills'] = dfr['Kills']
dfGami['Deaths'] = dfr['Deaths']
dfGami['Assists'] = dfr['Assists']
dfGami['Scorigami'] = dfr['Kills'].astype(str) + '-' + dfr['Deaths'].astype(str) + '-' + dfr['Assists'].astype(str)
dfGami = dfGami.sort_values(by=['Kills', 'Deaths', 'Assists'], ascending=False)
gamiPiv = dfGami.pivot_table(index='Scorigami', aggfunc='size')
gamiPiv = gamiPiv.sort_index()



# Sidebar Filters
map_filter = st.sidebar.selectbox('Map', ['All'] + list(dfr['Map'].unique()), index=0)
mode_filter = st.sidebar.selectbox('Mode', ['All'] + list(dfr['Category'].unique()), index=0)
start_date = st.sidebar.date_input('Start Date', min_value=dfr['Date'].min(),  max_value=dt.date.today(), value=dfr['Date'].min())
end_date = st.sidebar.date_input('End Date', min_value=dfr['Date'].min(), max_value=dt.date.today(), value=dfr['Date'].max())
st.sidebar.markdown('To clear filters reload the webpage')
st.sidebar.markdown('\n')
st.sidebar.markdown("Made with ❤️ by [palmerac](https://github.com/palmerac)")
# Apply Filters
if 'All' in map_filter:
    dfr = dfr
else:
    dfr = dfr[dfr['Map'] == map_filter]

if 'All' in mode_filter:
    dfr = dfr
else:
    dfr = dfr[dfr['Category'] == mode_filter]

dfr = dfr[(dfr['Date'] >= np.datetime64(start_date)) & (dfr['Date'] <= np.datetime64(end_date))]

total_time_played = dfr['LengthMinutes'].sum()
days = total_time_played // (24 * 60)
hours = (total_time_played % (24 * 60)) // 60
minutes = total_time_played % 60

tab1, tab2, tab3, tab4 = st.tabs(['Summary', 'Charts', 'Last x Games', 'Statogami'])

with tab1:
    st.subheader('Summary')
    col1, col2 = st.columns(2)

    with col1:
        st.text(f"Total Time Played: {int(days)}d, {int(hours)}h, {int(minutes)}min")
        st.text(f"Games Played: {len(dfr)}")
        st.text(f"Current CSR: {dfr['Csr'].iloc[-1]}")
        st.text(f"Highest CSR: {dfr['Csr'].max()}")
        st.text(f"Winrate: {round(len(dfr[dfr['Outcome'] == 1]) / len(dfr[dfr['Outcome'] == 0]),2)}")
        st.text(f"Wins-Losses-Draws: {len(dfr[dfr['Outcome'] == 1])}-{len(dfr[dfr['Outcome'] == 0])}-{len(dfr[dfr['Outcome'] == 0.5])}")
        st.text(f"KD: {round(dfr['Kills'].sum() / dfr['Deaths'].sum(),2)}")
        st.text(f"Accuracy: {round(dfr['ShotsLanded'].sum() / dfr['ShotsFired'].sum()*100,2)}%")
        st.text(f"Damage Ratio: {round(dfr['DamageDone'].sum() / dfr['DamageTaken'].sum(),2)}")
        st.text(f"Damage/Life: {round(dfr['DamageDone'].sum() / dfr['Deaths'].sum(),2)}")
        st.text(f"Damage/KA: {round(dfr['DamageDone'].sum() / (dfr['Kills'].sum() + dfr['Assists'].sum()),2)}")


    with col2:
        for i in ['Kills', 'Deaths', 'Assists', 'DamageDone', 'DamageTaken', 'ShotsLanded', 'ShotsFired', 'Betrayals', 'Suicides', 'Medals']:
            total_value = dfr[i].sum()
            avg_value = round(total_value / len(dfr), 1)
            # Check if the total value is greater than 10,000
            if total_value > 10000:
                total_value_formatted = "{:,}".format(total_value)
            else:
                total_value_formatted = str(total_value)
            st.text(f"{i}: {total_value_formatted} ({avg_value})")
    

with tab2:
    tab21, tab22, tab23 = st.tabs(['Moving Average', 'Lifetime', 'Boxplot'])
    with tab21:
        # Create a dropdown list to select a column
        ma_cols = ['Csr', 'Kills', 'Kills/10Min', 'Deaths','Deaths/10Min', 'Assists', 'Assists/10Min',
                    'DamageDone', 'DamageDone/10Min', 'DamageTaken', 'DamageTaken/10Min', 'Damage/Life',
                    'Assists/Life', 'Damage/KA']
        selected_columns = st.multiselect('Select columns', ma_cols, default=ma_cols[0])

        # Create an input cell to enter a moving average period
        moving_average_period = st.number_input('Enter a moving average period', min_value=5, value=50, step=5)

        # Plot the selected value over time with a moving average
        fig, ax = plt.subplots(figsize=(16,10))
        for col in selected_columns:
            ax.plot(dfr.index, dfr[col].rolling(window=moving_average_period).mean())
        plt.title(f"{', '.join(selected_columns)} {moving_average_period} Game Moving Average")
        plt.xlabel('Index')
        plt.ylabel('Value')
        ax.legend()
        st.pyplot(fig)

    with tab22:
        # Create a dropdown list to select a column
        lf_cols = ['LifetimeKD', 'LifetimeDmgRatio', 'LifetimeAcc', 'LifetimeWinRate', 'Csr']
        selected_columns = st.multiselect('Select columns', lf_cols, default=lf_cols[0])

        # Plot the selected value over time with a moving average
        fig, ax = plt.subplots(figsize=(16,10))
        for col in selected_columns:
            ax.plot(dfr.index, dfr[col])
        plt.title(f"{', '.join(selected_columns).replace('Lifetime','')} Over Time")
        plt.xlabel('Index')
        plt.ylabel('Value')
        ax.legend()
        st.pyplot(fig)

    with tab23:
        columns = ['Kills', 'Deaths', 'Assists', 'KDA', 'DamageDone', 'DamageTaken', 'Csr', 'Accuracy']
        fig, axes = plt.subplots(nrows=4, ncols=2, figsize=(15, 15))
        axes = axes.flatten()
        for i, column in enumerate(columns):
            sns.boxplot(x=dfr[column], ax=axes[i])
            axes[i].set_title(column)
        plt.suptitle('Boxplots of Game Stats', fontsize=20)
        plt.tight_layout()
        st.pyplot(fig)

with tab3:
    st.subheader('Last x Games')
    tail = int(st.number_input('Enter value for x: ', step=5, value=10))

    tab31, tab32 = st.tabs(['Statistics', 'Raw Data'])
    dfTail = dfr.tail(tail)

    col31, col32, col33 = st.columns(3)
    with tab31:
        wins = len(dfTail[dfTail['Outcome'] == 1])
        losses = len(dfTail[dfTail['Outcome'] == 0])
        draws = len(dfTail[dfTail['Outcome'] == 0.5])
        st.text(f"Wins-Losses-Draws: {wins}-{losses}-{draws}")
        st.text(f"Winrate: {round(wins/losses,2)}")

        with col31:
            st.markdown('#### Regular')
            for i in ['Kills', 'Deaths', 'Assists']:
                st.text(f'{i}: {dfTail[i].sum()} ({round(dfTail[i].sum()/tail,1)})')
            st.text(f"KD: {round(dfTail['Kills'].sum() / dfTail['Deaths'].sum(),2)}")
            st.text(f"Damage Ratio: {round(dfTail['DamageDone'].sum() / dfTail['DamageTaken'].sum(),2)}")
            st.text(f"Accuracy: {round(dfTail['ShotsLanded'].sum() / dfTail['ShotsFired'].sum()*100,2)}")
        
        with col32:
            st.markdown('#### Per 10 Min')
            for i in ['Kills/10Min', 'Deaths/10Min', 'Assists/10Min']:
                st.text(f'{i.replace("/10Min", "")}: {round(dfTail[i].sum(),)} ({round(dfTail[i].sum()/tail,1)})')
            st.text(f"KD: {round(dfTail['Kills/10Min'].sum() / dfTail['Deaths/10Min'].sum(), 2)}")
            st.text(f"Damage Ratio: {round(dfTail['DamageDone/10Min'].sum() / dfTail['DamageTaken/10Min'].sum(), 2)}")
            st.text(f"Accuracy: {round(dfTail['ShotsLanded/10Min'].sum() / dfTail['ShotsFired/10Min'].sum()*100, 2)}")


    with tab32:
        st.dataframe(dfTail)

with tab4: 
    st.subheader('Statogami')
    st.text("Inspired by the NFL's scorigami but its statlines that are repeated instead of unique ones")
    gamict = st.number_input("Enter minimum duplicate count", min_value=2)
    st.text(f"Records with >= {gamict} duplicates: {gamiPiv[gamiPiv.values>=gamict].count()}")
    st.dataframe(gamiPiv[gamiPiv.values>=gamict].sort_values(ascending=False))