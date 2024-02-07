# Halo Infinte Stat Dashboard

original csv was obtained from https://leafapp.co  
dashboard is a work in progress and at [streamlit](https://palmerac-halo.streamlit.app)  

halo.ipynb - stats since the start of bandit season, df.csv  
haloNS.ipynb - since MMR reset ~(Feb 3, 2024), dfNS.csv  
haloModels.ipynb - forked from Tennis ML models and updated to predict Win/Loss, work in progress dont think values are working right  

matchhistory-old.csv - an outdated format of the original csv, new one has more info  
scorigami.csv - list of the scorigami values that are duplicates (happened more than once)  
requirements.txt - requirements for streamlit website  

Plots are fairly self explanatory  

Could be ran for any user by: 
1. Fork/Cloning Repo
2. Getting User Data from https://leafapp.co/player/{username}/matches
   1. 'Request Stat Update' then 'export to csv'
3. Fix file path to new user data in cell 2 of halo.ipynb
4. Run all cells
