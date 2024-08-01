# app.py
import streamlit as st
import fastf1
import pandas as pd

def fetch_data():
    # Enable cache
    fastf1.Cache.enable_cache('cache')

    # Initialize an empty list to store the data
    data = []

    # Loop through years from 2020 to the current year
    for year in range(2020, 2025):  # Assuming the current year is 2024
        # Load the schedule for the year
        schedule = fastf1.get_event_schedule(year)
        
        # Loop through each event in the schedule
        for event in schedule.index:
            try:
                # Load the race session
                race = fastf1.get_session(year, event, 'R')
                race.load()
                
                # Get Lando Norris's data
                driver_data = race.results.loc[race.results['Abbreviation'] == 'NOR']
                
                if not driver_data.empty:
                    starting_position = driver_data['GridPosition'].values[0]
                    
                    # Get position after lap 1
                    laps = race.laps.pick_driver('NOR')
                    if not laps.empty:
                        position_lap_1 = laps.loc[laps['LapNumber'] == 1, 'Position'].values[0]
                    else:
                        position_lap_1 = "N/A"
                    
                    # Append the data to our list
                    data.append([year, race.event['EventName'], starting_position, position_lap_1])
            except Exception as e:
                st.error(f"Error processing {year} {event}: {str(e)}")

    # Create a DataFrame from the collected data
    return pd.DataFrame(data, columns=['Year', 'Race', 'Starting Position', 'Position After Lap 1'])

st.title('Lando Norris Race Data (2020-2024)')

if st.button('Fetch Data'):
    with st.spinner('Fetching data...'):
        df = fetch_data()
    st.dataframe(df)
