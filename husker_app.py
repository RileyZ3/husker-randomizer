import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# Set up the look of the website
st.set_page_config(page_title="Husker Hoops Randomizer", page_icon="🌽")
st.title("🔴 Nebraska Basketball Time Machine")
st.write("Pick a season, and the app will instantly grab that specific roster from the web!")

# 1. Create a dropdown for the years
selected_year = st.selectbox("Choose a Season:", list(range(2025, 1949, -1)))

# 2. The function to scrape ONLY the selected year
def get_single_roster(year):
    # The real URL where the stats live
    target_url = f"https://www.sports-reference.com/cbb/schools/nebraska/men/{year}.html"
    
    # THE FIX: Bounce the request through a public proxy so we don't look like a server
    proxy_url = f"https://api.allorigins.win/raw?url={target_url}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        # Ask the proxy for the data instead of asking Sports Reference directly
        response = requests.get(proxy_url, headers=headers, timeout=10)
        
        # If the proxy or Sports Reference fails, return None
        if response.status_code != 200:
            return None, target_url
            
        soup = BeautifulSoup(response.text, 'html.parser')
        players = []
        
        # Look directly for the player names on that specific page
        for player_cell in soup.find_all('td', {'data-stat': 'player'}):
            a_tag = player_cell.find('a')
            if a_tag:
                players.append(a_tag.text.strip())
                
        # Remove duplicates
        players = list(set(players))
        return players, target_url
        
    except Exception as e:
        # If the connection times out, catch the error so the app doesn't crash
        return None, target_url

# 3. The Button that triggers the scrape
if st.button(f"Get {selected_year} Roster & Pick a Player 🏀"):
    with st.spinner(f"Traveling to {selected_year} to find the roster..."):
        roster, url = get_single_roster(selected_year)
        
    if roster:
        st.success(f"Success! Found {len(roster)} players on the {selected_year} team.")
        
        # Pick a random player
        lucky_player = random.choice(roster)
        
        st.divider()
        st.subheader(f"⭐ Your Random Player: **{lucky_player}**")
        st.link_button(f"View {selected_year} Team Stats on Sports Reference", url)
        
        # Show the whole roster
        with st.expander(f"See everyone on the {selected_year} roster"):
            for p in sorted(roster):
                st.write(f"- {p}")
    else:
        st.error(f"Could not find a roster for {selected_year}. The proxy might be blocked, or the data doesn't exist!")
