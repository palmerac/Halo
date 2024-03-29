import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initial Setup
st.set_page_config(layout="wide")

# Title and Intro Text
st.title("Halo Infinite Dashboard")
st.markdown("\n  ")
st.text("This is a dashboard for my Halo Infinite ranked games.")
st.text("It has a bunch of graphs and statistics.")
st.markdown("Created with ❤️ by [Aaron Palmer](https://github.com/palmerac/).")
st.markdown("\n  ")

# Read/Convert CSV for raw and W/L dataframes
df = pd.read_csv("df.csv")
dfw = df[df["Outcome"] == 1]
dfl = df[df["Outcome"] == 0]

# Functions for stats
def avg(df, col, rnd=None):
    ans = round(df[col].mean(), rnd)
    return ans

def med(df, col, rnd=None):
    ans = round(df[col].median(), rnd)
    return ans

def tot(df, col, rnd=None):
    ans = round(df[col].sum(), rnd)
    return ans

def cnt(df, col):
    ans = len(df[col])
    return ans

def acc(df, rnd=None):
    ans = round(df['ShotsLanded'].sum() / df['ShotsFired'].sum() * 100,rnd)
    return ans

# Pivot Tables for Map/GameMode 
# Map Stats
mapKD = df.pivot_table(index='Map', 
                        values=['Kills', 'Deaths', 'Assists', 'Accuracy', 'DamageDone', 'DamageTaken', 'Outcome'], 
                        aggfunc='mean')

desired_col_order = ['Kills', 'Deaths', 'Assists', 'Accuracy', 'DamageDone', 'DamageTaken','Outcome']

mapKD = mapKD.reindex(desired_col_order, axis=1)
mapKD = mapKD.round(2)
mapKD[['DamageDone', 'DamageTaken']] = mapKD[['DamageDone', 'DamageTaken']].round()

# Map per 10 min stats
map10KD = df.pivot_table(index='Map', 
                        values=['Kills/10Min', 'Deaths/10Min', 'Assists/10Min', 'Dmg/10Min', 'DmgT/10Min', 'Outcome'], 
                        aggfunc='mean')

desired_col10_order = ['Kills/10Min', 'Deaths/10Min', 'Assists/10Min', 'Dmg/10Min', 'DmgT/10Min', 'Outcome']

map10KD = map10KD.reindex(desired_col10_order, axis=1)
map10KD = map10KD.round(2)
map10KD[['Dmg/10Min', 'DmgT/10Min']] = map10KD[['Dmg/10Min', 'DmgT/10Min']].round()

# GameMode Stats
catKD = df.pivot_table(index='Category', 
                        values=['Kills', 'Deaths', 'Assists', 'Accuracy', 'DamageDone', 'DamageTaken','Outcome'], 
                        aggfunc='mean')

desired_col_order = ['Kills', 'Deaths', 'Assists', 'Accuracy', 'DamageDone', 'DamageTaken','Outcome']

catKD = catKD.reindex(desired_col_order, axis=1)
catKD = catKD.round(2)
catKD[['DamageDone', 'DamageTaken']] = catKD[['DamageDone', 'DamageTaken']].round()

# GameMode per 10 min stats
cat10KD = df.pivot_table(index='Category', 
                        values=['Kills/10Min', 'Deaths/10Min', 'Assists/10Min', 'Dmg/10Min', 'DmgT/10Min', 'Outcome'], 
                        aggfunc='mean')

desired_col10_order = ['Kills/10Min', 'Deaths/10Min', 'Assists/10Min', 'Dmg/10Min', 'DmgT/10Min', 'Outcome']

cat10KD = cat10KD.reindex(desired_col10_order, axis=1)
cat10KD = cat10KD.round(2)
cat10KD[['Dmg/10Min', 'DmgT/10Min']] = cat10KD[['Dmg/10Min', 'DmgT/10Min']].round()

# Map/Mode Stats
catmapKD = df.pivot_table(index=['Map', 'Category'], 
                        values=['Kills', 'Deaths', 'Assists', 'Accuracy', 'DamageDone', 'DamageTaken','Outcome'], 
                        aggfunc='mean')

desired_col_order = ['Kills', 'Deaths', 'Assists', 'Accuracy', 'DamageDone', 'DamageTaken','Outcome']

catmapKD = catmapKD.reindex(desired_col_order, axis=1)
catmapKD = catmapKD.round(2)
catmapKD[['DamageDone', 'DamageTaken']] = catmapKD[['DamageDone', 'DamageTaken']].round()

# Map/Mode per 10 min stats
catmap10KD = df.pivot_table(index=['Map', 'Category'], 
                        values=['Kills/10Min', 'Deaths/10Min', 'Assists/10Min', 'Dmg/10Min', 'DmgT/10Min', 'Outcome'], 
                        aggfunc='mean')

desired_col10_order = ['Kills/10Min', 'Deaths/10Min', 'Assists/10Min', 'Dmg/10Min', 'DmgT/10Min', 'Outcome']

catmap10KD = catmap10KD.reindex(desired_col10_order, axis=1)
catmap10KD = catmap10KD.round(2)
catmap10KD[['Dmg/10Min', 'DmgT/10Min']] = catmap10KD[['Dmg/10Min', 'DmgT/10Min']].round()

