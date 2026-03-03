import streamlit as st
import requests
from bs4 import BeautifulSoup
import random

# Set up the look of the website
st.set_page_config(page_title="Husker Hoops Randomizer", page_icon="🌽")
st.title("🔴 Nebraska Basketball Time Machine")
st.write("Pick a season, and the app will instantly grab that specific roster from the web!")

# 1. Create a dropdown for the years
# Nebraska basketball goes back a long way, let's do 1950 to the present!
selected_year = st.selectbox("Choose a Season:", list(range(2025, 1949, -1)))

# 2. The function to scrape ONLY the selected year
def get_single_roster(year):
    url = f"https://www.sports-reference.com/cbb/schools/nebraska/men/{year}.html"
    
    # Act like a normal web browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    
    # If the page doesn't exist or blocks us, stop here
    if response.status_code != 200:
        return None, url
        
    soup = BeautifulSoup(response.text, 'html.parser')
    players = []
    
    # Look directly for the player names on that specific page
    for player_cell in soup.find_all('td', {'data-stat': 'player'}):
        a_tag = player_cell.find('a')
        if a_tag:
            players.append(a_tag.text.strip())
            
    # Remove duplicates (sometimes players are listed twice in different tables)
    players = list(set(players))
    return players, url

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
        
        # Optional: Show the whole roster so the user knows it worked
        with st.expander(f"See everyone on the {selected_year} roster"):
            for p in sorted(roster):
                st.write(f"- {p}")
    else:
        st.error(f"Could not find a roster for {selected_year}. The data might not exist for that year!")
