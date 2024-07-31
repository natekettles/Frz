# app.py
import streamlit as st
import pandas as pd
import requests

def fetch_norris_data(start_year, end_year):
    data = []
    for year in range(start_year, end_year + 1):
        url = f"http://ergast.com/api/f1/{year}/drivers/norris/results.json"
        response = requests.get(url)
        if response.status_code == 200:
            races = response.json()['MRData']['RaceTable']['Races']
            for race in races:
                race_name = race['raceName']
                round_number = race['round']
                if 'Results' in race and len(race['Results']) > 0:
                    result = race['Results'][0]
                    grid = result['grid']
                    position = result['position']
                    data.append([year, round_number, race_name, grid, position])
    
    return pd.DataFrame(data, columns=['Year', 'Round', 'Race', 'Grid Position', 'Final Position'])

st.title('Lando Norris Race Data')

start_year = st.number_input('Start Year', min_value=2019, max_value=2023, value=2020)
end_year = st.number_input('End Year', min_value=2019, max_value=2023, value=2023)

if st.button('Fetch Data'):
    with st.spinner('Fetching data...'):
        df = fetch_norris_data(start_year, end_year)
    
    if not df.empty:
        st.dataframe(df)
        
        # Calculate some statistics
        total_races = len(df)
        avg_grid = df['Grid Position'].astype(int).mean()
        avg_finish = df['Final Position'].astype(int).mean()
        
        st.subheader('Statistics')
        st.write(f"Total Races: {total_races}")
        st.write(f"Average Grid Position: {avg_grid:.2f}")
        st.write(f"Average Finish Position: {avg_finish:.2f}")
    else:
        st.write("No data found for the selected years.")