# Totals
st.write("Win-Loss:", cnt(dfw, "Outcome"), "-", cnt(dfl, "Outcome"))
st.write("Current CSR:", df['Csr'].iloc[-1])
st.write("Maximum CSR:", df['Csr'].max())
st.write("Time Played(h):", round(tot(df, 'LengthSeconds')/60/60,2))
st.write("Kills:",tot(df,"Kills",),)
st.write("Deaths:",tot(df,"Deaths",),)
st.write("Assists:",tot(df,"Assists",),)
st.write("Accuracy(%):",acc(df,2),)
st.write("Medals:",tot(df,"Medals",),)
st.write("Damage Done:",tot(df,"DamageDone",),)
st.write("Damage Taken:",tot(df,"DamageTaken",),)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "KD/Damage/WR/Acc Over Time",
        "KD/Damage/CSR Over Time",
        "Boxplots",
        "Stats in Wins vs Losses",
        "Map & Mode Stats",
        "Map/Mode Stats",
        "Raw Data",
    ]
)

with tab1:
    st.image("Plots/DamKDWRAcc.png")
    pass

with tab2:
    st.image("Plots/KDDamCSR.gif")
    pass

with tab3:
    st.image("Plots/Boxplots.png")
    pass

with tab4:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("## Total")
        st.write("Average Kills:", avg(df, "Kills", 2))
        st.write("Average Deaths:", avg(df, "Deaths", 2))
        st.write("KD Ratio:", round(tot(df,"Kills") / tot(df, "Deaths"),2))
        st.write("Average Assists:", avg(df, "Assists", 2))
        st.write("Accuracy(%):", acc(df,2))
        st.write("Damage Ratio:", round(tot(df, "DamageDone") / tot(df, "DamageTaken"), 2))
        st.write("Average Damage Done:", avg(df, "DamageDone",))
        st.write("Average Damage Taken:", avg(df, "DamageTaken",))
        st.markdown("  \n  ")
        st.markdown('#### Per 10 Minute Stats')
        st.write("Average Kills/10Min:", avg(df, "Kills/10Min", 2))
        st.write("Average Deaths/10Min:", avg(df, "Deaths/10Min", 2))
        st.write("Average Assists/10Min:", avg(df, "Assists/10Min", 2))
        st.write("Average Damage/10Min:", avg(df, "Dmg/10Min",)) 
        st.write("Average Damage Taken/10Min:", avg(df, "DmgT/10Min",))
        pass
    
    with col2:
        st.markdown("## Wins")
        st.write("Average Kills:", avg(dfw, "Kills", 2))
        st.write("Average Deaths:", avg(dfw, "Deaths", 2))
        st.write("KD Ratio:", round(tot(dfw,"Kills") / tot(dfw, "Deaths"),2))
        st.write("Average Assists:", avg(dfw, "Assists", 2))
        st.write("Accuracy(%):", acc(dfw,2))
        st.write("Damage Ratio:", round(tot(dfw, "DamageDone") / tot(dfw, "DamageTaken"), 2))
        st.write("Average Damage Done:", avg(dfw, "DamageDone",))
        st.write("Average Damage Taken:", avg(dfw, "DamageTaken",))
        st.markdown("  \n  ")
        st.markdown('#### Per 10 Minute Stats')
        st.write("Average Kills/10Min:", avg(dfw, "Kills/10Min", 2))
        st.write("Average Deaths/10Min:", avg(dfw, "Deaths/10Min", 2))
        st.write("Average Assists/10Min:", avg(dfw, "Assists/10Min", 2))
        st.write("Average Damage/10Min:", avg(dfw, "Dmg/10Min",)) 
        st.write("Average Damage Taken/10Min:", avg(dfw, "DmgT/10Min",))
        pass

    with col3:
        st.markdown("## Losses")
        st.write("Average Kills:", avg(dfl, "Kills", 2))
        st.write("Average Deaths:", avg(dfl, "Deaths", 2))
        st.write("KD Ratio:", round(tot(dfl,"Kills") / tot(dfl, "Deaths"),2))
        st.write("Average Assists:", avg(dfl, "Assists", 2))
        st.write("Accuracy(%):", acc(dfl,2))
        st.write("Damage Ratio:", round(tot(dfl, "DamageDone") / tot(dfl, "DamageTaken"), 2))
        st.write("Average Damage Done:", avg(dfl, "DamageDone",))
        st.write("Average Damage Taken:", avg(dfl, "DamageTaken",))
        st.markdown("  \n  ")
        st.markdown('#### Per 10 Minute Stats')
        st.write("Average Kills/10Min:", avg(dfl, "Kills/10Min", 2))
        st.write("Average Deaths/10Min:", avg(dfl, "Deaths/10Min", 2))
        st.write("Average Assists/10Min:", avg(dfl, "Assists/10Min", 2))
        st.write("Average Damage/10Min:", avg(dfl, "Dmg/10Min",)) 
        st.write("Average Damage Taken/10Min:", avg(dfl, "DmgT/10Min",))
        
        pass

with tab5:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('## Map Stats')
        st.dataframe(mapKD)
        st.markdown('#### Per 10 min')
        st.dataframe(map10KD)
        pass
    with col2:
        st.markdown('## Mode Stats')
        st.dataframe(catKD)
        st.markdown('\n\n  ')
        st.markdown('#### Per 10 min')
        st.dataframe(cat10KD)
        pass
    pass
    st.image('Plots/ModeDistro.png')

with tab6:
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('## Map/Mode')
        st.dataframe(catmapKD)
        pass
    with col2:
        st.markdown('## Map/Mode Per 10 Min')
        st.dataframe(catmap10KD)
        pass
    pass

with tab7:
    st.dataframe(df)
    pass
